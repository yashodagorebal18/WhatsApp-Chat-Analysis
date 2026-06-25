"""
Configuration file for WhatsApp Chat Analyzer
"""

# Application Settings
APP_NAME = "WhatsApp Chat Analyzer"
APP_VERSION = "2.0.0"
APP_DESCRIPTION = "Advanced Full-Stack WhatsApp Chat Analysis Platform"

# Flask Configuration
FLASK_HOST = "0.0.0.0"
FLASK_PORT = 5000
FLASK_DEBUG = True

# Streamlit Configuration
STREAMLIT_PORT = 8501
STREAMLIT_HOST = "localhost"

# File Upload Settings
UPLOAD_FOLDER = 'uploads'
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {'txt'}

# Analysis Settings
EMOJI_LIMIT = 10
WORD_FREQUENCY_LIMIT = 20
TOP_USERS_LIMIT = 10

# Sentiment Analysis
POSITIVE_THRESHOLD = 0.1
NEGATIVE_THRESHOLD = -0.1

# Visualization Settings
PLOT_STYLE = "default"
COLOR_PALETTE = "viridis"

# Common Words to Filter
COMMON_WORDS = {
    'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
    'of', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had',
    'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might',
    'i', 'you', 'he', 'she', 'it', 'we', 'they', 'what', 'which', 'who', 'when',
    'where', 'why', 'how', 'all', 'each', 'every', 'both', 'few', 'more', 'most',
    'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so',
    'than', 'too', 'very', 'just', 'that', 'this', 'as', 'if', 'me', 'him', 'her',
    'also', 'well', 'then', 'now', 'still', 'my', 'your', 'our', 'their', 'its'
}

# Feature Flags
ENABLE_SENTIMENT_ANALYSIS = True
ENABLE_WORD_CLOUD = True
ENABLE_EMOJI_ANALYSIS = True
ENABLE_RESPONSE_TIME = True
ENABLE_COMPARISONS = True
