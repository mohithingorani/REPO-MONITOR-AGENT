from pydantic import BaseModel,Field
from typing_extensions import Annotated,List,Dict,Literal
from operator import add
from langchain.messages import AnyMessage


class ObservationState(BaseModel):
    file:str
    severity:str
    issue:str


class RepoMetaData(BaseModel):
    tech_stack:List[str] = Field(description="Tech stacks used")
    license:str | None
    project_maturity:Literal["Prototype",
        "Early / MVP",
        "Production-ready",
        "Mature"]
    

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
    repo_metadata:RepoMetaData | None = None

