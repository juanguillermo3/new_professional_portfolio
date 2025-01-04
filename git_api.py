import os
import re
import ast
import logging
import requests
from requests.auth import HTTPBasicAuth

try:
    from dotenv import load_dotenv
except ImportError:
    os.system("pip install python-dotenv")
    from dotenv import load_dotenv

#
from dotenv import load_dotenv
load_dotenv()
#
ENVIRONMENT = os.getenv("ENVIRONMENT")
REPO_OWNER= os.getenv("REPO_OWNER")
REPOS_IN_PORTFOLIO=os.getenv("REPOS_IN_PORTFOLIO").split(",") 
#
ENVIRONMENT
REPO_OWNER
REPOS_IN_PORTFOLIO

#
# 0.
#
def get_repo_metadata(repo_owner, repo_name, username=None, token=None):
    """
    Retrieve metadata for a GitHub repository, including title, description, and an image URL.

    Args:
        repo_owner (str): Owner of the GitHub repository.
        repo_name (str): Name of the GitHub repository.
        username (str, optional): GitHub username for authentication.
        token (str, optional): GitHub token for authentication.

    Returns:
        tuple: A tuple containing the repository's title, description, and image URL. 
               Returns (None, None, None) if the request fails.
    """
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}"
    
    # Use authentication if provided
    if username and token:
        auth = HTTPBasicAuth(username, token)
        response = requests.get(url, auth=auth)
    else:
        response = requests.get(url)  # No auth needed for public repos
    
    if response.status_code == 200:
        repo_data = response.json()
        title = repo_data.get('name')
        description = repo_data.get('description')
        image_url = f"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/main/project_image.png"  # Adjust path if necessary
        return title, description, image_url
    else:
        return None, None, None

#
#[get_repo_metadata(REPO_OWNER,some_repo) for some_repo in REPOS_IN_PORTFOLIO]

#
# 1.
#
def list_repo_files(repo_owner, repo_name, username=None, token=None, file_pattern=r".*\.(py|R)$"):
    """
    Lists all files in a GitHub repository, optionally filtering by file type using a regex.

    Args:
        repo_owner (str): Owner of the GitHub repository.
        repo_name (str): Name of the GitHub repository.
        username (str, optional): GitHub username for authentication.
        token (str, optional): GitHub token for authentication.
        file_pattern (str, optional): Regex pattern to filter files by type. Defaults to Python and R files.

    Returns:
        list: A list of dictionaries containing file metadata, including name, path, size, type, and download URL.
              Returns an empty list if the request fails or no files match the pattern.
    """
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents"
    files_metadata = []

    # Use authentication if provided
    if username and token:
        auth = HTTPBasicAuth(username, token)
        response = requests.get(url, auth=auth)
    else:
        response = requests.get(url)  # No auth needed for public repos

    if response.status_code == 200:
        repo_data = response.json()
        pattern = re.compile(file_pattern)

        for file in repo_data:
            if file.get('type') == 'file' and pattern.match(file.get('name', '')):
                files_metadata.append({
                    'name': file.get('name'),
                    'path': file.get('path'),
                    'size': file.get('size'),
                    'type': file.get('type'),
                    'download_url': file.get('download_url')
                })
    return files_metadata

#
# 2.
#

# General file fetcher
def fetch_file_content(repo_owner, repo_name, file_path, username=None, token=None):
    """
    Fetches the content of a file from a GitHub repository.
    """
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"
    headers = {"Accept": "application/vnd.github.v3.raw"}
    if username and token:
        response = requests.get(url, headers=headers, auth=HTTPBasicAuth(username, token))
    else:
        response = requests.get(url, headers=headers)  # No auth for public repos
    return response.text if response.status_code == 200 else None

# Docstring extractor with differentiated methods for file types
def extract_docstring(file_content, file_type):
    """
    Extracts the docstring from the file content based on the file type.
    """
    if file_type == "python":
        try:
            tree = ast.parse(file_content)
            return ast.get_docstring(tree)  # Extract Python module-level docstring
        except SyntaxError:
            return None
    elif file_type == "r":
        # Assume docstring starts with "#'" for R files
        lines = file_content.splitlines()
        docstring_lines = [line[2:].strip() for line in lines if line.startswith("#'")]
        return "\n".join(docstring_lines) if docstring_lines else None
    else:
        raise ValueError(f"Unsupported file type: {file_type}")

# Function to parse the module-level docstring and extract key-value pairs
def parse_module_docstring(docstring):
    """
    Parses a docstring to extract key-value pairs using regular expressions.
    """
    metadata_pattern = r"(?P<key>\w+):\s*(?P<value>.+)"
    metadata = {}
    matches = re.findall(metadata_pattern, docstring)
    for key, value in matches:
        metadata[key.strip()] = value.strip()
    return metadata

# Main entry point
def get_module_metadata(repo_owner, repo_name, file_path, file_type, username=None, token=None):
    """
    Fetches a file from GitHub, extracts its docstring, and parses metadata.
    """
    # Fetch the file content
    file_content = fetch_file_content(repo_owner, repo_name, file_path, username, token)
    if not file_content:
        return None

    # Extract the docstring based on the file type
    docstring = extract_docstring(file_content, file_type)
    if not docstring:
        return None

    # Parse key-value pairs from the docstring
    return parse_module_docstring(docstring)


# Define a function to determine file type based on file extension (case-insensitive)
def get_file_type(file_path):
    file_path = file_path.lower()  # Convert file path to lowercase for case-insensitivity

    if file_path.endswith(".py"):
        return "python"
    elif file_path.endswith(".r"):
        return "r"
    # Add more file type mappings as needed
    else:
        return None  # Unsupported file type

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Extract metadata from all code files
# Extract metadata from all code files
def extract_metadata_from_all_files(all_code_files, repo_owner, username=None, token=None):
    metadata_list = []

    for file_data in all_code_files:
        file_path = file_data["path"]  # Assuming 'path' contains the file path
        repo_name = file_data["repo_name"]  # Assuming 'repo_name' is part of file_data
        file_type = get_file_type(file_path)

        if file_type:
            logging.info(f"Processing file: {file_path} (Type: {file_type})")
            metadata = get_module_metadata(repo_owner, repo_name, file_path, file_type, username, token)
            if metadata:
                # Flatten: Add 'file_path' and 'repo_name' directly to the metadata
                metadata["file_path"] = file_path
                metadata["repo_name"] = repo_name

                # Convert all keys to lowercase for standardization
                metadata = {key.lower(): value for key, value in metadata.items()}

                logging.info(f"Metadata extracted successfully for file: {file_path}")
                metadata_list.append(metadata)
            else:
                logging.warning(f"No metadata found in file: {file_path}")
        else:
            logging.warning(f"Unsupported file type for file: {file_path}")

    return metadata_list

#
# main pipeline
#
all_code_files=[]
for some_repo in REPOS_IN_PORTFOLIO:
    for file_data in list_repo_files(REPO_OWNER,some_repo):
        file_data.update({"repo_name": some_repo })
        all_code_files.append(file_data)
#
all_code_files
# 
metadata_list = extract_metadata_from_all_files(
    all_code_files,
    repo_owner=REPO_OWNER,
    #username="your_username",
    #token="your_token"
)

# Print or process the extracted metadata
metadata_list
