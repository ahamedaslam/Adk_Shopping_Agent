 # ADK Shopping Agent

Lightweight demo of a modular shopping assistant built with the Google ADK agent primitives. This repository contains small LLM agents that demonstrate a multi-agent ecommerce workflow (catalog browsing, checkout, and order summary).

**Status:** Minimal demo — intended for learning and local experimentation.

**Key points:**
- Uses `google-adk` agent primitives and simple in-memory session state.
- No persistent database; state is stored in the agent `ToolContext` during a session.
- Demo catalog is hard-coded for easy offline experimentation.

**Table of contents**
- Installation
- Quick start
- Project structure
- How the agents interact (workflow)
- Extending the demo
- Notes

## Installation

Prerequisites:
- Python 3.10+
- An account and credentials if you plan to call real LLM APIs (not required for the local demo)

Create and activate a virtual environment (Windows example):

```powershell
python -m venv venv
venv\Scripts\activate
```

Install the dependencies:

```powershell
pip install google-adk python-dotenv
```

Verify `google-adk` installation (optional):

```powershell
pip show google-adk
```

## Quick start

- Run the ADK web runner (if you have ADK CLI installed):

```powershell
adk web
```

- Or import the agents into your own runner / test harness. The repository is intentionally minimal so you can wire the agents into a simple loop or web endpoint.

## Project structure

- `catalog_agent/agent.py` — Agent that presents a small demo product catalog and adds items to cart.
- `checkout_agent/agent.py` — Agent that collects shipping address and saves it to session state.
- `order_summary_agent/agent.py` — Agent that reads session state and produces a friendly order summary.
- `ecommerce_agent/agent.py` — Root / router agent that collects user info and dispatches to the appropriate sub-agent.
- `README.md` — This file.

## How the agents interact (workflow)

1. `ecommerce_agent` greets the user and ensures basic user info (`name`, `email`, `mobile`) is captured via the `save_user_info` tool.
2. Based on the user's intent, the root agent delegates to exactly one sub-agent:
	- `catalog_agent` — for browsing products and adding items to cart. Uses a small fake catalog for demo (Smartphones, Laptops, Headphones).
	- `checkout_agent` — for collecting shipping address using `save_shipping_address`.
	- `order_summary_agent` — for generating a user-friendly summary of the completed order.
3. Each agent writes data into the session `ToolContext.state` (e.g. `item`, `quantity`, `price`, `shipping_address`). `order_summary_agent` reads these keys to produce the final summary.

Example session state keys used by the demo:
- `name`, `email`, `mobile`
- `category`, `item`, `quantity`, `price`
- `shipping_address`

## Usage examples

This repo is a code-level demo. You can experiment by importing `root_agent` from `ecommerce_agent.agent` into a small Python driver that simulates user messages and feeds them to the agent runner provided by `google-adk` or a simple loop for testing.

Minimal pseudo-runner idea:

```python
from ecommerce_agent.agent import root_agent

# integrate root_agent with your ADK runner or call its `handle` entrypoint according
# to the ADK runtime you have available.
```

See each `agent.py` for the exact instructions and tools the agent uses.

## Extending the demo

- Replace the hard-coded catalog inside `catalog_agent/agent.py` with a real product API.
- Add persistent cart storage (database) instead of saving to `ToolContext.state`.
- Add authentication and real payment handling in `checkout_agent`.
- Add a `tracking_agent` to support order status lookups.

## Notes and recommendations

- The demo models in the repository use model names like `gemini-2.5-flash` and `gemini-2.0-flash` in their definitions — ensure your account and ADK setup support them before making live API calls.
- Environment variables loaded via `.env` are used in the code (`dotenv.load_dotenv()` is called in each agent file). Create a `.env` file and add any required API keys if you want to connect to real LLM services.
- This project is provided as an educational example and is not production-ready.

---

If you'd like, I can:
- add a minimal runner script that simulates a user conversation, or
- create a `requirements.txt` and a small `.env.example`, or
- commit these changes for you and open a PR.

Happy to continue — tell me which of the follow-ups you'd like next.


