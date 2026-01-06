import streamlit as st
import pandas as pd
import time

# --- APP CONFIGURATION ---
st.set_page_config(
    page_title="Lab Commander Training",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS FOR "COURSE" FEEL ---
st.markdown("""
    <style>
    .main-header { font-size: 32px; font-weight: bold; color: #2E86C1; margin-bottom: 20px; }
    .sub-header { font-size: 24px; font-weight: bold; color: #2874A6; margin-top: 20px; }
    .instruction-box { background-color: #f4f6f9; border-left: 5px solid #2E86C1; padding: 15px; margin: 10px 0; }
    .warning-box { background-color: #fff5f5; border-left: 5px solid #c53030; padding: 15px; margin: 10px 0; }
    .success-box { background-color: #f0fff4; border-left: 5px solid #38a169; padding: 15px; margin: 10px 0; }
    .sim-button { width: 100%; height: 60px; font-weight: bold; font-size: 18px; }
    </style>
""", unsafe_allow_html=True)

# --- SESSION STATE MANAGEMENT ---
if 'progress' not in st.session_state:
    st.session_state.progress = {
        "setup": False,
        "baseline": False,
        "giladi": False,
        "vr": False
    }

# --- HELPER FUNCTIONS ---
def mark_complete(module):
    st.session_state.progress[module] = True
    st.balloons()
    st.success(f"✅ Module '{module.capitalize()}' Complete! Move to the next section.")

def check_dual_hand(left_action, right_action, expected_left, expected_right, feedback_success):
    if left_action == expected_left and right_action == expected_right:
        st.markdown(f"<div class='success-box'><b>CORRECT!</b> {feedback_success}</div>", unsafe_allow_html=True)
        return True
    else:
        st.markdown(f"<div class='warning-box'><b>INCORRECT.</b><br>You selected: Left='{left_action}' | Right='{right_action}'<br>Expected: Left='{expected_left}' | Right='{expected_right}'</div>", unsafe_allow_html=True)
        return False

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("🧪 Lab Academy")
st.sidebar.write("Welcome, Trainee.")
st.sidebar.progress(sum(st.session_state.progress.values()) / 4)

menu = st.sidebar.radio("Course Modules:", [
    "1. Hardware & Setup",
    "2. Baseline Protocols",
    "3. Giladi Protocols",
    "4. VR Protocols",
    "5. Final Review"
])

# ==========================================
# MODULE 1: HARDWARE & SETUP
# ==========================================
if menu == "1. Hardware & Setup":
    st.markdown("<div class='main-header'>Module 1: The Setup</div>", unsafe_allow_html=True)
    st.write("Before we test a patient, we must build the lab. Follow the steps below.")

    tab1, tab2, tab3, tab4 = st.tabs(["🔵 OPAL Sensors", "🔴 GoPros", "🟢 Equivital", "💾 MobilityLab"])

    with tab1:
        st.markdown("### Setting up the OPALs")
        st.image("https://support.apdm.com/hc/article_attachments/360000085206/Opals_in_Dock.png", caption="OPAL Docking Station", width=400)
        st.info("Goal: 5 Sensors (2 Shins, 2 Feet, 1 Lower Back).")
        
        check_1 = st.checkbox("Plug Access Point into Stand & Dock")
        check_2 = st.checkbox("Plug Power Cord to Wall")
        check_3 = st.checkbox("Sensors are flashing GREEN (Charged)")
        check_4 = st.checkbox("Remote is plugged into computer & Switch is ON (Green)")
        
        if check_1 and check_2 and check_3 and check_4:
            st.success("OPAL Hardware Ready!")

    with tab2:
        st.markdown("### Setting up the GoPros")
        st.warning("⚠️ CRITICAL: Always pair in the app BEFORE placing cameras on tripods.")
        
        st.markdown("""
        1. Turn on Cameras (Frontal & Sagittal).
        2. Swipe Down -> Left -> **"Pair Device"**.
        3. Open **GoProSync App** on Desktop.
        4. Type `Connect` (Case Sensitive!) -> Enter.
        5. Type `All` -> Enter.
        6. Listen for the **BEEP**.
        7. Type `Record` -> Enter (Wait for pending message).
        """)
        
        q_gopro = st.radio("What must you do immediately after the app finds the cameras?", 
                           ["Put them on tripods", "Type 'All' to connect", "Start recording"], index=None)
        if q_gopro == "Type 'All' to connect":
            st.success("Correct.")

    with tab3:
        st.markdown("### Setting up Equivital")
        st.markdown("""
        1. Connect SEM to Laptop via USB.
        2. **Equivital Manager:** 'SEM Configuration' -> Apply.
        3. **LabChart:** Open Template -> Click 'Don't Load' (3x).
        4. Wait for Serial Number pop-up -> OK.
        5. **File -> Save As...** (Use Naming Convention).
        6. Unplug SEM -> Put in Belt -> Put on Patient.
        """)

    with tab4:
        st.markdown("### MobilityLab Config")
        st.markdown("""
        1. Open App -> Configure Hardware -> Rescan.
        2. **Subjects Tab:** +New Subject -> Enter Details -> Save.
        3. **New Test:** Select `PD_HRV`.
        4. **Outfitting:** Place sensors on patient (Shins, Feet, Sacrum).
        """)
        
        if st.button("I have completed all setup steps"):
            mark_complete("setup")

# ==========================================
# MODULE 2: BASELINE
# ==========================================
elif menu == "2. Baseline Protocols":
    st.markdown("<div class='main-header'>Module 2: Baseline Measurements</div>", unsafe_allow_html=True)
    st.write("We measure the patient in 3 states: Sitting, Standing, Walking (5 mins each).")
    
    st.markdown("<div class='instruction-box'>🧠 <b>The Concept: Simultaneous Triggers</b><br>We have 3 computers. You must start them at the EXACT same time using two hands.</div>", unsafe_allow_html=True)

    # --- SIMULATOR SECTION ---
    st.markdown("### 🎮 Simulation: The 5-Minute Walk")
    st.write("Imagine you are about to start the Walking Baseline. Configure your hands:")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### ✋ Left Hand (Equivital)")
        left_hand = st.selectbox("Select Action:", ["(Nothing)", "Shift + A", "Shift + E", "Shift + S", "Remote >"], key="base_L")
    with col2:
        st.markdown("### ✋ Right Hand (Tablet)")
        right_hand = st.selectbox("Select Action:", ["(Nothing)", "Start 5 min Sitting", "Start 5 min Walk", "End 5 min Walk", "Start 2 min Walk"], key="base_R")

    st.markdown("**Context:** You are starting the **WALKING** baseline.")
    
    if st.button("💥 EXECUTE SIMULTANEOUS PRESS", key="btn_base"):
        # Logic: Baseline Walking Start = Shift+A & Start 5 min Walk
        # Note: Script says Shift+A is for Baseline. 
        if check_dual_hand(left_hand, right_hand, "Shift + A", "Start 5 min Walk", "You started the Equivital and the Sync Timer together."):
            st.markdown("...5 Minutes Later...")
            st.info("Now STOP the trial.")
            # Challenge them to stop it
            mark_complete("baseline")

    st.markdown("---")
    st.markdown("### 📷 Camera Check")
    cam_pos = st.radio("Where do the cameras go for the Walking Baseline?", 
                       ["Green Tape (Whiteboard)", "Blue Mark (Entry/Gait Carpet)"], horizontal=True)
    if cam_pos == "Blue Mark (Entry/Gait Carpet)":
        st.success("Correct. Always Blue for Baseline.")
    elif cam_pos:
        st.error("Wrong. Green is for Giladi.")

# ==========================================
# MODULE 3: GILADI PROTOCOL
# ==========================================
elif menu == "3. Giladi Protocols":
    st.markdown("<div class='main-header'>Module 3: The Giladi Protocol</div>", unsafe_allow_html=True)
    st.markdown("This involves 8 specific trials. The trigger logic changes here!")
    
    st.warning("⚠️ **Camera Change:** Move cameras to **GREEN TAPE** (Whiteboard + Window).")

    st.markdown("### The Workflow Loop")
    st.code("""
    1. VideoSync: Recall 'Record' -> Enter.
    2. MobilityLab: Wait for instruction.
    3. TRIGGER START (Remote + Tablet).
    4. Wait for completion.
    5. TRIGGER END (Remote + Tablet).
    """)

    st.markdown("### 🎮 Simulation: Starting a Trial")
    st.write("The Investigator says: *'Any time after the BEEP'*.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### ✋ Left Hand (Remote)")
        gl_left = st.selectbox("Select Action:", ["(Nothing)", "Shift + A", "Remote > (Slide Forward)", "Shift + S"], key="gl_L")
    with col2:
        st.markdown("### ✋ Right Hand (Tablet)")
        gl_right = st.selectbox("Select Action:", ["(Nothing)", "Start", "Stop", "Record"], key="gl_R")

    if st.button("💥 EXECUTE TRIGGER", key="btn_gl"):
        if check_dual_hand(gl_left, gl_right, "Remote > (Slide Forward)", "Start", "Beep sound occurs. Recording started."):
            st.success("Great work.")
            mark_complete("giladi")

    st.markdown("### 🚪 The Trial 8 Trap")
    st.write("Trial 8 is the 'Doorway Trial'. What must you do differently?")
    t8_ans = st.radio("Action:", ["Nothing", "Move Frontal Camera to Green Tape inside room", "Change sensors"], index=None)
    if t8_ans == "Move Frontal Camera to Green Tape inside room":
        st.success("Correct. Don't forget this move!")

# ==========================================
# MODULE 4: VR PROTOCOLS
# ==========================================
elif menu == "4. VR Protocols":
    st.markdown("<div class='main-header'>Module 4: VR Familiarization & Repo</div>", unsafe_allow_html=True)
    st.write("The participant is now wearing the VR headset. The commands change again.")

    tab_vr1, tab_vr2 = st.tabs(["Familiarization (Sit/Stand/Walk)", "Repositioned (30s)"])

    with tab_vr1:
        st.markdown("### Familiarization Phase")
        st.info("Sequence: 2 min Sit -> 2 min Stand -> 2 min Walk")
        
        st.markdown("**Command Rule:** For VR Fam, we mostly use `Shift + S` on Equivital.")
        
        st.markdown("#### 🎮 Simulation: VR Walking Start")
        st.write("Prepare to start the 2-min VR Walk.")
        
        vr_l = st.selectbox("Left Hand:", ["Shift + A", "Shift + S", "Shift + W"], key="vr_L")
        vr_r = st.selectbox("Right Hand:", ["Start 2 min Sitting", "Start 2 min Walk"], key="vr_R")
        
        if st.button("💥 EXECUTE VR START", key="btn_vr"):
            # Based on script: "Simultaneously press [Shift + S] & 'Start 2 min sitting'" 
            # (Note: User script had a typo saying 'Sitting' for the walk phase, 
            # but usually we want to log 'Walk'. I will look for 'Walk' to be safe, or 'Sit' if adhering strictly).
            # Let's adhere to the LIKELY INTENT which is 'Start 2 min Walk'.
            
            if check_dual_hand(vr_l, vr_r, "Shift + S", "Start 2 min Walk", "Correct. Note: Ensure you press the 'Walk' button on tablet!"):
                pass

    with tab_vr2:
        st.markdown("### Repositioned Trial (30s)")
        st.error("⚠️ Cameras back to BLUE MARKINGS.")
        
        st.markdown("""
        1. **PKMAS Start:** Press Start on PKMAS + Right Arrow on Remote.
        2. **Verbal:** Say "Starting 30s".
        3. **Equivital:** Shift + S (Sit) -> Wait 30s.
        4. **Transition:** SyncApp Stop -> SyncApp Start + Shift + W (Walk).
        """)
        
        if st.button("I understand the 30s protocol"):
            mark_complete("vr")

# ==========================================
# FINAL REVIEW
# ==========================================
elif menu == "5. Final Review":
    st.title("🎓 Certification")
    
    if all(st.session_state.progress.values()):
        st.balloons()
        st.markdown("""
        <div class='success-box'>
        <h2>🎉 CONGRATULATIONS!</h2>
        You have completed the Lab Commander Training Course.<br>
        You are now ready to operate the:
        <ul>
        <li>Equivital (Shift+A / Shift+S)</li>
        <li>MobilityLab & Video Sync</li>
        <li>Dual-Hand Triggers</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("You have not completed all modules yet. Please go back and finish the checklists/simulations.")
        st.write(st.session_state.progress)
