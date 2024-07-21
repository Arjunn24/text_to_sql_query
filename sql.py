


from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import sqlite3

import  google.generativeai  as genai

## configure genai key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

##Function to load google gemini model and provide queries as response
def get_gemini_response(question,prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([prompt[0],question])
    return response.text

##function to retrieve query from the database

def read_sql_query(sql,db):
    conn=sqlite3.connect(db)
    cur=conn.cursor()
    cur.execute(sql)
    rows=cur.fetchall()
    conn.commit()
    conn.close()
    for row in rows:
        print(row)
    return rows

    ## Defining prompt
prompt=[
    """
    You are an expert in converting english questions to SQL query!
    The SQL database has the name STUDENT and has the following columns - NAME , CLASS , SECTION\n\n For example ,
    \nExample 1 - How many entries of records are present ? ,
    the SQL command would be something like this SELECT COUNT(*) FROM STUDENT;
    \nExample 2 - Tell me all the students studying in Data Science class ?,
    the SQL command will be something like this SELECT * FROM STUDENT 
    WHERE CLASS = "Data Science";
    also the sql code should not have ``` in the begining or end and sql word in output  
    """
]    

## Streamlit app
st.set_page_config(page_title="I can retrieve any SQL query")
st.header("Gemini app to Retrieve SQL data")

question=st.text_input("Input : ",key="input")

submit=st.button("Ask the question ")

##if submit is clicked
if submit:
    response=get_gemini_response(question , prompt)
    response=read_sql_query(response,"student.db")
    st.subheader("The response is :")
    for row in response:
        print(row)
        st.header(row)
    
   



    
    