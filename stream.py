import streamlit as st
import pandas as pd
import numpy as np
from utils import model_predict
from mails import getEmails
st.set_page_config(layout="wide")
st.title('Spam CLassification')

color = st.slider('Select Number of Mails to scan',)
if st.button('Start Fetching'):
    with st.spinner('Fetching Emails...'):
        mails,preds,source,subjects=getEmails(color)
        st.success('Emails Fetched')
        df=pd.DataFrame({
            'Content':mails,
            'Spam':preds, 
            'Sender':source,
            'Subject':subjects,
        })
        st.data_editor(df,use_container_width=True)



