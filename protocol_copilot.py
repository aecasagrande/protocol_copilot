import streamlit as st
import pandas as pd
from datetime import datetime
import time
import io

# --- CONFIG & STYLING ---
st.set_page_config(page_title="Study Protocol Copilot", layout="wide")

st.markdown("""
    <style>
    .big-instruction { font-size: 28px !important; font-weight: bold; color: #1f77b4; }
    .key-combo { font-size: 24px; font-weight: bold; background-color: #f0f2f6; padding: 10px; border-radius: 10px; border: 1px solid #ccc; }
    .timer-box { font-size: 40px; font-weight: bold; color: #d62728; text-align: center; }
    .check-box { font-size: 20px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if 'logs' not in st.session_state:
    st.session_state.logs = []

def log_event(event_name, notes=""):
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.logs.append({"Event": event_name, "Time": timestamp, "Notes": notes})
    st.toast(f"Logged: {event_name} at {timestamp}")

# --- TIMER FUNCTION ---
def run_timer(seconds, label):
    placeholder = st.empty()
    progress_bar = st.progress(0)
    
    for i in range(seconds, -1, -1):
        mins, secs = divmod(i, 60)
        time_format = '{:02d}:{:02d}'.format(mins, secs)
        placeholder.markdown(f"<div class='timer-box'>{label}: {time_format}</div>", unsafe_allow_html=True)
        progress_bar.progress((seconds - i) / seconds)
        time.sleep(1)
    
    placeholder.markdown(f"<div class='timer-box'>TIME IS UP! 🛑</div>", unsafe_allow_html=True)
    st.balloons()

# --- SIDEBAR: NAVIGATION ---
st.sidebar.title("Protocol Phases")
phase = st.sidebar.radio("Go to:", [
    "1. Setup & Pre-Flight",
    "2. Baseline (Sit/Stand/Walk)",
    "3. Giladi Protocol (8 Trials)",
    "4. VR Familiarization",
    "5. VR Repositioned",
    "6. Finish & Export Logs"
])

# --- PAGE 1: SETUP ---
if phase == "1. Setup & Pre-Flight":
    st.title("🛠️ Equipment Setup Checklist")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("OPAL Sensors")
        st.checkbox("Access Point connected & Green Light")
        st.checkbox("Sensors flashing Green (Charged)")
        st.checkbox("Sensors placed on subject (2 Shins, 2 Feet, 1 Sacrum)")
        st.checkbox("MobilityLab: Subject Created & PD_HRV Selected")
    
    with col2:
        st.subheader("Cameras & Equivital")
        st.checkbox("GoPros Paired (Frontal + Sagittal)")
        st.checkbox("Equivital SEM Connected & Configured")
        st.checkbox("LabChart: Template Loaded")
        st.checkbox("Subject barefoot?")

    if st.button("Confirm Setup Complete"):
        log_event("Setup Complete")
        st.success("Ready for Baseline!")

# --- PAGE 2: BASELINE ---
elif phase == "2. Baseline (Sit/Stand/Walk)":
    st.title("📊 Baseline Measurements")
    
    tab1, tab2, tab3 = st.tabs(["Sitting (5m)", "Standing (5m)", "Walking (5m)"])
    
    with tab1:
        st.markdown("<div class='big-instruction'>Phase 1: Sitting</div>", unsafe_allow_html=True)
        st.info("Ensure Equivital & Sync App are ready.")
        
        st.markdown("**COMMANDS TO PRESS:**")
        col_a, col_b = st.columns(2)
        col_a.markdown("<div class='key-combo'>Equivital: [Shift + A]</div>", unsafe_allow_html=True)
        col_b.markdown("<div class='key-combo'>Sync App: 'Start 5 min Sitting'</div>", unsafe_allow_html=True)
        
        if st.button("▶️ START 5-Min Timer (Sitting)"):
            log_event("Baseline Sitting START")
            run_timer(300, "Sitting Timer")
            log_event("Baseline Sitting END")
            st.warning("PRESS: Equivital [Shift + E] + Sync App 'End'")

    with tab2:
        st.markdown("<div class='big-instruction'>Phase 2: Standing</div>", unsafe_allow_html=True)
        st.warning("Take Blood Pressure before starting this!")
        
        st.markdown("**COMMANDS TO PRESS:**")
        col_a, col_b = st.columns(2)
        col_a.markdown("<div class='key-combo'>Equivital: [Shift + A]</div>", unsafe_allow_html=True)
        col_b.markdown("<div class='key-combo'>Sync App: 'Start 5 min Standing'</div>", unsafe_allow_html=True)

        if st.button("▶️ START 5-Min Timer (Standing)"):
            log_event("Baseline Standing START")
            run_timer(300, "Standing Timer")
            log_event("Baseline Standing END")
            st.warning("PRESS: Equivital [Shift + E] + Sync App 'End'")

    with tab3:
        st.markdown("<div class='big-instruction'>Phase 3: Walking</div>", unsafe_allow_html=True)
        st.error("⚠️ CAMERAS: Blue Mark (Entry + Gait Carpet)")
        
        st.markdown("**COMMANDS TO PRESS:**")
        st.markdown("- **VideoSync:** Type 'Record' (Enter)")
        st.markdown("- **Remote:** Press Right Arrow (>)")
        
        col_a, col_b = st.columns(2)
        col_a.markdown("<div class='key-combo'>Equivital: [Shift + A]</div>", unsafe_allow_html=True)
        col_b.markdown("<div class='key-combo'>Sync App: 'Start 5 min Walk'</div>", unsafe_allow_html=True)

        if st.button("▶️ START 5-Min Timer (Walking)"):
            log_event("Baseline Walking START")
            run_timer(300, "Walking Timer")
            log_event("Baseline Walking END")
            st.warning("PRESS: Equivital [Shift + E] + Sync App 'End' + Remote (>)")

# --- PAGE 3: GILADI ---
elif phase == "3. Giladi Protocol (8 Trials)":
    st.title("🔄 Giladi Protocol")
    
    st.error("⚠️ CAMERAS: Green Tape (Whiteboard + Window)")
    
    trial_num = st.number_input("Current Trial Number", 1, 8, 1)
    
    st.markdown(f"### Running Trial {trial_num}")
    
    st.info("1. VideoSync: Recall 'Record' -> Enter (Pending)")
    st.info("2. MobilityLab: Select Test")
    st.info("3. Wait for instructions...")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button(f"🚀 START Trial {trial_num} (Trigger)"):
            log_event(f"Giladi Trial {trial_num} START")
            st.success("LOGGED: Start Timestamp. (Press Remote + Sync App NOW)")
    
    with col2:
        if st.button(f"🛑 STOP Trial {trial_num}"):
            log_event(f"Giladi Trial {trial_num} END")
            st.warning("LOGGED: Stop Timestamp. (Press Remote + Sync App NOW)")

    if trial_num == 7:
        st.markdown("---")
        st.error("🚨 NEXT IS TRIAL 8 (DOORWAY): MOVE FRONTAL CAMERA TO GREEN TAPE BY DESKS!")

# --- PAGE 4: VR FAMILIARIZATION ---
elif phase == "4. VR Familiarization":
    st.title("🥽 VR Familiarization")
    st.markdown("Sequence: Sit (2m) -> Stand (2m) -> Walk (2m)")
    
    mode = st.radio("Select Mode", ["Sitting", "Standing", "Walking"], horizontal=True)
    
    if mode == "Sitting":
        st.markdown("<div class='key-combo'>Equivital: [Shift + S] | Sync: 'Start 2 min sit'</div>", unsafe_allow_html=True)
        if st.button("Start 2m Timer"):
            log_event("VR Fam Sitting START")
            run_timer(120, "VR Sitting")
            log_event("VR Fam Sitting END")

    elif mode == "Standing":
        st.markdown("<div class='key-combo'>Equivital: [Shift + S] | Sync: 'Start 2 min stand'</div>", unsafe_allow_html=True)
        if st.button("Start 2m Timer"):
            log_event("VR Fam Standing START")
            run_timer(120, "VR Standing")
            log_event("VR Fam Standing END")

    elif mode == "Walking":
        st.markdown("<div class='key-combo'>Equivital: [Shift + S] | Sync: 'Start 2 min walk'</div>", unsafe_allow_html=True)
        if st.button("Start 2m Timer"):
            log_event("VR Fam Walking START")
            run_timer(120, "VR Walking")
            log_event("VR Fam Walking END")

# --- PAGE 6: EXPORT ---
elif phase == "6. Finish & Export Logs":
    st.title("💾 Session Complete")
    st.write("Here is the timeline of events for this session. Download this to sync your Equivital/Video data.")
    
    df_log = pd.DataFrame(st.session_state.logs)
    st.dataframe(df_log)
    
    # Create CSV
    csv = df_log.to_csv(index=False).encode('utf-8')
    
    st.download_button(
        "📥 Download Session Log (CSV)",
        csv,
        "session_logs.csv",
        "text/csv",
        key='download-csv'
    )
