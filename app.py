import streamlit as st
import pandas as pd
from datetime import date
from dotenv import load_dotenv # <-- NEW: Used to load the .env file
import os

# Load environment variables from the .env file immediately
load_dotenv()

# ----------------------------------------
# --- 0. MODULE IMPORTS ---
# ----------------------------------------
from database.db_functions import init_db, get_data, add_data 
from components.home_page import render_home_page, render_db_check
from components.tool_listings import render_tool_listing, render_tool_management
from components.crop_listings import render_crop_listing, render_crop_management

# ----------------------------------------
# --- CONFIGURATION AND SETUP ---
# ----------------------------------------

# 1. Database Initialization
if 'db_initialized' not in st.session_state:
    init_db()
    st.session_state.db_initialized = True

# 2. Page Config
st.set_page_config(page_title="Smart Farmer Marketplace", page_icon="🌾", layout="wide")

# 3. Custom CSS for styling
st.markdown(
    """
    <style>
    body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    h1,h2,h3 { color:#006400; text-align:center; font-weight:700; }
    [data-testid="stSidebar"] { background-color:#f0fff0; border-right:4px solid #3CB371; padding-top:20px; }
    
    /* Button Styling */
    .stButton>button { 
        background-color:#3CB371; color:white; border-radius:8px; padding:8px 16px; font-weight:bold; border:none; 
        box-shadow:0 2px 4px rgba(0,0,0,0.15); width:100%; transition:0.3s; 
    }
    .stButton>button:hover { 
        background-color:#2E8B57; box-shadow:0 4px 8px rgba(0,0,0,0.25); 
    }
    
    /* Card Styling */
    .card { 
        background-color:#ffffff; padding:25px; margin-bottom:20px; border-radius:12px; 
        box-shadow:0 6px 10px rgba(0,0,0,0.1); border-left:5px solid #3CB371; 
    }
    
    footer { visibility:hidden; }
    .stDataFrame, .stDataEditor { border:1px solid #3CB371; border-radius:8px; padding:5px; }
    </style>
    """,
    unsafe_allow_html=True
)

# 4. Persistent Database Loading
st.session_state.tools = get_data("tools")
st.session_state.crops = get_data("crops")


# ----------------------------------------
# --- USER LOGIN (Simple Farmer Identification) ---
# ----------------------------------------
st.sidebar.header("👨‍🌾 Farmer Login")

farmer_name = st.sidebar.text_input("Enter your name to manage listings", key="login_name").strip()

if farmer_name:
    st.session_state.farmer_name = farmer_name


# ----------------------------------------
# --- MAIN APPLICATION LOGIC ---
# ----------------------------------------
st.title("🌾 SMART FARMER MARKETPLACE")

st.markdown("""
<div style='background-color:#ccffcc;padding:12px;border-radius:10px;text-align:center;margin-bottom:20px;border: 1px dashed #3CB371;'>
    <h3>🚜 Empowering Farmers • Connecting Communities • Boosting Rural Economy 🌿</h3>
</div>
""", unsafe_allow_html=True)

menu = st.sidebar.radio(
    "📋 MARKETPLACE MENU", 
    ["🏠 Home", "📝 New Listing", "🔍 View Listings & Manage", "💾 Database Check (Admin)"]
)

# ----------------------------------------
# --- PAGE ROUTING ---
# ----------------------------------------

if menu == "🏠 Home":
    render_home_page()
    
elif menu == "📝 New Listing":
    st.header("✍️ Create a New Marketplace Listing")
    tab_tool, tab_crop = st.tabs(["🧰 List a Tool for Rent", "🌾 List a Crop for Sale"])
    
    with tab_tool:
        render_tool_listing(st.session_state.get("farmer_name", ""))
    with tab_crop:
        render_crop_listing(st.session_state.get("farmer_name", ""))

elif menu == "🔍 View Listings & Manage":
    st.header("🔍 All Active Listings & Management")
    tab1, tab2 = st.tabs(["🧰 Tools for Rent", "🌾 Crops for Sale"])

    with tab1:
        render_tool_management(st.session_state.tools, st.session_state.get("farmer_name", None))
    with tab2:
        render_crop_management(st.session_state.crops, st.session_state.get("farmer_name", None))

elif menu == "💾 Database Check (Admin)":
    render_db_check()
    
# ----------------------------------------
# --- FOOTER ---
# ----------------------------------------
st.markdown("""
<hr style='border-top: 2px solid #3CB371; margin-top: 30px;'>
<div style='text-align:center;color:#696969;padding:10px;'>
    <small>© 2025 Smart Farmer Marketplace | Prototype by Team AgroLink</small>
</div>
""", unsafe_allow_html=True)