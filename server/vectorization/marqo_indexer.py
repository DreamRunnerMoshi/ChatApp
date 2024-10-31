import marqo
from langchain_community.document_loaders import UnstructuredHTMLLoader
import os
from file_loader import FileLoader
import pprint

# Initialize Marqo client
mq = marqo.Client(url='http://localhost:8882')
index_name = 'alchemist_vectorized'

#mq.delete_index(index_name)
# Create the index with tensor_fields explicitly provided
#mq.create_index(index_name, tensor_fields=["Description"])

# Initialize FileLoader and load all HTML files
loader = FileLoader(root_directory='raw_files')
html_files = loader.load_files()

# List to hold documents to be indexed
documents = []
print("Total HTML files:", len(html_files))

# Read content from each HTML file and prepare documents for indexing
for file_path in html_files:
    content = loader.read_html_file(file_path)
    documents.append({
        "Title": os.path.basename(file_path),
        "Description": content
    })

# Add documents to Marqo index
i = 1
for document in documents:
    print ("Indexing : ", i)
    i = i + 1
    try:
        mq.index(index_name).add_documents([document], tensor_fields=["Description"])
    except Exception as e: 
        print(e)

# Perform a search query
results = mq.index(index_name).search(q="discussion with sadid")
pprint.pprint(results)