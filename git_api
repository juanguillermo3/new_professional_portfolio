import os
import re
import ast
import requests
import requests
from requests.auth import HTTPBasicAuth
import requests
from requests.auth import HTTPBasicAuth

REPO_OWNER= os.getenv("REPO_OWNER", "juanguillermo3")
REPOS_IN_PORTFOLIO= ["lab_market_trends"]

def get_repo_metadata(repo_owner, repo_name):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}"
    response = requests.get(url)
    if response.status_code == 200:
        repo_data = response.json()
        title = repo_data.get('name')
        description = repo_data.get('description')
        image_url = f"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/main/project_image.png"  # Adjust path accordingly
        return title, description, image_url
    else:
        return None, None, None
    

def get_repo_script_metadata(repo_owner, repo_name, username=None, token=None):
    # GitHub API endpoint to list the contents of the repo
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents"
    
    # Use authentication if provided (for private repos)
    if username and token:
        auth = HTTPBasicAuth(username, token)
        response = requests.get(url, auth=auth)
    else:
        response = requests.get(url)  # No auth needed for public repos
    
    if response.status_code == 200:
        files_metadata = []
        repo_data = response.json()
        
        # Loop through each file in the repo's contents
        for file in repo_data:
            file_info = {
                'name': file.get('name'),  # File name
                'path': file.get('path'),  # File path (in the repo)
                'size': file.get('size'),  # File size in bytes
                'type': file.get('type'),  # Type (file or dir)
                'download_url': file.get('download_url'),  # URL to download the file
                'last_modified': file.get('git').get('committed_date') if file.get('git') else None  # Last commit date (if available)
            }
            files_metadata.append(file_info)
        
        return files_metadata
    else:
        return None


def fetch_python_file(repo_owner, repo_name, file_path, username=None, token=None):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"
    headers = {"Accept": "application/vnd.github.v3.raw"}
    if username and token:
        response = requests.get(url, headers=headers, auth=HTTPBasicAuth(username, token))
    else:
        response = requests.get(url, headers=headers)  # No auth for public repos
    return response.text if response.status_code == 200 else None


# Function to parse the module-level docstring and extract key-value pairs
def parse_module_docstring(docstring):
    # Define a regular expression to match key-value pairs
    metadata_pattern = r"(?P<key>\w+):\s*(?P<value>.+)"

    # Find all key-value pairs in the docstring
    metadata = {}
    matches = re.findall(metadata_pattern, docstring)
    for key, value in matches:
        metadata[key.strip()] = value.strip()

    return metadata

# Extract module-level docstring from code and parse it
def get_module_metadata(repo_owner, repo_name, file_path, username=None, token=None):
    # Fetch the Python file content
    code = fetch_python_file(repo_owner, repo_name, file_path, username, token)
    if code:
        # Parse the module-level docstring using AST
        tree = ast.parse(code)
        module_docstring = ast.get_docstring(tree)  # Get the module-level docstring
        
        if module_docstring:
            # Extract key-value pairs from the docstring
            metadata = parse_module_docstring(module_docstring)
            return metadata
        else:
            return None
    else:
        return None

def fetch_metadata_from_github_modules():
   return [
      _ for _ in 
   [_ for _ in 
   [get_module_metadata(REPO_OWNER, "lab_market_trends", _ ) for _ in 
   [_["path"] for _ in get_repo_script_metadata(REPO_OWNER, "lab_market_trends") if re.search(".py$", _["path"] )]]
   if _ 
   ]
      if _['Portfolio']=="True"
   ]
   
fetch_metadata_from_github_modules()
