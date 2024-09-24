import os
import streamlit as st
import google.generativeai as genai

# Set up Google Generative AI
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

# Function to start the interview
def start_interview(interview_position, interview_name):
    interview_prompt = (
        f'I want you to act as an HR interviewer. '
        f'I will be the candidate and you will ask me behavioral and situational interview questions '
        f'for the {interview_position} position. My first sentence is "Hi".'
    )

    message_list = [
        {"role": "system", "content": interview_prompt},
        {"role": "user", "content": f"I want you to only reply as the interviewer. "
                                    f"Do not write all the conversation at once. "
                                    f"Ask me behavioral or situational questions one by one like an interviewer does and wait for my answers. "
                                    f"After asking 3 questions, let me know whether I got the job or not, "
                                    f"and how well I scored out of 10. After the interview, write '=== INTERVIEW OVER ==='. "
                                    f"My name is {interview_name}. Ask me my first question about {interview_position}."}
    ]

    conversation = []
    model = genai.GenerativeModel('gemini-pro')
    chat = model.start_chat(history=[])

    interview_in_progress = True

    while interview_in_progress:
        response = chat.send_message(message_list[-1]['content'], stream=True)
        msg = ""
        for chunk in response:
            if chunk.text:
                msg += chunk.text

        conversation.append(msg)
        message_list.append({"role": "assistant", "content": msg})

        st.write(msg)

        # Check if the interview is over
        if '===' in msg or 'INTERVIEW' in msg or 'OVER' in msg:
            interview_in_progress = False
            continue
        
        input_msg = st.text_input("Your response:", key=len(conversation))
        if input_msg:
            message_list.append({"role": "user", "content": input_msg})
            st.write(f"You: {input_msg}")

    st.write(f'\n{msg}')
    st.write('=== INTERVIEW OVER ===')

# Streamlit UI
st.subheader("HR Interview Simulation")
interview_position = st.text_input('What role are you applying for?')
interview_name = st.text_input('What is your name?')

if st.button('Start Interview'):
    start_interview(interview_position, interview_name)
