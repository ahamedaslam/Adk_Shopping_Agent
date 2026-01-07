from dotenv import load_dotenv
load_dotenv()

from google.adk.agents import LlmAgent
from google.adk.tools import google_search, ToolContext
from order_summary_agent.agent import order_summary_agent
from db.order_service import create_order, add_order_item, deduct_stock


def place_order(tool_context: ToolContext):
    email = tool_context.state["email"]
    cart = tool_context.state["cart"]

    total = sum(i["price"] * i["qty"] for i in cart)

    order = create_order(email, total)

    for item in cart:
        add_order_item(order["id"], item["product_id"], item["qty"], item["price"])
        deduct_stock(item["product_id"], item["qty"])

    tool_context.state["order"] = order
    return f"Order placed successfully! Order ID: {order['id']}"


def save_shipping_address(tool_context: ToolContext, address: str):
    tool_context.state["shipping_address"] = address


checkout_agent = LlmAgent(
    name="checkout_agent",
    description="A Checkout agent that collects user's shipping address",
    model="gemini-2.5-flash-lite",
   instruction="""
You are the CHECKOUT AGENT for an AI ecommerce system.

Your responsibilities:

1. Collect the user's full shipping address in a single clear message.
2. Call save_shipping_address to store it in the session state.
3. Confirm the address with the user.
4. When the user confirms checkout, call place_order to:
   - Create a real order in the database
   - Save order items
   - Deduct stock
5. After placing the order, inform the user with the generated Order ID.
6. Ask whether the user wants to view their order summary and, if yes, hand over to the order_summary_agent.
    
Rules:
- Do NOT place the order until the user explicitly confirms.
- Never make up order IDs.
- Always rely on the place_order tool to generate real orders.
- Keep responses short and professional.
"""
,
    tools=[save_shipping_address,place_order],
    sub_agents=[order_summary_agent]
)
