from pydantic import BaseModel
from typing_extensions import Annotated
from operator import add
from langchain.messages import AnyMessage


class ObservationState(BaseModel):
    file:str
    severity:str
    issue:str


class MessageState(BaseModel):
    messages : Annotated[list[AnyMessage],add]
    observations:Annotated[list[ObservationState],add] = []
    llm_calls : int = 0
    files: list[str] = []
    owner:str =""
    repo : str | None = None
    path:str = ""
    curr_index:int = 0
    curr_observation:str = ""
    issue_called: int| None = 0
    final_observations:str| None = None