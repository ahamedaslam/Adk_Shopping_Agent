from db.supabase_client import supabase

def get_products_by_category(category):
    category = category.lower().strip()
    
    res = supabase.table("products") \
        .select("id,name,price,stock") \
        .eq("category", category) \
        .eq("is_active", True) \
        .execute()
    
    return res.data


def get_product_by_name(name):
    res = supabase.table("products") \
        .select("id,name,price,stock") \
        .ilike("name", f"%{name}%") \
        .eq("is_active", True) \
        .execute()
    return res.data
