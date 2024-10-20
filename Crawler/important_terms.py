from sklearn.feature_extraction.text import TfidfVectorizer
import string
from nltk.corpus import stopwords
import nltk

def extract_important_terms_tfidf_from_file(file_path):
    # Read cleaned text from the specified file
    with open(file_path, "r", encoding="utf-8") as infile:
        cleaned_text = infile.read()
    
    tokens = nltk.word_tokenize(cleaned_text.lower())
    tokens = [word for word in tokens if word.isalpha() and word not in string.punctuation and word not in stopwords.words('english')]
    cleaned_text = ' '.join(tokens)
    # Create TF-IDF vectorizer
    vectorizer = TfidfVectorizer()

    # Transform the cleaned text using TF-IDF
    tfidf_matrix = vectorizer.fit_transform([cleaned_text])

    # Get feature names (terms)
    feature_names = vectorizer.get_feature_names_out()

    # Get TF-IDF scores for each term
    tfidf_scores = tfidf_matrix.toarray()[0]

    # Combine terms with their TF-IDF scores into a list of tuples
    terms_with_scores = list(zip(feature_names, tfidf_scores))

    # Sort terms based on TF-IDF scores in descending order
    sorted_terms = sorted(terms_with_scores, key=lambda x: x[1], reverse=True)

    # Extract top 25-40 important terms
    top_terms = sorted_terms[:min(40, len(sorted_terms))]

    return top_terms

cleaned_text_file = "combined_cleaned_file.txt"

# Extract important terms using TF-IDF for the cleaned text file
important_terms_tfidf_file = extract_important_terms_tfidf_from_file(cleaned_text_file)

print("\nTop important terms using TF-IDF for the cleaned text file:")
for term, score in important_terms_tfidf_file:
    print(f"{term}: {score}")
