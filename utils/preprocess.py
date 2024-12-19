# utils/preprocess.py

import re
import nltk

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')

from nltk.corpus import stopwords

def preprocess_text(text):
    # Remove multiple spaces and newlines
    text = re.sub(r'\s+', ' ', text)
    # Optionally, further cleaning like removing special characters
    text = re.sub(r'[^\w\s]', '', text)
    # Convert to lowercase
    text = text.lower()
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    words = text.split()
    filtered_words = [word for word in words if word not in stop_words]
    preprocessed_text = ' '.join(filtered_words)
    return preprocessed_text
