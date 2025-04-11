import nltk
import os

# Set a specific directory for NLTK data that is guaranteed to be writable
nltk_data_path = os.path.join(os.path.expanduser('~'), 'nltk_data')
os.makedirs(nltk_data_path, exist_ok=True)
nltk.data.path.insert(0, nltk_data_path)

# Download punkt to the specified directory
nltk.download('punkt', download_dir=nltk_data_path, quiet=False)
print(f"NLTK data downloaded to {nltk_data_path}")
print(f"NLTK data paths: {nltk.data.path}")