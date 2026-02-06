import requests
import os
from dotenv import load_dotenv
load_dotenv()




from langchain_core.tools import tool
GITHUB_API = "https://api.github.com"
HEADERS = {
    "Authorization": f"Bearer {os.getenv('GITHUB_TOKEN')}",
    "Accept": "application/vnd.github+json"
}
from langchain.messages import ToolMessage




import requests
from typing import List

GITHUB_API = "https://api.github.com"

# def fetch_repo_files(
#     owner: str,
#     repo: str,
#     path: str,
#     headers: dict
# ) -> List[str]:
#     url = f"{GITHUB_API}/repos/{owner}/{repo}/contents/{path}"
#     response = requests.get(url, headers=headers)
#     response.raise_for_status()

#     items = response.json()
#     files = []

#     for item in items:
#         if item["type"] == "file":
#             files.append(item["path"])
#         elif item["type"] == "dir":
#             files.extend(
#                 fetch_repo_files(owner, repo, item["path"], headers)
#             )

#     return files






@tool
def get_file_content(owner: str, repo: str, file_path: str) -> str:
    """
    Docstring for get_file_content
    
    :param owner: Description
    :type owner: str
    :param repo: Description
    :type repo: str
    :param file_path: Description
    :type file_path: str
    :return: Description
    :rtype: str
    """
    url = f"{GITHUB_API}/repos/{owner}/{repo}/contents/{file_path}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    file_info = response.json()
    if 'content' in file_info:
        import base64
        content = base64.b64decode(file_info['content']).decode('utf-8')
        return content
    return ""









