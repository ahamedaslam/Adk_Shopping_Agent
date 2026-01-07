from db.supabase_client import supabase

def create_order(email, total):
    return supabase.table("orders").insert({
        "email": email,
        "total": total,
        "status": "CREATED"
    }).execute().data[0]

def add_order_item(order_id, product_id, qty, price):
    supabase.table("order_items").insert({
        "order_id": order_id,
        "product_id": product_id,
        "qty": qty,
        "price": price
    }).execute()

def deduct_stock(product_id, qty):
    supabase.rpc("deduct_stock", {"pid": product_id, "qty": qty}).execute()
