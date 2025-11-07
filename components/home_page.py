# components/home_page.py

import streamlit as st
import pandas as pd
from database.db_functions import get_data

def render_home_page():
    """
    Displays the main home page content:
    - Header
    - Unsplash banner image
    - Three value proposition cards in columns
    """
    st.session_state  # Ensure session state is accessible

    # Header
    st.title("Welcome to AgroConnect 🌱")
    st.write(
        "Your smart agriculture companion: connect with farmers, explore crops, and make data-driven decisions!"
    )

    # Banner Image
    st.image(
        "https://images.unsplash.com/photo-1599759805137-c15e8d7a7a06?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=1200",
        use_column_width=True
    )

    # Value Proposition Cards
    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("📈 **Data-Driven Insights**\nGet real-time crop and market data to make informed decisions.")
    with col2:
        st.success("🤝 **Connect with Farmers**\nEasily discover and collaborate with local farmers and suppliers.")
    with col3:
        st.warning("🌱 **Sustainable Practices**\nPromote eco-friendly and climate-smart agricultural methods.")


def render_db_check():
    """
    Displays a read-only view of the 'tools' and 'crops' tables.
    Uses tabs for each table and shows success/error messages with record counts.
    """
    st.session_state  # Ensure session state is accessible

    # Tabs for tools and crops
    tab_tools, tab_crops = st.tabs(["Tools Table", "Crops Table"])

    # Tools Table
    with tab_tools:
        try:
            tools_df = get_data("tools")
            if tools_df.empty:
                st.warning("No records found in the 'tools' table.")
            else:
                st.dataframe(tools_df)
                st.success(f"Loaded {len(tools_df)} records from 'tools'.")
        except Exception as e:
            st.error(f"Error loading 'tools' table: {e}")

    # Crops Table
    with tab_crops:
        try:
            crops_df = get_data("crops")
            if crops_df.empty:
                st.warning("No records found in the 'crops' table.")
            else:
                st.dataframe(crops_df)
                st.success(f"Loaded {len(crops_df)} records from 'crops'.")
        except Exception as e:
            st.error(f"Error loading 'crops' table: {e}")
