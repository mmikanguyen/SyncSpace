import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title('Student Home Page')

if st.button('View Advisor Feedback', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/21_Advisor_Feedback.py')