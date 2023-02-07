from pydantic import BaseModel

class ProjectDetails(BaseModel):
    projectcode: str
    systemnamekey: str
    componentnamekey: str
    
class NameDetails(BaseModel):
    projectname: str
    systemname: str
    componentname: str