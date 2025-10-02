import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv

from src.mcqgenerator.utils import read_file, get_table_data # this
from src.mcqgenerator.logger import logging
from src.mcqgenerator.MCQgenerator import generate_evaluate_chain

import streamlit as st

#  pip install langchain-community langchain-openai
from langchain_community.callbacks.manager import get_openai_callback

# loading json file
# with open('D:\SACHI\GEN-AI\mcq-generator\Response.json','r') as file:
#    RESPONSE_JSON = json.load(file)
import os

file_path = os.path.join(os.path.dirname(__file__), "Response.json")
with open(file_path, "r") as file:
    data = file.read()

   
# creating a title for the app
st.title("MCQ Generator App with Langchain")

# Cute disclaimer
st.info("⚠️ Heads up! Currently, the OpenAI API integration is **disabled** in the Live deployment to avoid high costs 💰, but you can see the demo screenshots and working flow in the README. 🚀✨")


# create a form
with st.form("user inputs"):
   #upload file
   uploaded_file = st.file_uploader("Upload a pdf or txt file")
   #input fields
   mcq_count  = st.number_input("Number of MCQs", min_value=3, max_value=20)
   #subject
   subject=st.text_input("Insert subject", max_chars=50)
   #quiz tone
   tone=st.text_input("Complexity Level of Questions", max_chars=20, placeholder="simple")
   #add button
   button=st.form_submit_button("Create MCQs")
   
   if button and uploaded_file is not None and mcq_count and subject and tone : 
      with st.spinner("generating..."):
         try:
            text=read_file(uploaded_file)
              # Run MCQ generation with token usage tracking
            with get_openai_callback() as cb:
               response = generate_evaluate_chain(
                  {
                     "text":text,
                     "number":mcq_count,
                     "subject":subject,
                     "tone":tone,
                     "response_json":json.dumps(RESPONSE_JSON)
                  }
               )
         except Exception as e:
            # Print traceback and show error in UI
            traceback.print_exception(type(e), e, e.__traceback__)
            st.error("Error")
         else:
            print(f"Total Tokens:{cb.total_tokens}")
            print(f"Prompt Tokens:{cb.prompt_tokens}")
            print(f"Completion Tokens:{cb.completion_tokens}")
            print(f"Total Cost:{cb.total_cost}")
            
            # Process and display quiz if valid
            if isinstance(response, dict):
               quiz=response.get("quiz",None)
               if quiz is not None:
                  table_data=get_table_data(quiz)
                  if table_data is not None:
                     df=pd.DataFrame(table_data)
                     df.index=df.index+1 # Start index at 1
                     st.table(df)
                     st.text_area(label="Review", value=response["review"])
                  else:
                     st.error("Error in the table data")
            else:
               st.write(response)
               
# Run with :
#     streamlit run StreamlitApp.py

