import pickle

file_path = 'user1_data.pkl'

# Read the content of the binary file using binary mode
with open(file_path, 'rb') as file:
    # Unpickle the data
    unpickled_data = pickle.load(file)

print("Unpickled Data:")
print(unpickled_data)
