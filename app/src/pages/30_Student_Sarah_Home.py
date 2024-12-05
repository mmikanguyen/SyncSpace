
import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title(f"Welcome Student, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

# View Student List Button
if st.button('View Student List', type='primary', use_container_width=True):
    st.switch_page('pages/30_2_View_Student_List.py')

# Manage Student Profile Button
if st.button('Manage Student Profile', type='primary', use_container_width=True):
    st.switch_page('pages/30_1_Manage_Student_Profile.py')

if st.button('View Professional Events', type='primary', use_container_width=True):
    st.switch_page('pages/30_4_View_Events.py')

if st.button('Feedback', type='primary', use_container_width=True):
    st.switch_page('pages/30_5_Submit_Feedback.py')




