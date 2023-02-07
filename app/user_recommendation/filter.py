import pandas as pd
import time
import schedule
import threading

from .database import componentcompares_df, projects_df, languagetexts_df, users_df




def component_compare():
    
    filter_1 = componentcompares_df[['userid', 'projectcode', 'projectid', 'systemnamekey', 'componentnamekey', 'creationtime']]
    
    # Merging the filter_1 and raw_data_2 to get the project name.
    filter_2 = pd.merge(filter_1, projects_df[["projectcode", "projectname"]], left_on='projectcode', right_on='projectcode',
                        how='inner')

    # Eliminate duplicate datas from filter_2.
    filter_2 = filter_2.drop_duplicates(subset = ['projectname','componentnamekey','systemnamekey'])
    filter_2 = filter_2[filter_2.duplicated(subset='userid', keep=False)]

    # giving the value to systemnamekey.
    filter_3 = pd.merge(filter_2, languagetexts_df, left_on='systemnamekey', right_on='key', how='inner')
    filter_3 = filter_3.rename(columns={'value': 'systemname'})
    filter_3 = filter_3.drop(columns=["key"])

    # giving the value to componentnamekey.
    filter_4 = pd.merge(filter_3, languagetexts_df, left_on='componentnamekey', right_on='key', how='inner')
    filter_4 = filter_4.rename(columns={'value': 'componentname'})
    filter_4 = filter_4.drop(columns=["key"])

    # drop the row, if the projectname doesn't contains more than one unique values.
    drop_email = []
    # Iterate over each unique user_id value
    for userid in filter_4["userid"].unique():
        # Get all rows with the current
        user_rows = filter_4[filter_4["userid"] == userid]
        # Check if the column "projectname" has more than one unique value
        if len(user_rows["projectname"].unique()) <= 1:
            # If it has only one unique value, add the user_id to the list to drop
            drop_email.append(userid)

    # Drop the rows with the user_id in the list
    filter_5 = filter_4[~filter_4["userid"].isin(drop_email)]

    # deleting the row if the systemnamekey contains the value as Com_00000001(overview).
    filter_6 = filter_5.query('systemnamekey != "Com_00000001"')

    # importing user table for getting the user's email_id.
    filter_7 = pd.merge(filter_6, users_df, left_on='userid', right_on='id', how='inner')

    # selecting the rquired columns for comparing.
    result = filter_7[['email', 'creationtime', 'projectname', 'systemname', 'componentname']]
    result.head()

    # Separating the email to find total users.
    email_sep = result["email"].unique()
    df = pd.DataFrame(email_sep)
    list1 = []
    # Giving an email one by one to process the data.
    for u in range(len(df)):
        email = df.iloc[u][0]
        user_data = result[result['email'] == email]
        # print(f'Processing email ID is {email}')
        user_data = user_data.reset_index().rename(columns={user_data.index.name: 'bar'})
        for i in range(len(user_data)):
            mainproject = user_data.iloc[i]['projectname']
            for j in range(0, len(user_data)):
                if i != j:
                    if i > j:
                        if user_data.iloc[i]['systemname'] == user_data.iloc[j]['systemname']:
                            creationtime = user_data.iloc[j]['creationtime']
                            projectname = user_data.iloc[j]['projectname']
                            systemname = user_data.iloc[j]['systemname']
                            componentname = user_data.iloc[j]['componentname']
                            dic = {"email": email, "mainproject": mainproject, "creationtime": creationtime,
                                "projectname": projectname, "systemname": systemname, "componentname": componentname}
                            list1.append(dic)

                    elif i < j:
                        if user_data.iloc[i]['systemname'] == user_data.iloc[j]['systemname']:
                            creationtime = user_data.iloc[j]['creationtime']
                            projectname = user_data.iloc[j]['projectname']
                            systemname = user_data.iloc[j]['systemname']
                            componentname = user_data.iloc[j]['componentname']
                            dic = {"email": email, "mainproject": mainproject, "creationtime": creationtime,
                                "projectname": projectname, "systemname": systemname, "componentname": componentname}
                            list1.append(dic)
    value  = filter_7
    result = list1
    final_df = pd.DataFrame(result)
    print(final_df.head())
    return result, value

result1 = component_compare()
result, value = result1
filter_7 = value
result = result
final_df = pd.DataFrame(result)

schedule.every(10).minutes.do(component_compare)

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)
    
thread = threading.Thread(target=run_schedule)
thread.start()


