from difflib import SequenceMatcher

from fastapi import APIRouter, HTTPException, status

from .filter import filter_7

from .database import audit_view_csv, component_compare_csv

from . import schemas

router = APIRouter(
    prefix="/User-Based",
    tags=['User_Collaborative_Filter']
)    


@router.post("/recommendation by User's Data (component_campare_Table)")
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
    
    # filter a table with user input project_name and system_name.
    select_by_project = component_compare_csv[component_compare_csv['mainproject'] == project_name]
    if not select_by_project.any().any():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Project_id : {project_name} is not available")
        
    
    select_by_systemname = select_by_project[select_by_project['systemname'] == system_name]
    if not select_by_systemname.any().any():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"System_name_key : {system_name} is not available")
        
    # Droping the duplicate values. if it is in same email id
    droping =select_by_systemname.drop_duplicates(subset = ['email','projectname','systemname', 'componentname'])

    # Group the DataFrame to find the repeated count 
    grouped = droping.groupby(['email','projectname','systemname', 'componentname']).size().reset_index(name='counts')
    
    # giving the similare score and find the similar one

    from difflib import SequenceMatcher
    similarity_scores = []
    column = grouped['componentname']

    for element in column:
        similarity = SequenceMatcher(None, component_name, element).ratio()
        similarity_scores.append(similarity)

    sim = grouped.assign(similarity_scores = similarity_scores)
    sim

    # align the similarity_score in descending order
    sim.sort_values(by='similarity_scores', ascending=False, inplace=True)
    max_repeated_values = sim.head(10)

    list_1 = []
    for j in range(len(max_repeated_values)):
            projectname = max_repeated_values.iloc[j]['projectname']
            systemname = max_repeated_values.iloc[j]['systemname']
            componentname = max_repeated_values.iloc[j]['componentname']
            dic = {"projectname":projectname,"systemname":systemname,"componentname":componentname}
            list_1.append(dic)
    result = list_1
    return {"result": result}



@router.post("/recommendation by User's Data (audit_view_Table)")
# getting the product name from the user
def recommend(request: schemas.Audit_Details):
    
    try:
        # selecting all user data in a table using input project name.
        select_by_project = audit_view_csv[(audit_view_csv['mainproject'] == request.project_id) & (audit_view_csv['mainpackagename'] == request.packagename) & (audit_view_csv['maincomponentname'] == request.componentname)]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"There is relevent project for given input")
        
    droping = select_by_project.drop_duplicates(subset = ['maincomponentname','suggestedproject','packagename', 'componentname'])    
    
    # Group the DataFrame to find the repeated count
    grouped = droping.groupby(['suggestedproject','packagename', 'componentname']).size().reset_index(name='counts')

    max = grouped['counts'].max()
    print(f' Maximun repeated project count is {max}')
    
    if max == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"There is no similar projects avilable for given input")
    elif max == 1:
        matching_rows = grouped.head(10)
    else:
        grouped.sort_values(by='counts', ascending=False, inplace=True)
        matching_rows = grouped.head(10)
    
    list_1 =[]
    for index, row in matching_rows.iterrows():   
            projectid = row['suggestedproject']
            packagename = row['packagename']
            componentname = row['componentname']
            users_recommendation = {'projectid': projectid, 'packagename': packagename, 'componentname': componentname }
            list_1.append(users_recommendation)
    return list_1
    













