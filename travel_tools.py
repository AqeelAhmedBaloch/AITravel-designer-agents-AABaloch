# travel_tools.py
from agents import function_tool

@function_tool
def get_flights(destination: str) -> str:
    return f"Searching for flights to {destination}: PKR 46,000 - PKR 78,000"

@function_tool
def suggest_hotels(destination: str) -> str:
    return f"Suggesting hotels in {destination}: Pearl Continental, Serena Hotel, and Marriott Hotel"