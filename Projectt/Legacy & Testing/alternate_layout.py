import streamlit as st

# Initialize session state for storing subject names
if 'subject_names' not in st.session_state:
    st.session_state.subject_names = []

# Function to add a subject title
def add_subject():
    new_subject_name = st.text_input("Enter subject name:", value="")
    
    if st.button("Confirm", key="confirm_subject"):
        if new_subject_name:
            st.session_state.subject_names.append(new_subject_name)
            st.rerun()  # Rerun to display the new "div"

# Display the form to enter new subject names
add_subject()

# Display a "div" (expander) for each subject in the session state
for i, subject_name in enumerate(st.session_state.subject_names):
    with st.expander(subject_name, expanded=True):
        st.write(f"Settings for {subject_name}")
        
        # Add delete button next to each subject
        if st.button(f"Delete {subject_name}", key=f"delete_{i}"):
            st.session_state.subject_names.pop(i)  # Remove the subject
            st.rerun()  # Refresh the app to reflect changes
