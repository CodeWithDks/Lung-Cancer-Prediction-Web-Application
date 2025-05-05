# Lung Cancer Prediction Web Application

A full-stack web application for predicting lung cancer risk using machine learning. The application takes various patient attributes and uses a trained Random Forest model to assess the likelihood of lung cancer.

## Features

- User-friendly web interface for entering patient data
- Machine learning-based prediction using a Random Forest model
- Results visualization and interpretation
- Storage of prediction history in MongoDB Atlas
- REST API for programmatic access

## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Database**: MongoDB Atlas
- **ML Model**: Scikit-learn Random Forest Classifier

## Project Structure

```
lung_cancer_app/
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
│
├── templates/
│   ├── index.html
│   └── result.html
│
├── models/
│   └── lung_cancer_model.pkl
│
├── app.py                  # Flask application
├── database.py             # MongoDB connection and functions
├── model_utils.py          # Model loading and prediction functions
├── config.py               # Configuration settings
└── requirements.txt        # Project dependencies
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd lung_cancer_app
   ```

2. Set up a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up MongoDB Atlas:
   - Create a MongoDB Atlas account and cluster (see MongoDB_Setup.md for detailed instructions)
   - Update the `.env` file with your MongoDB Atlas connection string

5. Make sure you have the trained model file:
   - Place your `lung_cancer_model.pkl` file in the `models/` directory

## Running the Application

1. Start the Flask server:
   ```
   python app.py
   ```

2. Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

## API Endpoints

The application provides the following API endpoints:

- `POST /predict` - Submit patient data for prediction
  - Accepts JSON data with patient attributes
  - Returns prediction result and probability

- `GET /api/predictions` - Get all prediction history
  - Returns a JSON array of all predictions

- `GET /api/prediction/<prediction_id>` - Get specific prediction
  - Returns JSON data for a specific prediction

## Model Information

The lung cancer prediction model was trained using a Random Forest Classifier with the following feature importance:

1. ALLERGY (0.312)
2. ALCOHOL CONSUMING (0.191)
3. PEER_PRESSURE (0.088)
4. CHRONIC DISEASE (0.080)
5. YELLOW_FINGERS (0.073)
6. FATIGUE (0.053)
7. SWALLOWING DIFFICULTY (0.046)
8. COUGHING (0.029)
9. GENDER (0.028)
10. WHEEZING (0.024)
11. AGE (0.023)
12. ANXIETY (0.019)
13. SHORTNESS OF BREATH (0.015)
14. SMOKING (0.010)
15. CHEST PAIN (0.008)

## Future Enhancements

- User authentication and personal prediction history
- Detailed visualization of risk factors
- Email reports for healthcare providers
- Integration with electronic health record systems
- Mobile application version

## Disclaimer

This application is for educational and demonstration purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.