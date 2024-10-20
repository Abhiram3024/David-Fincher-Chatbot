import os

def combine_cleaned_files(input_dir, output_file):
    # Create a list to store the cleaned text from each file
    cleaned_texts = []

    # Process each file in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith(".txt"):
            file_path = os.path.join(input_dir, filename)

            with open(file_path, "r", encoding="utf-8") as infile:
                cleaned_text = infile.read()
                cleaned_texts.append(cleaned_text)

    # Combine all cleaned texts into one string
    combined_text = "\n".join(cleaned_texts)

    # Save the combined text to the output file
    with open(output_file, "w", encoding="utf-8") as outfile:
        outfile.write(combined_text)

    print(f"Combined and saved all cleaned files to: {output_file}")

input_dir = "cleaned_pages"
output_file = "combined_cleaned_file.txt"
combine_cleaned_files(input_dir, output_file)
