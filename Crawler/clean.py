import nltk
import os
import re

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

def clean_text(raw_text):
    cleaned_text = clean_punctuation(raw_text)
    return cleaned_text

def clean_punctuation(text):
    text = re.sub(r'\w+:\/\/\S+', '', text)
    text = re.sub(r'\[\d+\]', '', text)
    text = re.sub(r'[^0-9A-Za-z \t.]', '', text)
    return text

def clean_and_save_files(input_dir, output_dir):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Process each file in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith(".txt"):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)

            with open(input_path, "r", encoding="utf-8") as infile:
                raw_text = infile.read()
                cleaned_text = clean_text(raw_text)

                # Save cleaned text to a new file
                with open(output_path, "w", encoding="utf-8") as outfile:
                    outfile.write(cleaned_text)

                print(f"Manually cleaned and saved: {output_path}")

input_dir = "pages"
output_dir = "cleaned_pages"
clean_and_save_files(input_dir, output_dir)
