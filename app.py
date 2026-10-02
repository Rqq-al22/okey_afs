import datetime
import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(page_title="Task Prioritizer", layout="centered")

st.title("Task Prioritizer for Lecturers")
st.write(
    "A simple application designed to automatically organize and prioritize"
    " academic workload, lecture prep, and grading tasks."
)

# Initialize Session State
if "task_list" not in st.session_state:
  st.session_state.task_list = []

# --- TASK INPUT FORM ---
with st.form("task_form", clear_on_submit=True):
  st.subheader("Add New Task")

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
    # Priority Score Calculation
    days_left = (deadline - datetime.date.today()).days
    deadline_score = max(1, 5 - max(0, days_left))

    priority_score = (
        (urgency * 0.4) + (importance * 0.4) + (deadline_score * 0.2)
    )

    # Priority Category (Only Color Indicators)
    if urgency >= 3 and importance >= 3:
      quadrant = "🔴 Do First"
    elif urgency < 3 and importance >= 3:
      quadrant = "🔵 Schedule"
    elif urgency >= 3 and importance < 3:
      quadrant = "🟡 Delegate"
    else:
      quadrant = "⚪ Later"

    st.session_state.task_list.append({
        "Task": task_name,
        "Deadline": deadline.strftime("%Y-%m-%d"),
        "Priority Score": round(priority_score, 2),
        "Category": quadrant,
    })
    st.success(f"Task '{task_name}' added successfully!")

# --- DISPLAY & SORT TASKS ---
st.divider()
st.subheader("Prioritized Task List")

if st.session_state.task_list:
  df = pd.DataFrame(st.session_state.task_list)
  df = df.sort_values(by="Priority Score", ascending=False).reset_index(
      drop=True
  )

  st.dataframe(df, use_container_width=True)

  if st.button("Clear All Tasks"):
    st.session_state.task_list = []
    st.rerun()
else:
  st.info("No tasks added yet. Fill out the form above to get started!")
