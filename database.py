# GrocerFlow — database.py
# All Supabase interactions live here. app.py never calls Supabase directly.

import streamlit as st
from supabase import create_client, Client


def get_client() -> Client:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)


def fetch_items(is_deleted: bool):
    """Fetch all items where is_deleted matches the argument."""
    supabase = get_client()
    response = supabase.table("inventory").select("*").eq("is_deleted", is_deleted).execute()
    return response.data


def add_item(name: str, category: str, quantity: float, price: float, threshold: int):
    """Insert a new item into inventory."""
    supabase = get_client()
    supabase.table("inventory").insert({
        "name": name,
        "category": category,
        "quantity": quantity,
        "price": price,
        "threshold": threshold,
        "is_deleted": False,
    }).execute()


def update_item(item_id: str, name: str, category: str, quantity: float, price: float, threshold: int):
    """Update all fields for an existing item."""
    supabase = get_client()
    supabase.table("inventory").update({
        "name": name,
        "category": category,
        "quantity": quantity,
        "price": price,
        "threshold": threshold,
    }).eq("id", item_id).execute()


def delete_item(item_id: str):
    """Soft delete — mark item as deleted without removing it."""
    supabase = get_client()
    supabase.table("inventory").update({"is_deleted": True}).eq("id", item_id).execute()


def restore_item(item_id: str):
    """Restore a soft-deleted item back to active inventory."""
    supabase = get_client()
    supabase.table("inventory").update({"is_deleted": False}).eq("id", item_id).execute()


def perm_delete_item(item_id: str):
    """Permanently remove an item from the database."""
    supabase = get_client()
    supabase.table("inventory").delete().eq("id", item_id).execute()
