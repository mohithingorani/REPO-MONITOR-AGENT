from pydantic import BaseModel,Field
from typing_extensions import List,Annotated
from langchain.messages import AnyMessage
from operator import add
from typing_extensions import Literal
class ImportantFilesOutput(BaseModel):
    """Get important files"""
    important_files: List[str] = Field(description="A list of important files)")


# With description
class isIssue(BaseModel):
    is_issue: bool = Field(description="Indicates whether the content is an issue or not.")
    issue_description:str | None= Field(description="A brief description of the issue if it is an issue, otherwise an empty string.")
    severity:Literal["Critical","High","Medium","Low"] | None

class LLMWithTools(BaseModel):
    messages: Annotated[list[AnyMessage], add]
    curr_index: int = 0
