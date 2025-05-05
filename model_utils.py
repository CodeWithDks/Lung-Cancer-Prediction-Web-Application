import joblib
import pandas as pd
import logging
import os
from config import MODEL_PATH, FEATURE_NAMES, CLASS_LABELS

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelManager:
    def __init__(self):
        self.model = None
        self.load_model()

    def load_model(self):
        """Load the trained model from file"""
        try:
            # Check if model file exists
            if not os.path.exists(MODEL_PATH):
                raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
            
            # Load the model
            self.model = joblib.load(MODEL_PATH)
            logger.info(f"Model loaded successfully from {MODEL_PATH}")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise

    def validate_input(self, data):
        """
        Validate input data for prediction
        
        Args:
            data (dict): Dictionary with patient attributes
            
        Returns:
            pandas.DataFrame: Validated DataFrame ready for prediction
            
        Raises:
            ValueError: If validation fails
        """
        try:
            # Convert to DataFrame
            df = pd.DataFrame([data], columns=FEATURE_NAMES)
            
            # 1. Data type validation
            for col in FEATURE_NAMES:
                try:
                    df[col] = pd.to_numeric(df[col])
                except:
                    raise ValueError(f"Non-numeric value in column {col}")
            
            # 2. Value range checks
            # GENDER (0=Female, 1=Male)
            if not df['GENDER'].isin([0, 1]).all():
                invalid = df[~df['GENDER'].isin([0,1])]['GENDER'].unique()
                raise ValueError(f"GENDER must be 0 (Female) or 1 (Male). Invalid values: {invalid}")
            
            # AGE (0-120 years)
            if (df['AGE'] < 0).any() or (df['AGE'] > 120).any():
                invalid = df[(df['AGE'] < 0) | (df['AGE'] > 120)]['AGE'].values
                raise ValueError(f"AGE must be 0-120. Invalid values: {invalid}")
            
            # Symptoms (1=No, 2=Yes)
            symptom_cols = [col for col in FEATURE_NAMES if col not in ['GENDER', 'AGE']]
            for col in symptom_cols:
                if not df[col].isin([1, 2]).all():
                    invalid = df[~df[col].isin([1,2])][col].unique()
                    raise ValueError(f"{col} must be 1 (No) or 2 (Yes). Invalid values: {invalid}")
            
            return df
        except Exception as e:
            logger.error(f"Input validation failed: {e}")
            raise ValueError(f"Input validation failed: {e}")

    def predict(self, data):
        """
        Make prediction with validated data
        
        Args:
            data (dict): Dictionary with patient attributes
            
        Returns:
            dict: Prediction results
        """
        try:
            # Validate input
            df = self.validate_input(data)
            
            # Make prediction
            prediction_class = self.model.predict(df)[0]
            prediction_label = CLASS_LABELS[prediction_class]
            
            # Get probability if available
            probability = None
            try:
                probability = float(self.model.predict_proba(df)[0][1])  # Probability of positive class
            except:
                logger.warning("Probability prediction not available")
            
            result = {
                "prediction": prediction_label,
                "prediction_class": int(prediction_class)
            }
            
            if probability is not None:
                result["probability"] = probability
            
            return result
        except Exception as e:
            logger.error(f"Prediction failed: {e}")
            raise