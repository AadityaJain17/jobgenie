import streamlit as st
from pathlib import Path
import importlib.util

# Set page configuration
st.set_page_config(
    page_title="JobGenie",
    page_icon="🧞‍♂️",
)

st.title("JobGenie")
# Define the tabs
tabs = st.tabs(["Home", "ATS Checker", "Technical Interview Prep","Behavioral Questions","Job Search"])

# Function to dynamically load and run the selected page
def load_page(page_name):
    page_path = Path(f"{page_name}.py")
    if page_path.is_file():
        spec = importlib.util.spec_from_file_location(page_name, str(page_path))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    else:
        st.error(f"Page {page_name} not found!")

# Load content for each tab
with tabs[0]:
    load_page("home")
with tabs[1]:
    load_page("ats")  
with tabs[2]:
    load_page("int")  
with tabs[3]:
    load_page("behave")  
with tabs[4]:
    load_page("job")