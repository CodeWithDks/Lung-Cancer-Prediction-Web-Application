from pymongo import MongoClient
import datetime
import config
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.client = None
        self.db = None
        self.collection = None
        self.connect()

    def connect(self):
        """Connect to MongoDB Atlas"""
        try:
            self.client = MongoClient(config.MONGO_URI)
            self.db = self.client[config.DB_NAME]
            self.collection = self.db[config.PREDICTION_COLLECTION]
            logger.info("Connected to MongoDB Atlas")
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB Atlas: {e}")
            raise

    def insert_prediction(self, patient_data, prediction, prediction_probability=None):
        """
        Insert prediction data into MongoDB
        
        Args:
            patient_data (dict): Patient attributes used for prediction
            prediction (str): Prediction result (cancer/no cancer)
            prediction_probability (float, optional): Probability score of prediction
        
        Returns:
            str: ID of inserted document
        """
        try:
            # Prepare document to insert
            doc = {
                "patient_data": patient_data,
                "prediction": prediction,
                "timestamp": datetime.datetime.utcnow()
            }
            
            # Add probability if available
            if prediction_probability is not None:
                doc["probability"] = prediction_probability
                
            # Insert document
            result = self.collection.insert_one(doc)
            logger.info(f"Inserted prediction with ID: {result.inserted_id}")
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Failed to insert prediction: {e}")
            raise

    def get_all_predictions(self, limit=100):
        """
        Get recent predictions from database
        
        Args:
            limit (int): Maximum number of records to return
            
        Returns:
            list: List of prediction documents
        """
        try:
            cursor = self.collection.find().sort("timestamp", -1).limit(limit)
            predictions = list(cursor)
            # Convert ObjectId to string for JSON serialization
            for pred in predictions:
                pred["_id"] = str(pred["_id"])
            return predictions
        except Exception as e:
            logger.error(f"Failed to retrieve predictions: {e}")
            return []

    def get_prediction_by_id(self, prediction_id):
        """
        Get a specific prediction by ID
        
        Args:
            prediction_id (str): ID of prediction to retrieve
            
        Returns:
            dict: Prediction document
        """
        try:
            from bson.objectid import ObjectId
            prediction = self.collection.find_one({"_id": ObjectId(prediction_id)})
            if prediction:
                prediction["_id"] = str(prediction["_id"])
            return prediction
        except Exception as e:
            logger.error(f"Failed to retrieve prediction {prediction_id}: {e}")
            return None

    def close(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            logger.info("Closed MongoDB connection")