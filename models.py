
from pydantic import BaseModel, Field

from typing import List

class ImportantFilesOutput(BaseModel):
    important_files: List[str] = Field(description="A list of important files)")


# With description
class IsUssueOutput(BaseModel):
    is_issue: bool = Field(description="Indicates whether the content is an issue or not.")
    issue_description:str | None= Field(description="A brief description of the issue if it is an issue, otherwise an empty string.")
