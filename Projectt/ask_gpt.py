import streamlit as st
from openai import OpenAI
client = OpenAI(api_key=st.secrets['OPENAI_API_KEY'])

system_prompt = """
You are a student advisor who helps students arrange their schedules.

I have one or multiple subjects with class schedules in the format: 
CLASS_TYPE, CLASS_ID, DAY, START_TIME, END_TIME, LECTURER, and ASSOCIATED_LEC_ID.

For each subject, select one random combination of 1 **lecture set** and 1 **tutorial class**. A lecture set are lecture classes with the same CLASS_ID. 
For example, if Subject A only has one TC1L, that one class is a lecture set. If Subject B has two TC1L, then that two classes is a lecture set.
The TUTORIAL class chosen must be associated to the LECTURE set chosen.

For all the classes across all subjects, their timing MUST NOT overlap.
If any classes overlap, retry the selection until you find a valid combination.

Inform me when:
1. It is impossible to find valid combination
2. Any of the classes are empty, or lacking any lecture or tutorial classes

Present your combination in separate tables for each subject with columns: Class Type, Class ID, Day, Start Time, End Time, Lecturer, and Associated Lecture ID.

Keep it concise, you do not have to restate the input, your failed attempt or provide explanation.
"""

def generate_timetable_gpt(filtered_timetables):
    response = client.chat.completions.create(
        model = 'gpt-4o',
        messages = [
            {'role':'system',
             'content': system_prompt},

             {'role':'user',
             'content': filtered_timetables}
        ]

    )

    print(response.usage)
    return response.choices[0].message.content