import json
import marqo
from langchain_community.document_loaders import UnstructuredHTMLLoader
import os

from openai import OpenAI
from file_loader import FileLoader
from beautiful_soup_parser import BeautifulSoupParser  # Import the parser
import pprint


import json

class DataObject:
    def __init__(self, persons, summary):
        self.persons = persons
        self.summary = summary

    def __repr__(self):
        return f"DataObject(persons={self.persons}, summary={self.summary})"
    
# Initialize Marqo client
mq = marqo.Client(url='http://localhost:8882')
index_name = 'alchemist_vectorized'

#mq.delete_index(index_name)
# Create the index with tensor_fields explicitly provided
#mq.create_index(index_name, tensor_fields=["Description"])

# Initialize FileLoader and load all HTML files
loader = FileLoader(root_directory='/Users/mdrahman/mTech/ChatApp/server/raw_files')
html_files = loader.load_files()

os.environ["OPENAI_API_KEY"] = 'sk-proj-zdiUmjsNs6PACoKSWrR2T3BlbkFJhOvMKIisyFJUdp2F13t3'

# List to hold documents to be indexed
documents = []
print("Total HTML files:", len(html_files))

# Read content from each HTML file and prepare documents for indexing
i = 0
for file_path in html_files:
    content = loader.read_html_file(file_path)
    parser = BeautifulSoupParser(content)  # Use the parser to get header and body text
    html_content = parser.extract_header_and_body_texts()

    client = OpenAI(
            organization='org-ROdsRxFwHq5KOHYVhreIGG25',
            project='proj_dyNIbzUJx56xiXHve8VY9P3A',
        )
    system_prompt = "You are an intelligent agent to summarize unstructued document.\
        This document is just text from a html content. I will provide the text, \
        you will identify and summarise as exactly this JSON format, please format before replying and don't add any explanation: \
        This is the json format I want : \
        { \"persons\": Persons mentions in this document if any in comma seperated values, \"summary\": String: SUMMARIZES IN BRIEF, DO NOT FORGET TO INCLUDE INPORTANT STUFFS}"
    
    gpt_response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages= [
                {   "role": "system", 
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": html_content
                }],
        stream=False,
    )
    content = gpt_response.choices[0].message.content
    print(content)
    data_dict = json.loads(content)

    # Create a DataObject instance
    data_object = DataObject(persons=data_dict['persons'], summary=data_dict['summary'])

    pprint.pprint(data_object.summary)
    documents.append({
        "summary": data_object.summary,
        "persons": data_object.persons
    })
    i = i+1
    if(i>4): 
        break
    
# Add documents to Marqo index
i = 1
for document in documents:
    print ("Indexing : ", i)
    i = i + 1
    try:
        mq.index(index_name).add_documents([document], tensor_fields=["persons", "summary"])
    except Exception as e: 
        print(e)

# Perform a search query
cresults = mq.index(index_name).search(q="discussion with sadid")
#pprint.pprint(results)


