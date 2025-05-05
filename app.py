from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_cors import CORS
import logging
import os
import json
from model_utils import ModelManager
from database import Database
import config
from flask import send_from_directory


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for API requests

# Initialize model and database
model_manager = None
db = None

@app.before_request
def initialize_app():
    if not hasattr(app, 'initialized'):
        app.initialized = True
        global model_manager, db
        
        # Initialize model
        try:
            model_manager = ModelManager()
            logger.info("Model manager initialized")
        except Exception as e:
            logger.error(f"Failed to initialize model: {e}")
        
        # Initialize database
        try:
            db = Database()
            logger.info("Database initialized")
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")

# Add this route to handle favicon (place it before your index route)
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                           'favicon.ico', mimetype='image/vnd.microsoft.icon')


# Modify your index route to ensure variables are always passed
@app.route('/')
def index():
    """Render the main page with the prediction form"""
    return render_template('index.html', 
                          feature_names=config.FEATURE_NAMES,
                          feature_display_names=config.FEATURE_DISPLAY_NAMES,
                          feature_options=config.FEATURE_OPTIONS,
                          error=None)  # Explicitly pass error as None

@app.route('/predict', methods=['POST'])
def predict():
    """Handle prediction request"""
    try:
        # Extract data from form or JSON
        if request.is_json:
            data = request.get_json()
        else:
            data = {}
            for feature in config.FEATURE_NAMES:
                value = request.form.get(feature)
                # Convert to appropriate type
                if feature == 'AGE':
                    data[feature] = int(value) if value and value.isdigit() else 0
                else:
                    data[feature] = int(value) if value and value.isdigit() else 1  # Default to 1 = No
        
        # Validate all required features
        missing_features = [f for f in config.FEATURE_NAMES if f not in data]
        if missing_features:
            raise ValueError(f"Missing input for: {', '.join(missing_features)}")
        
        # Make prediction
        result = model_manager.predict(data)

        # Save prediction to database
        if db:
            prediction_id = db.insert_prediction(
                patient_data=data,
                prediction=result.get('prediction'),
                prediction_probability=result.get('probability')
            )
            result['prediction_id'] = str(prediction_id)  # Cast to string for JSON/template safety

        # Return JSON or render HTML
        if request.is_json:
            return jsonify(result)
        else:
            return render_template('result.html',
                                   result=result,
                                   patient_data=data,
                                   feature_display_names=config.FEATURE_DISPLAY_NAMES,
                                   feature_options=config.FEATURE_OPTIONS)

    except ValueError as e:
        error_message = str(e)
        if request.is_json:
            return jsonify({'error': error_message}), 400
        else:
            return render_template('index.html',
                                   error=error_message,
                                   feature_names=config.FEATURE_NAMES,
                                   feature_display_names=config.FEATURE_DISPLAY_NAMES,
                                   feature_options=config.FEATURE_OPTIONS)

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        logger.exception(error_message)  # Use exception() for stack trace in logs
        if request.is_json:
            return jsonify({'error': error_message}), 500
        else:
            return render_template('index.html',
                                   error=error_message,
                                   feature_names=config.FEATURE_NAMES,
                                   feature_display_names=config.FEATURE_DISPLAY_NAMES,
                                   feature_options=config.FEATURE_OPTIONS)


@app.route('/history')
def history():
    """Show prediction history"""
    try:
        # Get predictions from database
        predictions = db.get_all_predictions() if db else []
        
        # Render template with predictions
        return render_template('result.html', 
                            predictions=predictions,
                            feature_display_names=config.FEATURE_DISPLAY_NAMES,
                            feature_options=config.FEATURE_OPTIONS)
    except Exception as e:
        logger.error(f"Failed to fetch prediction history: {e}")
        return redirect(url_for('index'))

@app.route('/api/predictions', methods=['GET'])
def api_predictions():
    """API endpoint to get prediction history"""
    try:
        # Get predictions from database
        predictions = db.get_all_predictions() if db else []
        return jsonify(predictions)
    except Exception as e:
        logger.error(f"API error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/prediction/<prediction_id>', methods=['GET'])
def api_prediction(prediction_id):
    """API endpoint to get specific prediction"""
    try:
        # Get prediction from database
        prediction = db.get_prediction_by_id(prediction_id) if db else None
        
        if prediction:
            return jsonify(prediction)
        else:
            return jsonify({'error': 'Prediction not found'}), 404
    except Exception as e:
        logger.error(f"API error: {e}")
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors"""
    return render_template('index.html', error="Page not found"), 404

@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors"""
    return render_template('index.html', error="Server error"), 500

if __name__ == '__main__':
    # Fix issue with initialization in development mode
    with app.app_context():
        if model_manager is None:
            model_manager = ModelManager()
        if db is None:
            db = Database()
    
    # Run the app
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)