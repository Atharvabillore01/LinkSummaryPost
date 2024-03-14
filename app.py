import streamlit as st
from dotenv import load_dotenv
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
import facebook
import os
load_dotenv()
Open_AI_Key = os.environ["OPENAI_API_KEY"] 
FB_Access_Token = os.environ["FBToken"] #"EAAPycmxIikwBOZBIakM9wLPyKZCj0HPsU1p4DOtDn4tSw2PgZAW5tbXtfGX1XHflER73YyCuWr7G6HMAL92q7CSYDgC4d77dLst9LYpEFvVdGxifwq3I6pCu6jeKEpPqrUqFwtjlDuicXawgHT5kbAWppfTTpZBPxoEWEYZBPRDoV68GYGGinoBExfD5kjjUZD"
FB_Page_ID = os.environ["FB_Page_ID"]

st.set_page_config(page_title="URL Summirazer", page_icon=":shark:")
st.markdown("<h1 style='text-align: center;'>URL TO MEDIA_POST</h1>", unsafe_allow_html=True)
st.session_state['URL']=st.text_input("Past  URL Here ",type="default")
llm = ChatOpenAI(model_name="gpt-3.5-turbo-1106")
chain = load_summarize_chain(llm, chain_type="stuff")
summarise_button = st.button("Summarise the URL", key="summarise")
std = ""
if st.session_state['URL'] !="":
  url = st.session_state['URL']
  loader = WebBaseLoader(url)
  docs = loader.load()
  summarize_text=chain.invoke(docs)
  std = summarize_text.get("output_text")
  
send_button = st.button("Post on Facebook page",key="Post")

if summarise_button:
  summarise_placeholder = st.write(std)
if send_button:
  access_token = FB_Access_Token
  graph = facebook.GraphAPI(access_token)
  page_id = FB_Page_ID 
  post_message = std
  graph.put_object(page_id, "feed", message=post_message)

  print("Post successfully sent to Facebook.")
    