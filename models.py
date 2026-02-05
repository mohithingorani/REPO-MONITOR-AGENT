
from operator import add
from pydantic import BaseModel, Field
from langchain.messages import AnyMessage
from typing import Annotated, List

class ImportantFilesOutput(BaseModel):
    """Get important files"""
    important_files: List[str] = Field(description="A list of important files)")


# With description
class IsUssueOutput(BaseModel):
    is_issue: bool = Field(description="Indicates whether the content is an issue or not.")
    issue_description:str | None= Field(description="A brief description of the issue if it is an issue, otherwise an empty string.")

class FileState(BaseModel):
    file_path : str

class MessageState(BaseModel):
    messages : Annotated[list[AnyMessage],add]
    llm_calls : int = 0
    files: list[str] = []
    owner:str =""
    repo : str | None = None
    path:str = ""