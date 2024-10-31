from pathlib import Path
from bs4 import BeautifulSoup as BSHTMLLoader
import pprint

class FileLoader:
    def __init__(self, root_directory='raw_files'):
        self.root_directory = Path(root_directory)
        self.current_directory = Path.cwd()

    def load_files(self):
        # Use the glob method to find all HTML files recursively in raw_files folder
        html_files = self.root_directory.rglob('*.html')
        # Convert the generator to a list of absolute paths
        file_paths = [self.current_directory / file for file in html_files]
        return file_paths

    def read_html_file(self, file_path):
        # Load the file content with error handling for encoding issues
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            data = f.read()

        # Parse the HTML by creating a BeautifulSoup object
        soup = BSHTMLLoader(data, 'html.parser')
        text = soup.get_text()
        return text
    
# Example usage
if __name__ == "__main__":
    loader = FileLoader()
    html_files = loader.load_files()

    if html_files:
        for file_path in html_files:
            print(f"Processing file: {file_path}")
            text = loader.read_html_file(file_path)
            print(text)
            break
    else:
        print("No HTML files found.")