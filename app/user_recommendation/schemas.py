from pydantic import BaseModel

class ProjectDetails(BaseModel):
    projectcode: str
    systemnamekey: str
    componentnamekey: str