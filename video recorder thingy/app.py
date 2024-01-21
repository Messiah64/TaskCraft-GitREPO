import os
import sys
import streamlit as st
import whisper
from audio_recorder_streamlit import audio_recorder
from datetime import datetime
import openai
import datetime as dt
import streamlit as st
import requests
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

###CSS Styling
class dataProcessor:
    
    def __init__(self):
        # Initalize instance attributes
        self.file_name = "./docs/static/style.css"
        self.email = None
        self.contact_number = None

    #CSS File For Streamlit Pages
    def local_css(self):
        with open(self.file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

dataprocessor = dataProcessor()# Create Class instance
dataprocessor.local_css()

# Set your OpenAI API key
openai.api_key = "sk-APIKEY"
# Set up Google Calendar API
SCOPES_CALENDAR = ["https://www.googleapis.com/auth/calendar"]
# Set up Google Drive API
SCOPES_DRIVE = ["https://www.googleapis.com/auth/drive.file"]



# Event input is the transcripted text
# Calendar ID is the target Gmail
# Timezone is Singapore/Asia by default
def create_google_calendar_events(event_input, calendar_id, timezone):
    key_dict = json.loads(st.secrets["textkey"])
    creds = service_account.Credentials.from_service_account_info(key_dict, scopes=SCOPES_CALENDAR)
    service = build("calendar", "v3", credentials=creds)

    events_data = event_input.split('|')

    for i in range(0, len(events_data), 4):
        summary = events_data[i].strip()
        description = events_data[i + 1].strip()
        start_datetime = events_data[i + 2].strip()
        end_datetime = events_data[i + 3].strip()

        event = {
            'summary': summary,
            'description': description,
            'start': {
                'dateTime': start_datetime,
                'timeZone': timezone,
            },
            'end': {
                'dateTime': end_datetime,
                'timeZone': timezone,
            },
        }

        service.events().insert(calendarId=calendar_id, body=event).execute()

    print("Events created successfully.")

# Google Calendar API Email Address: alphatrack@alpha-track-400504.iam.gserviceaccount.com
def generate_schedule_planner_response(transcripted_text):

    # Get the current date and time
    current_datetime = datetime.now()
    # Format the date and time as strings
    formatted_date = current_datetime.strftime("%Y-%m-%d")
    formatted_time = current_datetime.strftime("%H:%M:%S")


    # Define the conversation messages
    messages = [
        {"role": "system", "content": "You are an expert personal schedule planner. You will get a text string, detailing a student's assignments, tasks, and home chores that needs to be done, you will also get their completion date. I want you to first identify all the tasks to do and then using your expertness to rank the tasks in order of priority of most due deadline. You may choose to break down larger tasks of the student like a School report into smaller chunks and spread them over more days until the deadline. Keep in mind, i sleep by 12am to 7am every night. Feel free to estimate time taken to complete each task but be resonable, and dont forget the other tasks too. The format of output is a string: summary|description|start_datetime|end_datetime|summary|description|start_datetime|end_datetime|summary|description|start_datetime|end_datetime . An example of output is: Finish math homework|10 calculus questions|2023-11-05T14:00:00|2023-11-05T15:00:00|. Dont give me answer in any other format than the example output as shown. Dont give me anything other than the correct output. Make sure you adhere to the sleep schedule, as well as the time deadlline in each task."},
        {"role": "user", "content": f"Current time is: {formatted_time}, Current date is: {formatted_date}. " + transcripted_text},
    ]

    # Call OpenAI Chat API
    response = openai.ChatCompletion.create(
        model="gpt-4",
        max_tokens=2048,
        messages=messages,
    )

    # Extract and return the content of the generated response
    generated_response = response["choices"][0]["message"]["content"]
    return generated_response


# Google Calendar API Email Address: alphatrack@alpha-track-400504.iam.gserviceaccount.com
def extract_tasks(google_calender_response):

     

    # Define the conversation messages
    messages = [
        {"role": "system", "content": "You are an expert on google calender API documentation. You will get a text string, detailing a student's tasks. I want you to extract the tasks one by one, and lay them out in point form. Its very important you do this properly and exactly what i say. I want it in neat point form. I do not want the time in ISO 8601, but instead in normal time. for example: 15:00 is 3PM"},
        {"role": "user", "content": "Extract data and leave it in point form. " + google_calender_response},
    ]

    # Call OpenAI Chat API
    response = openai.ChatCompletion.create(
        model="gpt-4",
        max_tokens=2048,
        messages=messages,
    )

    # Extract and return the content of the generated response
    generated_response = response["choices"][0]["message"]["content"]
    return generated_response

# checks if the tasks are done on time
def response_checker(transcripted_text):

    # Get the current date and time
    current_datetime = datetime.now()
    # Format the date and time as strings
    formatted_date = current_datetime.strftime("%Y-%m-%d")
    formatted_time = current_datetime.strftime("%H:%M:%S")


    # Define the conversation messages
    messages = [
        {"role": "system", "content": "You are an expert personal schedule planner. You will get a text string, detailing a student's assignments, tasks, and home chores that needs to be done, you will also note their completion date. Your job is to check if the tasks are done on time. If not, you will need to reschedule the tasks. You may choose to break down larger tasks of the student like a School report into smaller chunks and spread them over more days until the deadline. Keep in mind, i sleep by 12am to 7am every night. Feel free to estimate time taken to complete each task but be resonable, and dont forget the other tasks too. The format of output is a string: summary|description|start_datetime|end_datetime|summary|description|start_datetime|end_datetime|summary|description|start_datetime|end_datetime . An example of output is: Finish math homework|10 calculus questions|2023-11-05T14:00:00|2023-11-05T15:00:00|. Dont give me answer in any other format than the example output as shown. Dont give me anything other than the correct output. Make sure you adhere to the sleep schedule, as well as the time deadlline in each task. Very important to check the input for time adhering. if no tasks are mismatched, then just return the output. Dont give me any other explaination or whatever, Make sure you follow the format."},
        {"role": "user", "content": "Check following for correct timing adherement. " + formatted_date + formatted_time + transcripted_text},
    ]

    # Call OpenAI Chat API
    response = openai.ChatCompletion.create(
        model="gpt-4",
        max_tokens=2048,
        messages=messages,
    )

    # Extract and return the content of the generated response
    generated_response = response["choices"][0]["message"]["content"]
    return generated_response




# Set up path to utility folder
absolute_path = os.path.join(os.path.dirname(__file__), 'utility')
sys.path.append(absolute_path)  # Add the absolute path to the system path

# Create Class instance
# dataprocessor = dataProcessor()

# dataprocessor.local_css()


st.markdown(
    """
    # :red[TaskCraft] 📝📅:
    ##### :white[Create tasks from your thoughts] 
    ##### :white[No more fretting over what and when you need to do things] 
    """
)

st.text("")
st.text("")

label_gmail = r'''
$\textsf{
     \Large Enter E-mail for Google Calendar:
}$
'''

target_gmail = st.text_input(label_gmail)

st.text("")
st.text("")

# Audio recording
# from st_audiorec import st_audiorec
# audio_bytes = st_audiorec()
col1, col2, col3 = st.columns(3)
with col1:
    audio_bytes = audio_recorder(
        text="Record",
        recording_color="#FF0000",
        neutral_color="#FFFFFF",
        icon_name="microphone",
        icon_size="1x",
    )
    if audio_bytes:
        value = st.audio(audio_bytes, format="audio/wav")

# Button to process the audio
with st.form("record_form"):
    # Every form must have a submit button.
    submitted = st.form_submit_button("Start Processing")

# Load Whisper model
model = whisper.load_model("base") 
st.success("Model Loaded")

# If the Process button is clicked
if submitted:
    if audio_bytes is not None:
        if target_gmail is not None:

            # Create Google Calendar events
            st.success("Processing Audio")

            # Save audio bytes to a temporary file
            temp_file_path = "temp_audio.wav"
            with open(temp_file_path, "wb") as temp_file:
                temp_file.write(audio_bytes)
            # Transcribe from the temporary file
            try:
                transcription = model.transcribe(temp_file_path)
            except RuntimeError as e:
                st.error(f"Error during transcription: {str(e)}")
            finally:
                # Remove the temporary file
                os.remove(temp_file_path)

            st.markdown(transcription["text"])
            st.success("Transcription completed successfully")
            

            #Test with Default Transcripted Text
            # transcripted_text = "I need to finish my math homework by 8 pm today. I have 10 calculus questions to do. I have to sweep the floor and do the dishes soon, and need my parents' signature on a consent form for tomorrow's school trip"
            gpt4_response = generate_schedule_planner_response(transcription["text"])
            st.success("Tasks are being created ...")
            Task_Extraction = extract_tasks(response_checker(gpt4_response))
            print(Task_Extraction,"Task_Extraction")
            st.markdown(Task_Extraction)
            gpt4_response = response_checker(gpt4_response)
            st.success("Tasks Created successfully")
            create_google_calendar_events(gpt4_response, target_gmail, 'Asia/Singapore')
            st.success("Events created successfully.")
            
            # Event input is the transcripted text
            # Calendar ID is the target Gmail
            # Timezone is Singapore/Asia by default


        else:
            st.error("Please enter your gmail address in text box")
    
    else:
        st.error("Please record audio")

