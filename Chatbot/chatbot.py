import pickle
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import random
import os
import spacy
from spacy.lang.en import English 

nlp = spacy.load("en_core_web_sm")

# File to store user data
user_data_file = 'user1_data.pkl'

# Load existing user data if available
if os.path.exists(user_data_file):
    with open(user_data_file, 'rb') as file:
        user_data = pickle.load(file)
else:
    user_data = {}

# Load the pickled knowledge base
with open('knowledge_base.pkl', 'rb') as file:
    knowledge_base = pickle.load(file)

# Preprocess the text
def preprocess_text(text):
    text = re.sub(r'\W', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.lower()

# Calculating cosine similarity
def calculate_cosine_similarity(user_input, known_sentences):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([user_input] + known_sentences)
    similarity_matrix = cosine_similarity(vectors)
    return similarity_matrix[0, 1:]

#Saving user data
def save_user_data(name, likes_dislikes, liked_movie=None):
    if name in user_data:
        user_data[name]['likes_fincher'] = likes_dislikes
        if liked_movie:
            user_data[name]['liked_movie'] = liked_movie
    else:
        user_data[name] = {'likes_fincher': likes_dislikes, 'liked_movie': liked_movie}
    
    with open(user_data_file, 'wb') as file:
        pickle.dump(user_data, file)

    
# Function to get user preference
def get_user_preferences(user_name):
    if user_name in user_data:
        return user_data[user_name]['likes_fincher']
    else:
        preference = input("Fin: Do you like David Fincher? Type 'yes' if you do, or 'no' if you do not like him or don't know much about him: ")
        if preference.lower() not in ['yes', 'no']:
            print("Fin: Invalid response. Assuming 'no'.")
            return 'no'
        return preference.lower()

def chatbot(user_input, user_name, user_likes_dislikes):
    user_input = preprocess_text(user_input)
    doc = nlp(user_input)

    # Extract named entities
    entities = [(ent.text, ent.label_) for ent in doc.ents]  
    entities = [ent.text for ent in doc.ents]
    
    # Append entity texts to user input
    entity_text = " ".join(entities)
    user_input += " " + entity_text

    best_match_key = None
    best_match_score = 0

    for key, sentences in knowledge_base.items():
        sentences = [preprocess_text(sentence) for sentence in sentences]
        similarity_scores = calculate_cosine_similarity(user_input, sentences)
        avg_similarity = np.mean(similarity_scores)

        if avg_similarity > best_match_score:
            best_match_key = key
            best_match_score = avg_similarity

    if best_match_key is not None:
        matched_responses = knowledge_base[best_match_key]
        selected_response = random.choice(matched_responses)
        return selected_response
    else:
        return "Sorry, I don't have information on that."

# Startingconversation
print("Fin: Hello! I'm Fin, a David Fincher fan chatbot.")

# Asking user's name
user_name = input("Fin: What's your name? ")

# Get user preference
user_preference = get_user_preferences(user_name)

# Customize opening prompt based on user's preference and whether they are a new user
if user_name in user_data and 'likes_fincher' in user_data[user_name]:
    if user_preference == 'yes':
        print(f"Fin: Hello {user_name}! Welcome back. I remember you like David Fincher.")
        if 'liked_movie' in user_data[user_name]:
            liked_movie = user_data[user_name]['liked_movie']
            print(f"Fin: By the way, you mentioned that you like '{liked_movie}'.")
            print("Fin: Please name another Fincher movie you like.")
            # Get the user's liked movie
            liked_movie = input(f"{user_name}: ")
            if liked_movie == 'Alien 3':
                print(f"Fin: Well, that's a controversial choice!")
            else:
                print(f"Fin: That's great! {liked_movie} is indeed a fantastic film.")
                save_user_data(user_name, user_preference, liked_movie)
    else:
        print(f"Fin: Hello {user_name}! Welcome back. I remember you do not like David Fincher or know much about him.")
        save_user_data(user_name, user_preference)
else:
    if user_preference == 'yes':
        print(f"Fin: Hello {user_name}! Nice to meet you. I see you like David Fincher.")
        if 'liked_movie' not in user_data.get(user_name, {}):
            print("Fin: Please name a Fincher movie you like.")
            # Get the user's liked movie
            liked_movie = input(f"{user_name}: ")
            if liked_movie == 'Alien 3':
                print(f"Fin: Well, that's a controversial choice!")
            else:
                print(f"Fin: That's great! {liked_movie} is indeed a fantastic film.")
                save_user_data(user_name, user_preference, liked_movie)
    else:
        print(f"Fin: Hello {user_name}! Nice to meet you. I see you do not like David Fincher or know much about him.")
        print("Fin: Have you watched any Fincher movies before? Type 'yes' or 'no'")
        # Get the user's response
        watched_fincher = input(f"{user_name}: ").lower()
        
        if watched_fincher == 'yes':
            # User has watched Fincher movies before
            print("Fin: That's good to know.")
            
            # Ask which Fincher movie they watched
            watched_movie = input("Fin: Which Fincher movie did you like the most? Please provide the name: ")
            if watched_movie != 'Alien 3':
                print(f"Fin: Nice! {watched_movie} is a great choice.")
                save_user_data(user_name, user_preference, watched_movie)
            else:
                print(f"Fin: Well, that's a controversial choice!")
        elif watched_fincher == 'no':
            # User hasn't watched Fincher movies
            print("Fin: Well, if you're interested, here are some popular David Fincher movies: Fight Club, The Social Network, Gone Girl, Seven, The Girl with the Dragon Tattoo, The Killer, Alien 3, Zodiac.")
            save_user_data(user_name, user_preference)
        else:
            print("Fin: Invalid response. Assuming 'no'.")
            print("Fin: Well, if you're interested, here are some popular David Fincher movies: Fight Club, The Social Network, Gone Girl, Seven, The Girl with the Dragon Tattoo, The Killer, Alien 3, Zodiac.")
            save_user_data(user_name, user_preference)
# Continue the conversation
print(f"Fin: Fincher has won many awards, made several book adaptations, including one about Facebook, ventured into his own production company 'Propaganda', has made music videos before entering filmmaking, and has a longtime collaboration with composer Trent Reznor from the Nine Inch Nails. ")
print(f"Fin: Ask me more about the above topics or just Fincher in general or type 'exit' to end the conversation.")
while True:
    user_input = input(f"{user_name}: ")

    if user_input.lower() == 'exit':
        print("Fin: Goodbye! Have a great day.")
        break

    response = chatbot(user_input, user_name, user_preference)
    print("Fin:", response)
