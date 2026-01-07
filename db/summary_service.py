from db.supabase_client import supabase

def get_order_summary(order_id):
    order = supabase.table("orders").select("*").eq("id", order_id).single().execute().data
    items = supabase.table("order_items") \
        .select("qty,price,products(name)") \
        .eq("order_id", order_id) \
        .execute().data
    return order, items
