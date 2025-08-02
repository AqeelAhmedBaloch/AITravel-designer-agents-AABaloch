import os
import re
import chainlit as cl
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig

# Load environment variables
load_dotenv()

# Initialize Gemini-compatible OpenAI client
client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url=os.getenv("BASE_URL")
)

# Model setup
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client
)

# Runner configuration
config = RunConfig(
    model=model,
    tracing_disabled=True
)

# ---------------------------
# Utility: Convert USD to PKR
# ---------------------------
def convert_usd_to_pkr(text, rate=280):
    """
    Finds $ amounts and converts to PKR using a fixed exchange rate.
    Example: $100 → $100 (PKR 28000)
    """
    def replacer(match):
        usd = float(match.group(1))
        pkr = int(usd * rate)
        return f"${usd:.0f} ({pkr} PKR)"
    
    return re.sub(r"\$(\d+(?:\.\d{1,2})?)", replacer, text)

# ---------------------------
# Agent Definitions
# ---------------------------

# Step 1: Destination Suggestion Agent
destination_agent = Agent(
    name="DestinationAgent",
    instructions="You are a travel assistant. Suggest 1-2 exciting travel destinations based on the user's mood or interest in a friendly and concise way.",
    model=model,
)

# Step 2: Booking Simulation Agent
booking_agent = Agent(
    name="BookingAgent",
    instructions="""
You are a booking assistant. Simulate flight and hotel bookings based on the destination.
DO NOT use actual function names like get_flights() or suggest_hotels(). Just describe:

- Two flights (airline, time, price)
- Two hotels (name, location, rating)

Respond in short, friendly bullet points.
""",
    model=model,
)

# Step 3: Explore Attractions Agent
explore_agent = Agent(
    name="ExploreAgent",
    instructions="Suggest 2 popular attractions and 2 local food items to try at the destination. Keep it short and exciting.",
    model=model,
)

# ---------------------------
# Chainlit Chat Logic
# ---------------------------

@cl.on_chat_start
async def welcome_message():
    await cl.Message(
        content="#### AI Travel Designer Agent by *Aqeel Ahmed Baloch*\n\nWelcome! I’ll help plan your next adventure by coordinating between expert agents.\nJust tell me your **mood** or **interest** (e.g., `relaxing`, `adventure`, `cultural travel`) to get started!"
    ).send()

@cl.on_message
async def handle_user_input(message: cl.Message):
    mood_or_interest = message.content.strip()

    await cl.Message(content=f"✈️ Received: **{mood_or_interest}**\nPlanning your trip...").send()

    # Step 1: Destination suggestion
    await cl.Message(content="🔍 Finding ideal destinations...").send()
    result1 = await Runner.run(destination_agent, input=mood_or_interest, run_config=config)
    destination = result1.final_output.strip()
    await cl.Message(content=f"📍 **Suggested Destination**: {destination}").send()

    # Step 2: Booking simulation
    await cl.Message(content="🛏️ Searching for flights and hotels...").send()
    result2 = await Runner.run(booking_agent, input=destination, run_config=config)
    booking_info = convert_usd_to_pkr(result2.final_output.strip())
    await cl.Message(content=f"📦 **Booking Info**:\n{booking_info}").send()

    # Step 3: Local explore suggestions
    await cl.Message(content="🍽️ Planning local experiences...").send()
    result3 = await Runner.run(explore_agent, input=destination, run_config=config)
    await cl.Message(content=f"🌆 **Explore Suggestions**:\n{result3.final_output.strip()}").send()

    # Final message
    await cl.Message(content="""
✅ **Trip Plan Ready!**

Type another mood or interest to explore more destinations.

Happy travels! 🌍
""").send()
