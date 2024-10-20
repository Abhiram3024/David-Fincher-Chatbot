# David Fincher Chatbot

## About the Project

This project implements a chatbot based on David Fincher. It provides information about the acclaimed filmmaker, his works, and related topics. The chatbot is built using Natural Language Processing (NLP) techniques and a custom knowledge base created from web-crawled data.

**Project Structure**

The project is divided into two main parts:

**Part 1: Web Crawler and Knowledge Base Creation**

crawl.py: Crawls websites related to David Fincher and collects data.  
clean.py: Preprocesses the scraped data by removing URLs and non-alphanumeric characters.  
combine_files.py: Combines cleaned text files into a single file.  
important_terms.py: Extracts the 40 most important terms using TF-IDF.  
kb_create.py: Creates a knowledge base using selected important terms.

**Part 2: Chatbot Implementation**

Implements a conversational interface using the created knowledge base.
Utilizes NLP techniques for better understanding and response generation.

## Features

Web crawling and data extraction from David Fincher-related websites
Text preprocessing and cleaning
Important term extraction using TF-IDF
Knowledge base creation and storage
User model persistence (remembers user preferences)
Natural language understanding using tokenization, lemmatization, and Named Entity Recognition (NER)
Response generation using cosine similarity

## Usage

Run the web crawler and knowledge base creation scripts in Part 1.
Launch the chatbot.py script from Part 2.
Interact with the chatbot by answering initial questions and then asking about David Fincher and his works.

Dependencies  
Python 3.x  
spaCy  
NLTK  
Requests  
BeautifulSoup4  
scikit-learn  
numpy  
pickle  
re  
os  
sys  

## File Descriptions

crawl.py: Web crawler script  
clean.py: Text cleaning script  
combine_files.py: File combiner script  
important_terms.py: Important terms extraction script  
kb_create.py: Knowledge base creation script  
chatbot.py: Main chatbot script  
user1_data.pkl: Pickled file for storing user data  
kbdict.txt: Readable version of the knowledge base  
