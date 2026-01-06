import streamlit as st
import time

# --- PAGE CONFIG ---
st.set_page_config(page_title="Lab Protocol Trainer", layout="wide", page_icon="🎓")

# --- CSS FOR REALISM ---
st.markdown("""
    <style>
    .hardware-card { background-color: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 5px solid #ff4b4b; margin-bottom: 10px; }
    .sim-screen { background-color: #000; color: #0f0; padding: 20px; font-family: 'Courier New', monospace; border-radius: 5px; margin-bottom: 20px; }
    .success-msg { color: green; font-weight: bold; }
    .error-msg { color: red; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- SESSION STATE (To track progress) ---
if 'sim_step' not in st.session_state:
    st.session_state.sim_step = 0
if 'sim_log' not in st.session_state:
    st.session_state.sim_log = []

# --- SIDEBAR NAVIGATION ---
st.sidebar.header("🎓 Training Modules")
module = st.sidebar.radio("Select Module:", [
    "1. The Hardware Zoo",
    "2. The 'Sync' Theory",
    "3. Practice: The 5-Min Walk",
    "4. Exam: Full Giladi Trial"
])

# --- MODULE 1: HARDWARE ---
if module == "1. The Hardware Zoo":
    st.title("Module 1: Know Your Gear")
    st.write("Before you touch a button, you must identify the equipment.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.image("https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&w=300&q=80", caption="Symbolic Lab Image")
        with st.expander("🔵 OPAL Sensors (MobilityLab)"):
            st.markdown("""
            **What it is:** Motion sensors on the body.
            **Critical Check:** Must be flashing GREEN before starting.
            **Placement:** 2 Shins, 2 Feet, 1 Lower Back (Belt).
            """)
        with st.expander("🔴 GoPros (Video Sync)"):
            st.markdown("""
            **What it is:** 2 Cameras (Frontal + Sagittal).
            **Critical Check:** Battery must be charged. Red light flashes when recording.
            **The Trap:** Always check they are paired in the GoProSync App first!
            """)
            
    with col2:
        with st.expander("🟢 Equivital (LabChart)"):
            st.markdown("""
            **What it is:** Chest strap for physiological data (ECG/Breathing).
            **Critical Check:** Ensure SEM is clicked in.
            **Key Commands:** `Shift+A` (Start), `Shift+E` (End).
            """)
        with st.expander("📱 Sync App (Tablet)"):
            st.markdown("""
            **What it is:** The 'Master Clock' that logs timestamps.
            **Rule:** You almost ALWAYS press this simultaneously with another key.
            """)

# --- MODULE 2: THEORY ---
elif module == "2. The 'Sync' Theory":
    st.title("Module 2: The Synchronization Dance")
    st.markdown("### The Golden Rule: Simultaneous Pressing")
    st.info("💡 **Why do we do this?** We have 3 different computers collecting data. If you start one 5 seconds late, we can't match the heart rate to the walking speed later. We use 'Triggers' to start them at the exact same millisecond.")

    st.subheader("The 3 Key Combinations")
    st.markdown("Memorize these pairs. You will be tested.")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("#### 1. The Physio Start")
        st.markdown("<div class='hardware-card'>Left Hand: <b>Shift + A</b> (Equivital)<br>Right Hand: <b>'Start'</b> (Sync App)</div>", unsafe_allow_html=True)
    with c2:
        st.markdown("#### 2. The Video Start")
        st.markdown("<div class='hardware-card'>Left Hand: <b>Right Arrow ></b> (Remote)<br>Right Hand: <b>'Start'</b> (Sync App)</div>", unsafe_allow_html=True)
    with c3:
        st.markdown("#### 3. The Walk Start")
        st.markdown("<div class='hardware-card'>Left Hand: <b>Shift + W</b> (Equivital)<br>Right Hand: <b>'Start Walk'</b> (Sync App)</div>", unsafe_allow_html=True)

# --- MODULE 3: SIMULATOR (WALKING BASELINE) ---
elif module == "3. Practice: The 5-Min Walk":
    st.title("✈️ Flight Simulator: Baseline Walking")
    st.write("Welcome to the Virtual Lab. Your goal is to successfully start the 5-Minute Walking Baseline without error.")
    
    # Define the correct sequence
    # Step 0: Check Cameras -> Step 1: Type Record -> Step 2: Shift+A/Sync -> Step 3: Wait -> Step 4: Stop
    
    st.markdown("### 🖥️ Virtual Control Panel")
    
    # Status Screen
    status_text = "SYSTEM IDLE. Waiting for protocol start..."
    if st.session_state.sim_step == 1: status_text = "Cameras Checked. Video Sync Ready."
    if st.session_state.sim_step == 2: status_text = "Video Pending. Ready for Trigger."
    if st.session_state.sim_step == 3: status_text = "RECORDING IN PROGRESS (Timer Running)..."
    
    st.markdown(f"<div class='sim-screen'>{status_text}</div>", unsafe_allow_html=True)
    
    # Interactive Buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("1. Setup Actions")
        if st.button("👀 Check Camera Positions"):
            if st.session_state.sim_step == 0:
                st.session_state.sim_step = 1
                st.success("Correct! Always check the blue tape first.")
            else:
                st.warning("You already did this.")
                
        if st.button("⌨️ Type 'Record' + Enter"):
            if st.session_state.sim_step == 1:
                st.session_state.sim_step = 2
                st.success("Correct! The system is now 'Pending'. Don't press anything else yet!")
            elif st.session_state.sim_step == 0:
                st.error("WRONG! You forgot to check the camera positions first. The participant walked out of frame!")
            else:
                st.warning("Already done.")

    with col2:
        st.subheader("2. Triggers (Simultaneous)")
        if st.button("🚀 Shift+A & Sync 'Start'"):
            if st.session_state.sim_step == 2:
                st.session_state.sim_step = 3
                st.balloons()
                st.success("PERFECT! You started Equivital and the Sync Timer together.")
            elif st.session_state.sim_step < 2:
                st.error("Too early! You haven't set up the video yet.")
                
        if st.button("🎥 Remote > & Sync 'Start'"):
            st.error("Wrong trigger for this specific task (Walking Baseline). This trigger is for Giladi trials!")

    with col3:
        st.subheader("3. Ending")
        if st.button("🛑 Shift+E & Sync 'End'"):
            if st.session_state.sim_step == 3:
                st.session_state.sim_step = 0
                st.success("Session Saved. Great job!")
            else:
                st.error("You aren't recording yet!")

    if st.button("Reset Simulator"):
        st.session_state.sim_step = 0
        st.experimental_rerun()

# --- MODULE 4: EXAM ---
elif module == "4. Exam: Full Giladi Trial":
    st.title("🔥 The Final Exam: Giladi Protocol")
    st.write("You are in the hot seat. No hints.")
    
    # A simple state machine for the exam
    st.info("Scenario: The participant is standing ready. You need to run **Trial 1** of the Giladi protocol.")
    
    exam_actions = st.multiselect("Select your actions IN ORDER:", 
        ["Press Start on Eqivital", 
         "Check Camera Green Tape", 
         "Check Camera Blue Tape",
         "Type 'Record' in VideoSync", 
         "Press Remote > & Sync App", 
         "Yell 'Go!'"]
    )
    
    if st.button("Submit Exam"):
        correct_order = ["Check Camera Green Tape", "Type 'Record' in VideoSync", "Press Remote > & Sync App"]
        
        if exam_actions == correct_order:
            st.balloons()
            st.success("PASSED! You are ready to run the study.")
        else:
            st.error("FAILED. Review the protocol.")
            st.write(f"You selected: {exam_actions}")
            st.write("Correct Order: Check Green Tape -> Type Record -> Press Remote/Sync Trigger")
