import requests
import os
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain.messages import ToolMessage
import requests
from config.github import GITHUB_API,HEADERS

load_dotenv()




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









