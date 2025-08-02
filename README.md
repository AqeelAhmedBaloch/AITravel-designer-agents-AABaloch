# 🧳 AI Travel Designer Agents

**AI Travel Designer** is an intelligent, multi-agent system that helps users create personalized travel plans. It uses LLM-based agents to suggest destinations, itineraries, budgets, and more — all through interactive conversations. Built using **Chainlit**, **OpenAI Agent SDK**, and modular agent design.

## 🌍 What It Does

- 🧠 **TravelAgent**: Understands user preferences and trip details.
- 📍 **DestinationAgent**: Suggests ideal destinations.
- 📅 **PlannerAgent**: Builds day-wise travel itineraries.
- 💰 **BudgetAgent**: Estimates and optimizes travel costs.
- 💬 Interactive storytelling and planning in a chat interface.
- 🔧 Uses tools like:
  - `get_flight_estimates()`
  - `get_destination_info()`
  - `get_budget_breakdown()`

---

## 🚀 Getting Started

### 📦 Prerequisites

- Python 3.10+
- [Poetry](https://python-poetry.org/docs/#installation)
- OpenAI API Key (or compatible proxy)
- Node.js (optional, for Chainlit UI)

### 🔧 Installation

```bash
git clone https://github.com/AqeelAhmedBaloch/AITravel-designer-agents-AABaloch.git
cd AITravel-designer-agents-AABaloch
poetry install
