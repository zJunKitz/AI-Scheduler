import streamlit as st
import datetime
from Parameters import Parameters
from timetable_filter import find_unique, filter_timetable
from ask_gpt import generate_timetable_gpt

subject_parameters = {}

if 'subject_num' not in st.session_state:
    st.session_state.subject_num = 1

if 'subject_names' not in st.session_state:
    st.session_state.subject_names = [ ]

st.title("Timetable Scheduler")

for i in range(st.session_state.subject_num):

    with st.expander(f"Subject {i+1}", expanded = True):
        uploaded_csv = st.file_uploader(f"Upload CSV for Subject {i+1}", type = "csv", key = f"csv_{i}")

        if uploaded_csv:
            available_lecturers = find_unique(uploaded_csv, 'LECTURER')

            subject_name = st.text_input(
                f"Subject Name",
                key = f"subject_name_{i}"
            )
            undesired_days = st.multiselect(
                f"Filter classes on:", 
                ('MON','TUE','WED','THUR','FRI','SAT'), 
                key = f"undesired_day_{i}"
                )
            threshold_start_time = st.time_input(
                f"Filter classes with starting time later than:", 
                key = f"undesired_time_{i}",
                #value = datetime.time(16,0)
                )
            undesired_lecturer = st.selectbox(
                f"Filter classes taught by:", ['NONE'] + available_lecturers, 
                key = f"undesired_lecturer_{i}"
                )

            # Save parameters for each subject
            params = Parameters(
                subject_name=subject_name,
                undesired_days=undesired_days,
                threshold_start_time=str(threshold_start_time),
                undesired_lecturer=[undesired_lecturer]
            )
            subject_parameters[i] = (uploaded_csv, params)

        

#Add/delete subject buttons
def add_subject():
    if st.session_state.subject_num < 5:
        st.session_state.subject_num += 1
        st.rerun()
    else:
        st.toast("Maximum number of subjects reached")

def delete_subject():
    if st.session_state.subject_num > 1:
        st.session_state.subject_num -= 1
        st.rerun()
    else:
        st.toast("You didn't even take **one** subject?")

col1, col2 = st.columns([1,4])
with col1:
    if st.button("Add subject"):
        add_subject()

with col2:
    if st.button("Remove subject"):
        delete_subject()

st.divider()

filtered_timetables = """"""
if st.button("Generate Timetable"):
    for idx, (csv_file, params) in subject_parameters.items():
        filtered_df = filter_timetable(csv_file, params)
        st.write(f"Filtered Timetable for **{params.subject_name}**")
        st.dataframe(filtered_df)

        filtered_timetables += "Timetable for " + params.subject_name + ":\n" + filtered_df.to_csv(index=False) + "\n\n"

    st.divider()
    
    filtered_timetables += "Make sure lecture classes of each subject with the same CLASS_ID (NOT TO BE CONFUSED WITH ASSOCIATED_LEC_ID) are all taken together into your table."
    ai_suggestion = generate_timetable_gpt(filtered_timetables)
    st.write(ai_suggestion)









