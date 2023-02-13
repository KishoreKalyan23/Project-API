from pydantic import BaseModel

class ProjectDetails(BaseModel):
    projectcode: str
    systemnamekey: str
    componentnamekey: str
    
class NameDetails(BaseModel):
    projectname: str
    systemname: str
    componentname: str
    
class Audit_Details(BaseModel):
    project_id: int
    packagename: str
    componentname: str