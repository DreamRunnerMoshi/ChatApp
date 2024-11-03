from file_loader import FileLoader
from bs4 import BeautifulSoup

class BeautifulSoupParser:
    def __init__(self, html_content):
        self.soup = BeautifulSoup(html_content, 'html.parser')

    def extract_header_and_body_texts(self):
        """
        Extract the text from an HTML document.
        """
        text = self.soup.get_text()
        return text

# Example usage:
loader = FileLoader(root_directory='raw_files')
html_files = loader.load_files()

# Read content from an HTML file
for file_path in html_files:
    print ("Processing file: ", file_path)
    content = loader.read_html_file(file_path)
    print ("Content : \n", content)
