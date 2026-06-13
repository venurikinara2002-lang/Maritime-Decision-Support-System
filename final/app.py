import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor 

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="OceanGuard Optimizer", page_icon="⚓", layout="wide")

# --- PROFESSIONAL MARITIME STYLING ---
st.markdown("""
    <style>
    /* Main Background and Text Color */
    .stApp { background: linear-gradient(to bottom, #001f3f, #0074D9); color: white; }
    
    /* Metric Styling */
    div[data-testid="stMetricValue"] { color: #FFDC00 !important; font-size: 28px; }
    
    /* Headers and Subheaders */
    h1, h2, h3 { color: #7FDBFF !important; }
    
    /* Sidebar and Input Styling */
    .stSelectbox label, .stSlider label, .stNumberInput label { color: #7FDBFF !important; font-weight: bold; }
    
    /* Intro Box Styling */
    .intro-box { 
        background-color: rgba(255, 255, 255, 0.1); 
        padding: 25px; 
        border-radius: 12px; 
        border-left: 6px solid #FF851B; 
        margin-bottom: 25px; 
        line-height: 1.6;
    }

    /* Condition Guide Box */
    .condition-guide {
        background-color: rgba(0, 0, 0, 0.2);
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #7FDBFF;
        margin-top: 15px;
    }
    
    /* Fisherman Alert Box Styling */
    .fisherman-alert { 
        background-color: #FF851B; 
        padding: 20px; 
        border-radius: 12px; 
        color: white; 
        border: 2px solid white; 
        margin-top: 20px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.3);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 1. DATA LOADING & PREPROCESSING ---
@st.cache_data
def load_and_clean_data():
    try:
        df = pd.read_csv("fishing_data.csv") 
        column_mapping = {
            'totalHoursSpent(travelAndfishing)': 'totalHoursSpent',
            'safety': 'safetyCategory',
            'year': 'tripYear',
            'catchWeightOfYellowfinTuna(kg)': 'w_yellowfin',
            'catchWeightOfSkipjack(kg)': 'w_skipjack',
            'catchWeightOfMarlin(kg)': 'w_marlin'
        }
        df.rename(columns=column_mapping, inplace=True, errors='ignore')
        
        def create_sea_condition(data):
            conditions = [
                (data['wave_m'] > 2.0) | (data['wind_kph'] > 30),
                (data['wave_m'] > 1.0) | (data['wind_kph'] > 15)
            ]
            choices = ['Rough', 'Moderate']
            data['seaCondition'] = np.select(conditions, choices, default='Calm')
            return data

        return create_sea_condition(df)
    except Exception:
        return pd.DataFrame()

df = load_and_clean_data()

# --- 2. MODEL TRAINING ---
@st.cache_resource
def train_app_model(data):
    if data.empty: return None
    features = ['engine_hp', 'distance_km', 'allowedOffshoreDays', 'wind_kph', 'wave_m', 'crew_size']
    X = data[features].fillna(0)
    y = np.log1p(data['total_cost_LKR']) 
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model

model = train_app_model(df)

# --- 3. SIDEBAR NAVIGATION ---
st.sidebar.markdown("# ⚓ Navigation Center")
page = st.sidebar.selectbox("Select Station:", ["Fleet Dashboard", "Safety Analytics", "Financial Planner"])

# --- PAGE 1: FLEET DASHBOARD ---
if page == "Fleet Dashboard":
    st.title("Fleet Operations Dashboard")
    
    try:
        st.image("boat_dashboard.png", use_container_width=True)
    except:
        st.info("💡 Tip: Save your boat image as 'boat_dashboard.png' in the same folder as this script.")

    st.markdown("""
    <div class="intro-box">
    <h3>Welcome to OceanGuard Optimizer</h3>
    <p>This professional maritime tool is designed for fishermen to bridge the gap between 
    traditional knowledge and data science. By analyzing historical fleet data, we help you prepare 
    before you leave the harbor.</p>
    <ul>
        <li><b>Safety Checks:</b> Compare your forecasted conditions against fleet limits.</li>
        <li><b>Predictive Costs:</b> Estimate trip expenses based on crew size and vessel specs.</li>
        <li><b>Catch Targeting:</b> Set specific weight goals based on your estimated costs.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    # Metrics Row
    if not df.empty:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Vessels", f"{len(df)}")
        c2.metric("Avg Fuel Cost", f"LKR {df['fuel_cost_LKR'].mean():,.0f}")
        c3.metric("Avg Crew Size", f"{df['crew_size'].mean():.1f}")
        c4.metric("Avg Trip Days", f"{df['allowedOffshoreDays'].mean():.1f}")
    
    st.divider()
    
    col_l, col_r = st.columns([1, 1])
    
    with col_r:
        st.subheader("Live Sea Safety Tester")
        t_wind = st.slider("Current Wind Speed (kph)", 0, 100, 20)
        t_wave = st.slider("Current Wave Height (m)", 0.0, 5.0, 1.0)
        
        if t_wave > 2.0 or t_wind > 30: 
            current_status = 'Rough'
            st.error(f"### STATUS: {current_status} - DEPARTURE NOT RECOMMENDED")
        elif t_wave > 1.0 or t_wind > 15: 
            current_status = 'Moderate'
            st.warning(f"### STATUS: {current_status} - PROCEED WITH CAUTION")
        else: 
            current_status = 'Calm'
            st.success(f"### STATUS: {current_status} - SAFE TO DEPART")

        # --- CONDITION RANGES DISPLAYED UNDER STATUS ---
        st.markdown("""
        <div class="condition-guide">
        <center><b>Condition Reference Guide</b></center><hr style="margin:5px 0; border-color: #7FDBFF;">
        🟢 <b>Calm:</b> Wave < 1.0m & Wind < 15kph<br>
        🟡 <b>Moderate:</b> Wave 1.0-2.0m or Wind 15-30kph<br>
        🔴 <b>Rough:</b> Wave > 2.0m or Wind > 30kph
        </div>
        """, unsafe_allow_html=True)

    with col_l:
        st.subheader("Fleet Condition Distribution")
        if not df.empty:
            sea_dist = df['seaCondition'].value_counts()
            explode = [0.2 if label == current_status else 0 for label in sea_dist.index]
            
            fig1, ax1 = plt.subplots()
            color_map = {'Calm': '#2ECC40', 'Moderate': '#FF851B', 'Rough': '#FF4136'}
            colors = [color_map.get(x, '#7FDBFF') for x in sea_dist.index]
            
            ax1.pie(sea_dist, labels=sea_dist.index, autopct='%1.1f%%', 
                    colors=colors, explode=explode, shadow=True, startangle=140)
            
            fig1.patch.set_facecolor('#001f3f')
            plt.setp(ax1.texts, color="white", fontweight='bold')
            st.pyplot(fig1)

# --- PAGE 2: SAFETY ANALYTICS ---
elif page == "Safety Analytics":
    st.title("Fleet Risk & Catch Analysis")
    
    if not df.empty:
        col_a, col_b = st.columns(2)
        with col_a:
            st.subheader("Historical Safety Rating")
            fig_safe, ax_safe = plt.subplots()
            fig_safe.patch.set_facecolor("#ffffff")
            sns.countplot(data=df, x='safetyCategory', palette="Blues", ax=ax_safe)
            ax_safe.tick_params(colors='black')
            st.pyplot(fig_safe)

        with col_b:
            st.subheader("Crew Size vs. Total Cost")
            fig_crew, ax_crew = plt.subplots()
            fig_crew.patch.set_facecolor("#ffffff")
            sns.barplot(data=df, x='crew_size', y='total_cost_LKR', palette="viridis", ax=ax_crew)
            ax_crew.tick_params(colors='black')
            st.pyplot(fig_crew)

        st.divider()
        st.subheader("Species Weight Distribution (Historical)")
        spec = st.selectbox("Select Species to View Weight Range:", ["w_yellowfin", "w_skipjack", "w_marlin"])
        fig_hist, ax_hist = plt.subplots(figsize=(10, 4))
        fig_hist.patch.set_facecolor("#FFFFFF")
        sns.histplot(df[spec], bins=30, kde=True, color="skyblue", ax=ax_hist)
        ax_hist.tick_params(colors='black')
        st.pyplot(fig_hist)

# --- PAGE 3: FINANCIAL PLANNER ---
elif page == "Financial Planner":
    st.title("Pre-Trip Financial Optimizer")
    
    if model:
        st.subheader("Step 1: Estimate Operational Trip Costs")
        c1, c2, c3 = st.columns(3)
        with c1:
            hp = st.number_input("Engine HP", value=40)
            crew = st.number_input("Crew Size", min_value=1, max_value=20, value=5)
        with c2:
            dist = st.slider("Trip Distance (km)", 0, 500, 100)
            days = st.slider("Duration (Days)", 1, 30, 10)
        with c3:
            wind = st.slider("Expected Wind (kph)", 0, 60, 20)
            wave = st.slider("Expected Waves (m)", 0.0, 4.0, 1.2)
        
        in_row = np.array([[hp, dist, days, wind, wave, crew]])
        pred_cost = np.expm1(model.predict(in_row)[0])
        st.info(f"### Estimated Operational Cost: LKR {pred_cost:,.2f}")

        st.divider()

        st.subheader("Step 2: Calculate Profit Break-Even Point")
        m1, m2, m3 = st.columns(3)
        p_yellow = m1.number_input("Yellowfin Price (LKR/kg)", value=1200)
        p_skip = m2.number_input("Skipjack Price (LKR/kg)", value=850)
        p_marlin = m3.number_input("Marlin Price (LKR/kg)", value=1000)
        
        avg_market_price = (p_yellow + p_skip + p_marlin) / 3
        be_weight = pred_cost / avg_market_price
        
        st.metric("Required Total Catch (kg)", f"{be_weight:.2f} kg")
        
        st.markdown(f"""
        <div class="fisherman-alert">
        <h4>📢 Attention Fisherman:</h4>
        <p style="font-size: 19px;">To cover your estimated operational costs of <b>LKR {pred_cost:,.2f}</b>, 
        your minimum total catch target <b>MUST BE {be_weight:.2f} kg</b> of mixed species.</p>
        <p>Every kilogram caught beyond this target is your profit. Focus your efforts to reach this weight!</p>
        </div>
        """, unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("<br><hr><center>OceanGuard Optimizer | Maritime Analytics | Index: s16919 Venuri Kinara</center>", unsafe_allow_html=True)