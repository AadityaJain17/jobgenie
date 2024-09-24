import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

st.subheader("Job Listings")
st.write("Explore various job listings from Linkedin...")

keyword = st.text_input("Enter job title or keyword:", key='keyword')
location = st.text_input("Enter job location:", key='location')

def scrape_linkedin_jobs(keyword, location):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    url = f"https://www.linkedin.com/jobs/search?keywords={keyword}&location={location}&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        jobs = []

        for job_card in soup.find_all('div', class_='base-card'):
            title = job_card.find('h3', class_='base-search-card__title').text.strip()
            company = job_card.find('h4', class_='base-search-card__subtitle').text.strip()
            location = job_card.find('span', class_='job-search-card__location').text.strip()
            link = job_card.find('a', class_='base-card__full-link')['href']
            jobs.append({
                'title': title,
                'company': company,
                'location': location,
                'link': link
            })
        return jobs
    else:
        return []

if st.button("Search Jobs"):
    if keyword and location:
        st.write(f"Searching jobs for '{keyword}' in '{location}'...")
        jobs = scrape_linkedin_jobs(keyword, location)
        if jobs:
            st.session_state['jobs'] = jobs
        else:
            st.write("No LinkedIn jobs found.")
    else:
        st.write("Please enter both job title and location.")

if 'jobs' in st.session_state:
    jobs = st.session_state['jobs']

    st.write(f"**LinkedIn Jobs ({len(jobs)})**:")
    for job in jobs:
        st.markdown(f"**[{job['title']}]({job['link']})** at {job['company']} ({job['location']})")

    df = pd.DataFrame(jobs)

    csv = df.to_csv(index=False)
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name='linkedin_jobs.csv',
        mime='text/csv'
    )
