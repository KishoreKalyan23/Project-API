import pandas as pd

from .filter import filter_7

from . import schemas

from fastapi import APIRouter, HTTPException, status


router = APIRouter(
    prefix="/User-Based",
    tags=['Conversion']
)    


@router.post("/key to name convertion")
# getting the product name from the user
def recommend(request: schemas.ProjectDetails):
    
    # conversion of key to name
    try:
        project_name = filter_7.at[filter_7.index[filter_7['projectcode'] == request.projectcode][0], 'projectname']
    except Exception as e:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"projectcode : '{request.projectcode}' dosen't had any key value")
        
    try:
        system_name = filter_7.at[filter_7.index[filter_7['systemnamekey'] == request.systemnamekey][0], 'systemname']
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"systemnamekey : '{request.systemnamekey}' dosen't had any key value")
        
    try:    
        component_name = filter_7.at[filter_7.index[filter_7['componentnamekey'] == request.componentnamekey][0], 'componentname']
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"componentnamekey : '{request.componentnamekey}' dosen't had any key value")
    dic_1 = {'projectname': project_name, 'systemname': system_name, 'componentname': component_name}
    
    return {'key': dic_1}

@router.post("/name to key convertion")
# getting the product name from the user
def recommend(request: schemas.NameDetails):
    
    # conversion of key to name
    try:
        project_name = filter_7.at[filter_7.index[filter_7['projectname'] == request.projectname][0], 'projectcode']
    except Exception as e:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"projectcode : '{request.projectname}' dosen't had any key value")
        
    try:
        system_name = filter_7.at[filter_7.index[filter_7['systemname'] == request.systemname][0], 'systemnamekey']
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"systemnamekey : '{request.systemnamekey}' dosen't had any key value")
        
    try:    
        component_name = filter_7.at[filter_7.index[filter_7['componentname'] == request.componentname][0], 'componentnamekey']
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"componentnamekey : '{request.componentname}' dosen't had any key value")
    dic_1 = {'projectname': project_name, 'systemname': system_name, 'componentname': component_name}
    
    return {'key': dic_1}