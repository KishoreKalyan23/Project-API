from sqlalchemy import create_engine,text
import pandas as pd


# Database connection.

engine = create_engine('postgresql+psycopg2://admin:admin1234@postgres.telecomatics.com:5432/icebergprodnov')

conn = engine.connect()

engine_uam = create_engine('postgresql+psycopg2://admin:admin1234@postgres.telecomatics.com:5432/icebergproduam')

conn_uam = engine_uam.connect()


# Inserting a tables from database.

componentcompares = conn.execute(text("SELECT * FROM public.componentcompares")).fetchall()

projects = conn.execute(text("select * from public.projects")).fetchall()

languagetexts = conn.execute(text("SELECT key,value FROM public.languagetexts where code = 'en'")).fetchall()

users = conn.execute(text("SELECT id,email FROM public.users")).fetchall()

audit_view = conn_uam.execute(text("select * from public.audit_view where event_type = 'Get Tab Groups'")).fetchall()


# convert table to dataframe

componentcompares_df = pd.DataFrame(componentcompares)

projects_df = pd.DataFrame(projects)

languagetexts_df = pd.DataFrame(languagetexts)

users_df = pd.DataFrame(users)

audit_view_df = pd.DataFrame(audit_view)


# inserting the filtered csv data.

component_compare_csv = pd.read_csv('./app/user_recommendation/Data/component_compare_final_data.csv')

audit_view_csv = pd.read_csv("./app/user_recommendation/Data/audit_view_final_data.csv")

