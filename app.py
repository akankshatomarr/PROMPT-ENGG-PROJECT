
import streamlit as st
from datetime import date, datetime, time, timedelta
import csv
import io
import math

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="SmartStudy | Study Planner",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# PROFESSIONAL BROWN & WHITE DESIGN
# =========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: #F7F3ED;
    color: #38271D;
}

header[data-testid="stHeader"] {
    background: #F7F3ED;
}

.block-container {
    max-width: 1150px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

.brand {
    font-size: 30px;
    font-weight: 800;
    color: #39251B;
    letter-spacing: -1.2px;
    margin-bottom: 3px;
}

.brand-sub {
    color: #806C5C;
    font-size: 13px;
    margin-bottom: 28px;
}

.hero {
    background: linear-gradient(120deg, #39251B, #634532);
    padding: 35px;
    border-radius: 18px;
    color: white;
    margin-bottom: 30px;
}

.hero h1 {
    font-size: 34px;
    font-weight: 800;
    color: white;
    margin: 0 0 10px 0;
}

.hero p {
    color: #E8DCD1;
    font-size: 15px;
    margin: 0;
}

.section-heading {
    color: #39251B;
    font-size: 23px;
    font-weight: 800;
    margin: 15px 0 5px 0;
}

.section-sub {
    color: #806C5C;
    font-size: 13px;
    margin-bottom: 20px;
}

div[data-testid="stForm"] {
    background: #FFFFFF;
    border: 1px solid #E7DDD1;
    border-radius: 16px;
    padding: 25px;
}

div[data-testid="stForm"] label {
    color: #493426 !important;
    font-weight: 600 !important;
}

.stTextInput input,
.stTextArea textarea,
.stNumberInput input,
.stSelectbox div[data-baseweb="select"] > div {
    background-color: #FCFAF7 !important;
    color: #39251B !important;
    border: 1px solid #D9CABC !important;
    border-radius: 9px !important;
}

.stTextArea textarea {
    min-height: 190px;
}

.stButton button,
.stFormSubmitButton button {
    background: #493021 !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 9px !important;
    padding: 11px 20px !important;
    font-weight: 700 !important;
    min-height: 45px;
}

.stButton button:hover,
.stFormSubmitButton button:hover {
    background: #674733 !important;
    color: white !important;
}

.metric-card {
    background: white;
    border: 1px solid #E7DDD1;
    border-radius: 13px;
    padding: 18px;
    margin-bottom: 12px;
}

.metric-label {
    color: #806C5C;
    font-size: 12px;
    font-weight: 600;
}

.metric-value {
    color: #39251B;
    font-size: 25px;
    font-weight: 800;
    margin-top: 5px;
}

.study-card {
    background: #FFFFFF;
    border: 1px solid #E8DED2;
    border-left: 5px solid #684A35;
    padding: 15px 18px;
    border-radius: 10px;
    margin: 10px 0;
}

.break-card {
    background: #F0E9DF;
    border: 1px solid #E2D4C5;
    border-left: 5px solid #B18B66;
    padding: 12px 18px;
    border-radius: 10px;
    margin: 10px 0;
}

.session-time {
    color: #76563D;
    font-size: 12px;
    font-weight: 700;
}

.session-name {
    color: #39251B;
    font-size: 16px;
    font-weight: 800;
    margin-top: 5px;
}

.session-detail {
    color: #806C5C;
    font-size: 13px;
    margin-top: 4px;
}

div[data-testid="stExpander"] {
    background: white;
    border: 1px solid #E5D9CC;
    border-radius: 12px;
    margin-bottom: 10px;
}

div[data-testid="stExpander"] summary {
    color: #39251B;
    font-weight: 700;
}

.footer {
    text-align: center;
    color: #927D6D;
    font-size: 12px;
    margin-top: 55px;
}

hr {
    border-color: #E5D9CC;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="brand">📚 SmartStudy</div>
<div class="brand-sub">YOUR PERSONAL STUDY PLANNING ASSISTANT</div>

<div class="hero">
    <h1>Study smarter. Achieve more.</h1>
    <p>
        Build a structured study routine, prepare for exams,
        and make every study session count.
    </p>
</div>
""", unsafe_allow_html=True)


# =========================================================
# TIME OPTIONS
# =========================================================

TIME_OPTIONS = []

for hour in range(6, 23):
    for minute in (0, 30):
        t = time(hour, minute)
        TIME_OPTIONS.append(t.strftime("%I:%M %p"))


# =========================================================
# SUBJECT PARSER
# =========================================================

def parse_subjects(text):
    subjects = []

    for line in text.strip().splitlines():

        if not line.strip():
            continue

        parts = [part.strip() for part in line.split("|")]

        name = parts[0]

        if not name:
            continue

        exam_date = None
        difficulty = "Medium"
        topics = []

        if len(parts) >= 2 and parts[1]:
            try:
                exam_date = date.fromisoformat(parts[1])
            except ValueError:
                # A non-date second field is treated as a difficulty.
                if parts[1].capitalize() in ["Easy", "Medium", "Hard"]:
                    difficulty = parts[1].capitalize()

        if len(parts) >= 3:
            if parts[2].capitalize() in ["Easy", "Medium", "Hard"]:
                difficulty = parts[2].capitalize()
            elif parts[2]:
                topics = [
                    x.strip()
                    for x in parts[2].split(",")
                    if x.strip()
                ]

        if len(parts) >= 4:
            topics = [
                x.strip()
                for x in parts[3].split(",")
                if x.strip()
            ]

        subjects.append({
            "name": name,
            "exam_date": exam_date,
            "difficulty": difficulty,
            "topics": topics
        })

    return subjects


# =========================================================
# TIMETABLE GENERATOR
# =========================================================

def generate_timetable(
    subjects,
    start_date,
    days,
    daily_hours,
    start_time,
    break_minutes
):

    timetable = []

    total_minutes = int(daily_hours * 60)

    # Divide study time into manageable sessions.
    session_lengths = []

    remaining = total_minutes

    while remaining > 0:
        session = min(50, remaining)
        session_lengths.append(session)
        remaining -= session

    number_of_sessions = len(session_lengths)

    # Prioritize subjects with earlier exams.
    sorted_subjects = sorted(
        subjects,
        key=lambda x: (
            x["exam_date"] is None,
            x["exam_date"] or date.max
        )
    )

    for day_index in range(days):

        current_date = start_date + timedelta(days=day_index)

        current_time = datetime.combine(
            current_date,
            start_time
        )

        daily_schedule = []

        for session_index, duration in enumerate(session_lengths):

            subject_index = (
                day_index * number_of_sessions + session_index
            ) % len(sorted_subjects)

            subject = sorted_subjects[subject_index]

            topics = subject["topics"]

            if topics:
                topic = topics[
                    (day_index + session_index) % len(topics)
                ]
            else:
                topic = "Concept learning and practice"

            # Use a revision session near the end of the plan.
            is_revision = (
                day_index == days - 1
                and session_index == number_of_sessions - 1
            )

            session_name = (
                "Revision & practice" if is_revision
                else "Focused study"
            )

            end_time = current_time + timedelta(minutes=duration)

            daily_schedule.append({
                "type": "study",
                "start": current_time,
                "end": end_time,
                "subject": subject["name"],
                "topic": topic,
                "duration": duration,
                "session_name": session_name
            })

            current_time = end_time

            # Add breaks between study sessions.
            if session_index < number_of_sessions - 1:

                break_end = current_time + timedelta(
                    minutes=break_minutes
                )

                daily_schedule.append({
                    "type": "break",
                    "start": current_time,
                    "end": break_end,
                    "duration": break_minutes
                })

                current_time = break_end

        timetable.append({
            "date": current_date,
            "sessions": daily_schedule
        })

    return timetable


# =========================================================
# INPUT FORM
# =========================================================

st.markdown(
    '<div class="section-heading">Create your study plan</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-sub">Enter your subjects and preferences to generate your personalized timetable.</div>',
    unsafe_allow_html=True
)

with st.form("study_plan_form"):

    left, right = st.columns(2, gap="large")

    with left:

        st.markdown("### 01  Academic details")

        student_name = st.text_input(
            "Your name",
            placeholder="Enter your name (optional)"
        )

        subject_text = st.text_area(
            "Subjects and topics",
            placeholder="""Enter one subject per line:

Data Structures | 2026-12-10 | Hard | Trees, Graphs, Sorting
Operating Systems | 2026-12-15 | Medium | Processes, Deadlocks
Computer Networks | 2026-12-20 | Easy | TCP, IP, Routing""",
            height=210
        )

        st.caption(
            "Format: Subject | YYYY-MM-DD | Difficulty | Topics"
        )

        st.caption(
            "You can also enter just a subject name."
        )

    with right:

        st.markdown("### 02  Study preferences")

        daily_hours = st.number_input(
            "Daily study hours",
            min_value=1,
            max_value=12,
            value=4,
            step=1
        )

        planning_days = st.selectbox(
            "Planning period",
            options=[3, 5, 7, 10, 15, 20, 30],
            index=2,
            format_func=lambda x: f"{x} days"
        )

        start_date_text = st.text_input(
            "Start date (YYYY-MM-DD)",
            value=date.today().isoformat()
        )

        preferred_time = st.selectbox(
            "Preferred start time",
            options=TIME_OPTIONS,
            index=6
        )

        break_duration = st.selectbox(
            "Break duration",
            options=[5, 10, 15, 20],
            index=1,
            format_func=lambda x: f"{x} minutes"
        )

    st.markdown("---")

    submitted = st.form_submit_button(
        "Generate my study timetable →",
        use_container_width=True
    )


# =========================================================
# GENERATE AND SAVE PLAN
# =========================================================

if submitted:

    subjects = parse_subjects(subject_text)

    if not subjects:
        st.error("Please enter at least one subject.")

    else:
        try:
            selected_date = date.fromisoformat(
                start_date_text.strip()
            )

            selected_time = datetime.strptime(
                preferred_time,
                "%I:%M %p"
            ).time()

            plan = generate_timetable(
                subjects=subjects,
                start_date=selected_date,
                days=planning_days,
                daily_hours=daily_hours,
                start_time=selected_time,
                break_minutes=break_duration
            )

            st.session_state["generated_plan"] = plan

            st.session_state["plan_info"] = {
                "name": student_name,
                "subjects": subjects,
                "days": planning_days,
                "hours": daily_hours,
                "break": break_duration
            }

        except ValueError:
            st.error(
                "Invalid date. Please enter the date as YYYY-MM-DD."
            )


# =========================================================
# DISPLAY GENERATED TIMETABLE
# =========================================================

if "generated_plan" in st.session_state:

    plan = st.session_state["generated_plan"]
    info = st.session_state["plan_info"]

    st.markdown("---")

    st.markdown(
        '<div class="section-heading">Your study dashboard</div>',
        unsafe_allow_html=True
    )

    if info["name"]:
        st.markdown(
            f"Welcome, **{info['name']}**! Here's your study plan."
        )
    else:
        st.write("Your personalized study plan is ready.")

    # Summary cards
    c1, c2, c3, c4 = st.columns(4)

    metrics = [
        ("SUBJECTS", len(info["subjects"])),
        ("PLANNING PERIOD", f"{info['days']} days"),
        ("DAILY STUDY", f"{info['hours']} hours"),
        ("BREAK DURATION", f"{info['break']} min")
    ]

    for col, (label, value) in zip(
        [c1, c2, c3, c4],
        metrics
    ):

        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("### Your timetable")

    st.caption(
        "Select a day to view its study sessions. "
        "All times are displayed in AM/PM format."
    )

    # One compact expandable section per day.
    for day_index, day in enumerate(plan):

        day_date = day["date"]

        study_count = sum(
            1 for s in day["sessions"]
            if s["type"] == "study"
        )

        with st.expander(
            f"DAY {day_index + 1}  |  "
            f"{day_date.strftime('%A, %d %B %Y')}  |  "
            f"{study_count} study sessions",
            expanded=(day_index == 0)
        ):

            for session in day["sessions"]:

                start = session["start"].strftime("%I:%M %p")
                end = session["end"].strftime("%I:%M %p")

                if session["type"] == "study":

                    st.markdown(f"""
                    <div class="study-card">
                        <div class="session-time">
                            📖 {start} – {end}
                            &nbsp; | &nbsp;
                            {session['duration']} minutes
                        </div>
                        <div class="session-name">
                            {session['subject']}
                        </div>
                        <div class="session-detail">
                            {session['session_name']} · {session['topic']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                else:

                    st.markdown(f"""
                    <div class="break-card">
                        <div class="session-time">
                            ☕ {start} – {end}
                            &nbsp; | &nbsp;
                            {session['duration']} minutes
                        </div>
                        <div class="session-name">
                            Relax and recharge
                        </div>
                        <div class="session-detail">
                            Take a short break before your next session.
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

    # =====================================================
    # DOWNLOAD TIMETABLE
    # =====================================================

    st.markdown("---")

    st.markdown("### Export your timetable")

    csv_buffer = io.StringIO()

    writer = csv.writer(csv_buffer)

    writer.writerow([
        "Date",
        "Day",
        "Start Time",
        "End Time",
        "Session Type",
        "Subject",
        "Topic",
        "Duration (minutes)"
    ])

    for day in plan:

        for session in day["sessions"]:

            if session["type"] == "study":
                session_type = session["session_name"]
                subject = session["subject"]
                topic = session["topic"]
            else:
                session_type = "Break"
                subject = ""
                topic = "Relax and recharge"

            writer.writerow([
                day["date"].isoformat(),
                day["date"].strftime("%A"),
                session["start"].strftime("%I:%M %p"),
                session["end"].strftime("%I:%M %p"),
                session_type,
                subject,
                topic,
                session["duration"]
            ])

    st.download_button(
        label="⬇ Download study timetable (CSV)",
        data=csv_buffer.getvalue(),
        file_name="SmartStudy_Timetable.csv",
        mime="text/csv",
        use_container_width=True
    )

    if st.button("Create a new study plan", use_container_width=True):

        del st.session_state["generated_plan"]
        del st.session_state["plan_info"]

        st.rerun()


# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div class="footer">
    <b>SMARTSTUDY</b><br>
    Plan smarter. Study better. Achieve more.<br><br>
    Your personal study planning assistant.
</div>
""", unsafe_allow_html=True)
