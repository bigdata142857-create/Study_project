import os

def load_document(document_folder):

    documents = {}

    for file_name in os.listdir(document_folder):

        if file_name.endswith(".txt"):

            file_path = os.path.join(document_folder, file_name)

            with open(file_path, "r", encoding="utf-8") as f:

                documents[file_name] = f.read()

    return documents