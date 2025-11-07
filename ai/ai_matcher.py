# ai/ai_matcher.py

import os
import sqlite3
import pandas as pd
import google.generativeai as genai

# --- Initialize Gemini AI Client ---
client_available = False
try:
    API_KEY = os.environ['GEMINI_API_KEY']
    genai.configure(api_key=API_KEY)
    client_available = True
except KeyError:
    client_available = False
    print("Warning: GEMINI_API_KEY not found. AI suggestions will be unavailable.")

DB_NAME = "farmermarket.db"


def fetch_recent_data():
    """
    Fetch recent data from the SQLite database.
    Returns a dictionary containing 'tools' and 'crops' DataFrames.
    """
    conn = sqlite3.connect(DB_NAME)
    try:
        tools_df = pd.read_sql_query("SELECT * FROM tools ORDER BY id DESC LIMIT 10", conn)
        crops_df = pd.read_sql_query("SELECT * FROM crops ORDER BY id DESC LIMIT 10", conn)
    except Exception as e:
        print(f"Error fetching data from DB: {e}")
        tools_df = pd.DataFrame()
        crops_df = pd.DataFrame()
    finally:
        conn.close()

    return {
        "tools": tools_df,
        "crops": crops_df
    }


def get_recommendations(context: dict):
    """
    Generate AI-powered marketplace recommendations based on context and recent DB data.
    Returns a string with suggestions or a fixed error message if AI is unavailable.
    
    :param context: Dictionary containing user context or preferences.
    """
    if not client_available:
        return "(AI suggestion unavailable: GEMINI_API_KEY is not set.)"

    # Fetch recent database data
    recent_data = fetch_recent_data()

    # Prepare prompt for the AI model
    prompt = (
        "You are an AI assistant for an agricultural marketplace. "
        "Based on the following context and recent database information, provide actionable recommendations:\n\n"
        f"Context: {context}\n\n"
        f"Recent Tools: {recent_data['tools'].to_dict(orient='records')}\n"
        f"Recent Crops: {recent_data['crops'].to_dict(orient='records')}\n\n"
        "Provide concise and practical suggestions."
    )

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate(prompt=prompt)
        return response.result
    except Exception as e:
        return f"(AI suggestion unavailable due to an error: {e})"
