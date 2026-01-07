from dotenv import load_dotenv
load_dotenv()

from google.adk.agents import LlmAgent
from google.adk.tools import ToolContext
from checkout_agent.agent import checkout_agent
from db.product_service import get_product_by_name

from db.product_service import get_products_by_category


# Tool to list products by category
def list_products(tool_context: ToolContext, category: str):
    tool_context.state["last_category"] = category   # track browsing history

    products = get_products_by_category(category)

    if not products:
        return "No products available in this category."

    msg = f"🛒 {category.title()} Available Products:\n\n"
    for p in products:
        msg += f"- {p['name']} — ₹{p['price']} (Stock: {p['stock']})\n"

    return msg



# Tool to add product to cart
def save_cart(tool_context: ToolContext, product_name: str, quantity: int):
    products = get_product_by_name(product_name)

    if not products:
        return "❌ Product not found."

    product = products[0]

    if product["stock"] < quantity:
        return f"⚠️ Only {product['stock']} left in stock."

    if "cart" not in tool_context.state:
        tool_context.state["cart"] = []

    tool_context.state["cart"].append({
        "product_id": product["id"],
        "name": product["name"],
        "price": float(product["price"]),
        "email": tool_context.state["email"],
        "qty": quantity
    })  

    return f"✅ {quantity} × {product['name']} added to cart."


# Define the catalog agent    
catalog_agent = LlmAgent(
    name="catalog_agent",
    model="gemini-2.5-flash-lite",
    description=(
        "A catalog agent who can help users browse products and add them to cart"
    ),
instruction="""
IMPORTANT:
After calling any tool, you MUST repeat the tool result to the user as a normal chat message.

You are the PRODUCT CATALOG AGENT backed by Supabase.

Your responsibilities:

1. Politely ask the user which category they are interested in.
   Example: "We have Phones, Laptops and Headphones — which would you like to browse?"

2. When the user gives a category, call list_products and show the result to the user.

3. Once the user selects the product, call save_cart to save in the state.

4. After that asks the user politely if they want to continue shopping or proceed to checkout.

5. If they want to checkout, hand over to the checkout_agent.

6. Keep responses short, friendly and helpful.
""",
# Register tools and sub-agents
    tools=[list_products,save_cart],
    sub_agents=[checkout_agent]

) 
