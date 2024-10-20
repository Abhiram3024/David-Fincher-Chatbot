import re
import nltk
import pickle

def clean_sentence(sentence):
    cleaned_sentence = re.sub(r'\[\d+\]', '', sentence) 
    cleaned_sentence = re.sub(r'\s*([.,;!?])\s*', r'\1 ', cleaned_sentence)
    return cleaned_sentence.strip()

important_terms = ["film","music","writer","adaptation","thriller","noir","Reznor","Alien","Propaganda","award","Zuckerberg","Sorkin"]

knowledge_base = {}
for term in important_terms:
    knowledge_base[term] = []

with open("combined_cleaned_file.txt", encoding="utf-8") as f:
    text = f.read()
    
sentences = nltk.sent_tokenize(text)

for term in important_terms:
    for sentence in sentences:
        if term in sentence:
            cleaned_sentence = clean_sentence(sentence)
            if len(cleaned_sentence.split()) < 100:
                knowledge_base[term].append(cleaned_sentence)
                
with open('knowledge_base.pkl', 'wb') as f:
    pickle.dump(knowledge_base, f)

with open('knowledge_base.pkl', 'rb') as f:
    loaded_kb = pickle.load(f)

output_file_path = 'loaded_kb.txt'
with open(output_file_path, 'w', encoding='utf-8') as f:
    for term, sentences in loaded_kb.items():
        f.write(f"{term}:\n")
        for i, sentence in enumerate(sentences, 1):
            f.write(f"{i}. {sentence}\n")
        f.write("\n")

print(f"Saved readable knowledge base to {output_file_path}")