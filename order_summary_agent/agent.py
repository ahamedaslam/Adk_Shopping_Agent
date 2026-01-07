from dotenv import load_dotenv
load_dotenv()

from google.adk.agents import LlmAgent
from google.adk.tools import ToolContext
from db.summary_service import get_order_summary
from datetime import datetime
from datetime import datetime



# Tool to load order summary - generates invoice text
def load_order_summary(tool_context: ToolContext):
    order = tool_context.state["order"]
    customer = tool_context.state
    cart = tool_context.state["cart"]

    invoice = f"""
🧾 INVOICE
━━━━━━━━━━━━━━━━━━━━━━━━━━
Invoice ID : {order['id']}
Customer   : {customer['name']}
Email      : {customer['email']}
Mobile     : {customer['mobile']}
Date       : {datetime.now().strftime("%d %b %Y")}
━━━━━━━━━━━━━━━━━━━━━━━━━━

ITEMS
"""

    total = 0

    for item in cart:
        name = item["name"]
        qty = item["qty"]
        price = float(item["price"])
        line_total = qty * price
        total += line_total

        invoice += f"- {name:25} {qty} × ₹{price:.2f} = ₹{line_total:.2f}\n"

    gst = round(total * 0.18, 2)
    grand_total = total + gst

    invoice += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━
Subtotal : ₹{total:.2f}
GST (18%) : ₹{gst:.2f}
━━━━━━━━━━━━━━━━━━━━━━━━━━
GRAND TOTAL : ₹{grand_total:.2f}

Shipping Address:
{tool_context.state["shipping_address"]}

Thank you for shopping with us ❤️
"""

    return invoice





order_summary_agent = LlmAgent(
    name="order_summary_agent",
    model="gemini-2.5-flash-lite",
    description="Shows invoice summary",
    instruction="""
You provide the user's final invoice summary.
Always use load_order_summary tool to generate invoice.
Do not calculate manually.
""",
    tools=[load_order_summary]
)