from __future__ import annotations
import os
import threading
import pandas as pd
import re
from datetime import datetime
from typing import Any, Text, Dict, List, Optional
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from openai import OpenAI
import gspread
from oauth2client.service_account import ServiceAccountCredentials


# Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or "AIzaSyAb0RJRSMRheme0Ab2aoNKvm9i3n6Noin4"
EXCEL_FILE_PATH = os.getenv("EXCEL_FILE_PATH") or "actions/Sample.xlsx"

# Gemini Client
gemini_client = OpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


# ---------------- Excel Handler ---------------- #
class ExcelDataHandler:
    def __init__(self, sheet_id: str, sheet_name: str):
        self.sheet_id = sheet_id
        self.sheet_name = sheet_name
        self.data = pd.DataFrame()
        self._load_data()
        self._start_refresh()

    def _load_data(self):
        try:
            scope = ['https://spreadsheets.google.com/feeds',
                     'https://www.googleapis.com/auth/spreadsheets',
                     'https://www.googleapis.com/auth/drive.file',
                     'https://www.googleapis.com/auth/drive']

            creds = ServiceAccountCredentials.from_json_keyfile_name("actions/service_account.json", scope)
            client = gspread.authorize(creds)

            sheet = client.open_by_key(self.sheet_id).worksheet(self.sheet_name)
            records = sheet.get_all_records()
            self.data = pd.DataFrame.from_records(records)
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ Google Sheet refreshed: {len(self.data)} rows")
        except Exception as e:
            print(f"⚠️ Error loading Excel: {e}")

    def _start_refresh(self):
        def refresh():
           # self._load_data()
            threading.Timer(10, refresh).start()
        refresh()

    def get_preview(self, full: bool = False) -> str:
     self._load_data()
     return self.data.to_string(index=False) if full else self.data.head(50).to_string(index=False)


# ---------------- Response Pipeline ---------------- #
class ResponsePipeline:
    def __init__(self):
        self.sheet_id = os.getenv("SHEET_ID") or "1ONM8_0qEXfIgqknkqljzU1b_ebyCmZDvWm0hUuL4pzY"
        self.sheet_name = os.getenv("SHEET_NAME") or "Sheet1"
        self.excel_handler = ExcelDataHandler(self.sheet_id, self.sheet_name)
        self.initialized = False
        self.conversation_history: List[Dict[str, str]] = []

    def process_query(self, query: str) -> str:
        query = query.strip()
        if not query:
            return "Please provide a valid question."

        if not self.initialized:
            return self._start_with_excel(query)

        return self._continue_with_history(query)

    def _start_with_excel(self, query: str) -> str:
        excel_preview = self.excel_handler.get_preview(full=True)  # Send all rows
        print("\n=== ✅ DATA SENT TO GEMINI ===")
        print(excel_preview)
        print("================================\n")
        self.conversation_history = [
            {"role": "system", "content": "You are a helpful assistant using this Excel data to answer user queries and your company name was Only Skill and you are developed by J Sanjay Ram and your name was Qbee."},
            {"role": "user", "content": f"Here is the full Excel data:\n{excel_preview}\n\nUser asked: {query}"}
        ]
        self.initialized = True
        return self._get_llm_response()

    def _continue_with_history(self, query: str) -> str:
        self.conversation_history.append({"role": "user", "content": query})
        return self._get_llm_response()

    def _get_llm_response(self) -> str:
        try:
            response = gemini_client.chat.completions.create(
                model="gemini-2.0-flash",
                messages=self.conversation_history,
                max_tokens=300
            )
            reply = response.choices[0].message.content.strip()
            self.conversation_history.append({"role": "assistant", "content": reply})
            return reply
        except Exception as e:
            print("⚠️ Gemini error:", e)
            return "Sorry, I'm having trouble responding right now."


# Shared pipeline instance
response_pipeline = ResponsePipeline()


# ---------------- Rasa Custom Actions ---------------- #
class ActionExcelQuery(Action):
    def name(self) -> Text:
        return "action_excel_query"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        user_message = tracker.latest_message.get("text")
        response = response_pipeline.process_query(user_message)
        dispatcher.utter_message(text=response)
        return []


class ActionGeneralQuery(Action):
    def name(self) -> Text:
        return "action_general_query"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        user_message = tracker.latest_message.get("text")
        response = response_pipeline.process_query(user_message)
        dispatcher.utter_message(text=response)
        return []


class ActionFallback(Action):
    def name(self) -> Text:
        return "action_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(text="Sorry, I didn’t understand that. Could you rephrase?")
        return []
