from googleapiclient.discovery import build 
from google_auth_oauthlib.flow import InstalledAppFlow 
from google.auth.transport.requests import Request 
import pickle 
import os.path 
import base64 
import email 
from utils import model_predict
from bs4 import BeautifulSoup 
import streamlit as st
  
# Define the SCOPES. If modifying it, delete the token.pickle file. 
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly'] 
  
def getEmails(flag): 
    all_mails=[]
    preds=[]
    source=[]
    subjects=[]
    nm=0
    st.toast('Begining to fetch your mails', icon='😍')
    # Variable creds will store the user access token. 
    # If no valid token found, we will create one. 
    creds = None
  
    # The file token.pickle contains the user access token. 
    # Check if it exists 
    if os.path.exists('token.pickle'): 
  
        # Read the token from the file and store it in the variable creds 
        with open('token.pickle', 'rb') as token: 
            creds = pickle.load(token) 
  
    # If credentials are not available or are invalid, ask the user to log in. 
    if not creds or not creds.valid: 
        if creds and creds.expired and creds.refresh_token: 
            creds.refresh(Request()) 
        else: 
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES) 
            creds = flow.run_local_server(port='https://ratanpyla.streamlit.app/') 
  
        # Save the access token in token.pickle file for the next run 
        with open('token.pickle', 'wb') as token: 
            pickle.dump(creds, token) 
  
    # Connect to the Gmail API 
    service = build('gmail', 'v1', credentials=creds) 
  
    # request a list of all the messages 
    result = service.users().messages().list(userId='me').execute() 
  
    # We can also pass maxResults to get any number of emails. Like this: 
    # result = service.users().messages().list(maxResults=200, userId='me').execute() 
    messages = result.get('messages') 
    st.toast('Fetched 100 mails')
  
    # messages is a list of dictionaries where each dictionary contains a message id. 
    # iterate through all the messages 
    st.toast('analysing your mail')
    for msg in messages: 
        # Get the message from its id 
        if nm>flag:
            break
        txt = service.users().messages().get(userId='me', id=msg['id']).execute() 
        # Use try-except to avoid any Errors 
        print('a')
        try: 
            # Get value of 'payload' from dictionary 'txt' 
            payload = txt['payload'] 
            headers = payload['headers'] 
            
            # Look for Subject and Sender Email in the headers 
            for d in headers: 
                if d['name'] == 'Subject': 
                    subject = d['value'] 
                if d['name'] == 'From': 
                    sender = d['value'] 
            
            # The Body of the message is in Encrypted format. So, we have to decode it. 
            # Get the data and decode it with base 64 decoder. 
            parts = payload.get('parts')[0] 
            data = parts['body']['data'] 
            data = data.replace("-","+").replace("_","/") 
            decoded_data = base64.b64decode(data) 
            
            
            # Now, the data obtained is in lxml. So, we will parse  
            # it with BeautifulSoup library 
            all_mails.append(str(decoded_data))
            
            preds.append(model_predict(str(decoded_data)))
            source.append(sender)
            subjects.append(subject)
            
            
            nm+=1
            print(nm)
        except: 
            print('pass')
            pass
    return all_mails,preds,source,subjects
  
  
