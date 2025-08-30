
import os
import chainlit as cl
from typing import cast
from dotenv import load_dotenv
from openai import OpenAI
from agents import Agent, Runner, RunConfig, handoff, AsyncOpenAI, OpenAIChatCompletionsModel, Tool

load_dotenv()


# ---------------------------
#  Configuration Setup
# ---------------------------
def setup_config():
    # External Gemini client
    external_client = AsyncOpenAI(
        api_key=os.getenv("GEMINI_API_KEY"),
        base_url=os.getenv("BASE_URL"),
    )

    model = OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=external_client,
    )

    config = RunConfig(
        model=model,
        model_provider=external_client,
        tracing_disabled=True
    )

    # ---------------------------
    #  Agents
    # ---------------------------
    destination_agent = Agent(
        name="destination_agent",
        instructions="You help users find destinations based on preferences.",
        handoff_description="Destination finder agent",
        model=model,
    )

    booking_agent = Agent(
        name="booking_agent",
        instructions="You handle travel bookings (flights, hotels, cars).",
        handoff_description="Booking manager agent",
        model=model,

    )

    explore_agent = Agent(
        name="explore_agent",
        instructions="You suggest attractions, food, and experiences in a location.",
        handoff_description="Attraction and food suggestion agent",
        model=model
    )

    triage_agent = Agent(
        name="triage_agent",
        instructions=(
            "You triage travel-related queries to the right agent. "
            "If multiple agents are needed, call them in the right order. "
            "Always use provided tools for flights/hotels, never fetch them yourself."
        ),
        handoffs=[
            handoff(destination_agent),
            handoff(booking_agent),
            handoff(explore_agent)
        ],
        model=model
    )

    return triage_agent, config


# ---------------------------
#  Chainlit Events
# ---------------------------
@cl.on_chat_start
async def start():
    triage_agent, config = setup_config()

    cl.user_session.set("triage_agent", triage_agent)
    cl.user_session.set("config", config)
    cl.user_session.set("chat_history", [])

    await cl.Message(content="🌍 Welcome to AI Travel Designer Agent!(Aqeel Ahmed Baloch)").send()


@cl.on_message
async def main(message: cl.Message):
    msg = cl.Message(content="✈️ Thinking...")
    await msg.send()

    triage_agent = cast(Agent, cl.user_session.get("triage_agent"))
    config = cast(RunConfig, cl.user_session.get("config"))
    history = cl.user_session.get("chat_history") or []

    history.append({"role": "user", "content": message.content})

    # Run the triage agent
    result = await Runner.run(triage_agent, history, run_config=config)

    # Get and send final output
    response_content = result.final_output
    msg.content = response_content
    await msg.update()

    # Save chat history
    history.append({"role": "assistant", "content": response_content})
    cl.user_session.set("chat_history", history)