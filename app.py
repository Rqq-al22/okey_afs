import datetime
import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Lecturer Task Prioritizer", page_icon="📑", layout="centered"
)

st.title("📑 Smart Task Prioritizer for Lecturers")
st.write(
    "A simple web application designed to automatically prioritize academic workload, lecture prep, and grading tasks using a **Weighted Scoring Algorithm** and the **Eisenhower Matrix**."
)

# Initialize Session State
if "task_list" not in st.session_state:
    st.session_state.task_list = []

# --- TASK INPUT FORM ---
with st.form("task_form", clear_on_submit=True):
    st.subheader("➕ Add New Task")

    task_name = st.text_input(
        "Task Title", placeholder="e.g., Grade Midterm Exams - Class A"
    )

    col1, col2 = st.columns(2)
    with col1:
        urgency = st.slider(
            "Urgency Level",
            1,
            5,
            3,
            help="1 = Low urgency / Plenty of time, 5 = Critical / Due soon",
        )
    with col2:
        importance = st.slider(
            "Importance Level",
            1,
            5,
            3,
            help="1 = Low impact, 5 = High impact / Required",
        )

    deadline = st.date_input("Deadline", datetime.date.today())

    submitted = st.form_submit_button("Calculate & Add Task")

    if submitted and task_name:
        # Weighted Scoring Algorithm
        # Priority Score = (Urgency x 0.4) + (Importance x 0.4) + (Deadline Proximity x 0.2)
        days_left = (deadline - datetime.date.today()).days
        deadline_score = max(1, 5 - max(0, days_left))

        priority_score = (
            (urgency * 0.4) + (importance * 0.4) + (deadline_score * 0.2)
        )

        # Eisenhower Matrix Category Assignment
        if urgency >= 3 and importance >= 3:
            quadrant = "🔴 Do First (Urgent & Important)"
        elif urgency < 3 and importance >= 3:
            quadrant = "🔵 Schedule (Important, Not Urgent)"
        elif urgency >= 3 and importance < 3:
            quadrant = "🟡 Delegate (Urgent, Not Important)"
        else:
            quadrant = "⚪ Don't Do / Later (Low Priority)"

        st.session_state.task_list.append({
            "Task": task_name,
            "Deadline": deadline.strftime("%Y-%m-%d"),
            "Priority Score": round(priority_score, 2),
            "Eisenhower Category": quadrant,
        })
        st.success(f"Task '{task_name}' added successfully!")

# --- DISPLAY & SORT TASKS ---
st.divider()
st.subheader("📋 Prioritized Task List")

if st.session_state.task_list:
    # Convert list to DataFrame and sort by Priority Score (Descending)
    df = pd.DataFrame(st.session_state.task_list)
    df = df.sort_values(by="Priority Score", ascending=False).reset_index(
        drop=True
    )

    # Render Table
    st.dataframe(df, use_container_width=True)

    # Clear Data Button
    if st.button("Clear All Tasks"):
        st.session_state.task_list = []
        st.rerun()
else:
    st.info("No tasks added yet. Fill out the form above to get started!")
