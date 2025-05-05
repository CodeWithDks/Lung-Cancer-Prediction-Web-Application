import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Flask configuration
DEBUG = os.getenv('DEBUG', 'True') == 'True'
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 5000))

# MongoDB Atlas configuration
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/lung_cancer_app')
DB_NAME = os.getenv('DB_NAME', 'lung-cancer-app')
PREDICTION_COLLECTION = 'predictions'

# Model configuration
MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                          'models', 'lung_cancer_model.pkl')

# Feature names (must match model training order)
FEATURE_NAMES = [
    'GENDER', 'AGE', 'SMOKING', 'YELLOW_FINGERS', 'ANXIETY', 
    'PEER_PRESSURE', 'CHRONIC DISEASE', 'FATIGUE', 'ALLERGY', 
    'WHEEZING', 'ALCOHOL CONSUMING', 'COUGHING', 
    'SHORTNESS OF BREATH', 'SWALLOWING DIFFICULTY', 'CHEST PAIN'
]

# Label mapping
CLASS_LABELS = {0: "No Cancer", 1: "Lung Cancer"}

# Feature display names for UI
FEATURE_DISPLAY_NAMES = {
    'GENDER': 'Gender',
    'AGE': 'Age',
    'SMOKING': 'Smoking',
    'YELLOW_FINGERS': 'Yellow Fingers',
    'ANXIETY': 'Anxiety',
    'PEER_PRESSURE': 'Peer Pressure',
    'CHRONIC DISEASE': 'Chronic Disease',
    'FATIGUE': 'Fatigue',
    'ALLERGY': 'Allergy',
    'WHEEZING': 'Wheezing',
    'ALCOHOL CONSUMING': 'Alcohol Consumption',
    'COUGHING': 'Coughing',
    'SHORTNESS OF BREATH': 'Shortness of Breath',
    'SWALLOWING DIFFICULTY': 'Swallowing Difficulty',
    'CHEST PAIN': 'Chest Pain'
}

# Feature options for UI (1=No, 2=Yes except for gender)
FEATURE_OPTIONS = {
    'GENDER': [
        {'value': 0, 'label': 'Female'},
        {'value': 1, 'label': 'Male'}
    ],
    'SMOKING': [
        {'value': 1, 'label': 'No'},
        {'value': 2, 'label': 'Yes'}
    ],
    'YELLOW_FINGERS': [
        {'value': 1, 'label': 'No'},
        {'value': 2, 'label': 'Yes'}
    ],
    'ANXIETY': [
        {'value': 1, 'label': 'No'},
        {'value': 2, 'label': 'Yes'}
    ],
    'PEER_PRESSURE': [
        {'value': 1, 'label': 'No'},
        {'value': 2, 'label': 'Yes'}
    ],
    'CHRONIC DISEASE': [
        {'value': 1, 'label': 'No'},
        {'value': 2, 'label': 'Yes'}
    ],
    'FATIGUE': [
        {'value': 1, 'label': 'No'},
        {'value': 2, 'label': 'Yes'}
    ],
    'ALLERGY': [
        {'value': 1, 'label': 'No'},
        {'value': 2, 'label': 'Yes'}
    ],
    'WHEEZING': [
        {'value': 1, 'label': 'No'},
        {'value': 2, 'label': 'Yes'}
    ],
    'ALCOHOL CONSUMING': [
        {'value': 1, 'label': 'No'},
        {'value': 2, 'label': 'Yes'}
    ],
    'COUGHING': [
        {'value': 1, 'label': 'No'},
        {'value': 2, 'label': 'Yes'}
    ],
    'SHORTNESS OF BREATH': [
        {'value': 1, 'label': 'No'},
        {'value': 2, 'label': 'Yes'}
    ],
    'SWALLOWING DIFFICULTY': [
        {'value': 1, 'label': 'No'},
        {'value': 2, 'label': 'Yes'}
    ],
    'CHEST PAIN': [
        {'value': 1, 'label': 'No'},
        {'value': 2, 'label': 'Yes'}
    ]
}