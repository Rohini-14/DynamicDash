import streamlit as st
from datetime import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="MSME BI Dashboard",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CENTRALIZED STYLING (Apply this to all pages) ---
st.markdown("""
    <style>
        /* Core body and font styles */
        body {
            font-family: 'Inter', sans-serif;
        }

        /* Background */
        [data-testid="stAppViewContainer"] {
            background-color: #0d1117;
            background-image: radial-gradient(at 20% 20%, hsla(212,45%,15%,1) 0px, transparent 50%),
                              radial-gradient(at 80% 80%, hsla(282,35%,15%,1) 0px, transparent 50%);
        }

        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background-color: #0d1117;
            border-right: 1px solid #2a313c;
        }
        .st-emotion-cache-16txtl3 {
            padding: 2rem 1rem;
        }

        /* Headers and titles */
        h1, h2, h3 {
            color: #c9d1d9 !important;
            font-weight: 700;
        }
        .main-title {
            text-align: center;
            font-size: 2.5rem;
            color: #58a6ff !important;
            font-weight: 800;
            margin-bottom: 0.5rem;
        }
        .sub-title {
            text-align: center;
            font-size: 1.1rem;
            color: #8b949e;
            margin-bottom: 2rem;
        }

        /* Card styling */
        .dashboard-card, .step-card {
            background: rgba(13, 17, 23, 0.6);
            border: 1px solid #30363d;
            border-radius: 12px;
            padding: 25px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
            backdrop-filter: blur(4px);
            transition: all 0.3s ease;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        .dashboard-card:hover, .step-card:hover {
            border-color: #58a6ff;
            transform: translateY(-5px);
            box-shadow: 0 12px 40px 0 rgba(0, 119, 255, 0.2);
        }
        .dashboard-card h3 {
            font-size: 1.5rem;
            color: #58a6ff !important;
            margin-bottom: 10px;
        }
        .dashboard-card p {
            color: #8b949e;
            flex-grow: 1;
        }

        /* Button styling */
        .stButton button {
            background: linear-gradient(90deg, #238636, #2ea043);
            color: #ffffff !important;
            font-weight: 600 !important;
            border-radius: 8px !important;
            padding: 12px 30px !important;
            border: 1px solid #2ea043 !important;
            transition: all 0.3s ease !important;
            margin-top: 1rem; /* Add space above the button */
        }
        .stButton button:hover {
            background: linear-gradient(90deg, #2ea043, #238636);
            box-shadow: 0 0 15px rgba(46, 160, 67, 0.5);
            border: 1px solid #3fb950 !important;
        }
        
        /* Specific button for logout in the sidebar */
        [data-testid="stSidebar"] .stButton button {
             background: linear-gradient(90deg, #8B1818, #CF222E);
             border: 1px solid #CF222E !important;
        }
        [data-testid="stSidebar"] .stButton button:hover {
            background: linear-gradient(90deg, #CF222E, #8B1818);
            border: 1px solid #F85149 !important;
        }


        /* Footer styling */
        footer {
            text-align: center;
            color: #8b949e;
            margin-top: 4rem;
            font-size: 0.9rem;
        }
    </style>
""", unsafe_allow_html=True)


# --- SESSION STATE MANAGEMENT ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = ""


# --- LOGIN PAGE ---
if not st.session_state.authenticated:
    st.markdown("<h1 class='main-title'>💼 MSME Business Intelligence Hub</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-title'>Log in to unlock data-driven insights for your business.</p>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        with st.container():
            st.markdown("""
                <div style="background: rgba(13, 17, 23, 0.6); border: 1px solid #30363d; border-radius: 12px; padding: 30px; box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37); backdrop-filter: blur(4px);">
                    <h3 style="text-align: center;">Secure Login</h3>
            """, unsafe_allow_html=True)
            
            username = st.text_input("👤 Username", key="login_username")
            password = st.text_input("🔑 Password", type="password", key="login_password")
            
            st.write("") # Spacer
            login_button = st.button("Login", use_container_width=True)
            
            st.markdown("</div>", unsafe_allow_html=True)

            if login_button:
                # Use a simple authentication check for this example
                if username and password:
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.rerun()
                else:
                    st.error("Please enter both username and password.")

# --- MAIN DASHBOARD HOME PAGE (After Login) ---
else:
    # --- HEADER ---
    st.markdown(f"<h1 class='main-title'>Welcome, {st.session_state.username}!</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-title'>Your central hub for business analytics and insights.</p>", unsafe_allow_html=True)
    st.markdown("<hr style='border: 1px solid #30363d;'>", unsafe_allow_html=True)

    # --- GUIDED WORKFLOW SECTION ---
    st.subheader("🚀 Getting Started: Your Path to Insights")
    st.write("Follow this guided workflow to leverage the full power of your data.")

    step_cols = st.columns(4, gap="large")
    steps = [
        {"icon": "📤", "title": "1. Upload & Clean", "desc": "Start by uploading your sales data. The system supports CSV and Excel files and helps you prepare them for analysis."},
        {"icon": "📊", "title": "2. Visualize Insights", "desc": "Explore your data through interactive charts. Identify trends and key performance indicators in the main dashboard."},
        {"icon": "🤖", "title": "3. Get AI Predictions", "desc": "Leverage our AI to forecast future sales and get intelligent recommendations to guide your business strategy."},
        {"icon": "📄", "title": "4. Export Reports", "desc": "Generate and download professional PDF reports of your findings to share with your team and stakeholders."}
    ]
    
    for i, step in enumerate(steps):
        with step_cols[i]:
            st.markdown(f"""
                <div class='step-card'>
                    <h3 style='font-size: 1.8rem; text-align: center;'>{step['icon']}</h3>
                    <h4 style='text-align: center; color: #c9d1d9 !important;'>{step['title']}</h4>
                    <p style='font-size: 0.9rem; color: #8b949e; text-align: center;'>{step['desc']}</p>
                </div>
            """, unsafe_allow_html=True)


    st.markdown("<br><hr style='border: 1px solid #30363d;'><br>", unsafe_allow_html=True)

    # --- NAVIGATION CARDS SECTION ---
    st.subheader("🛠️ Your BI Toolkit")
    st.write("Jump directly into any section of your dashboard.")

    # --- FIX: Expanded this section to include all pages for direct navigation ---
    card_cols_1 = st.columns(3, gap="large")
    card_cols_2 = st.columns(3, gap="large")
    
    # Row 1
    with card_cols_1[0]:
        st.markdown("""
            <div class='dashboard-card'>
                <div>
                    <h3>📤 Upload Data</h3>
                    <p>Upload, clean, and preprocess your raw business data before analysis.</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Go to Upload", key="nav_upload", use_container_width=True):
            st.switch_page("pages/1_Upload_Preprocess.py")

    with card_cols_1[1]:
        st.markdown("""
            <div class='dashboard-card'>
                <div>
                    <h3>📊 Interactive Dashboard</h3>
                    <p>Dive deep into your data with a fully interactive analytics dashboard.</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Explore Dashboard", key="nav_dashboard", use_container_width=True):
            st.switch_page("pages/2_Dashboard.py")
            
    with card_cols_1[2]:
        st.markdown("""
            <div class='dashboard-card'>
                <div>
                    <h3>🤖 AI Predictive Analysis</h3>
                    <p>Use our AI models to forecast sales trends and guide your business strategy.</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Go to AI Predictive", key="nav_ai", use_container_width=True):
            st.switch_page("pages/3_AI_Predictive.py")

    # Row 2
    with card_cols_2[0]:
        st.markdown("""
            <div class='dashboard-card'>
                <div>
                    <h3>💡 AI Suggestions</h3>
                    <p>Get actionable, AI-powered advice to improve sales and profitability.</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Get AI Suggestions", key="nav_suggestions", use_container_width=True):
            st.switch_page("pages/4_AI_Suggestions.py")

    with card_cols_2[1]:
        st.markdown("""
            <div class='dashboard-card'>
                <div>
                    <h3>📄 Reports & Export</h3>
                    <p>Generate and download professional PDF reports of your findings.</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Go to Reports", key="nav_reports", use_container_width=True):
            st.switch_page("pages/5_Reports_Export.py")
            
    with card_cols_2[2]:
        st.markdown("""
            <div class='dashboard-card'>
                <div>
                    <h3>⚙️ Admin Panel</h3>
                    <p>Manage application settings, user access, and system configurations.</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Go to Admin Panel", key="nav_admin", use_container_width=True):
            st.switch_page("pages/6_Admin.py")

    # --- SIDEBAR LOGOUT ---
    with st.sidebar:
        st.header(f"Welcome, {st.session_state.username}!")
        st.write("You are logged in.")
        if st.button("Logout", key="logout_sidebar", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.username = ""
            st.rerun()

    # --- FOOTER ---
    st.markdown(f"""
        <footer>
            <hr style='border: 1px solid #30363d;'>
            <p>© {datetime.now().year} MSME BI Hub | Empowering Your Business with Data</p>
        </footer>
    """, unsafe_allow_html=True)
