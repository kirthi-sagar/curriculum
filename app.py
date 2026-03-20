# GrocerFlow — app.py
# Main Streamlit app. All UI lives here.

import streamlit as st
import database

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="GrocerFlow", page_icon="🛒", layout="wide")

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .header-title { font-size: 2rem; font-weight: 800; color: #FF9933; }
    .header-tagline { font-size: 1rem; color: #138808; margin-bottom: 1.5rem; }
    .low-stock-row { background-color: #FF6B35; color: white; padding: 0.4rem 0.8rem;
                     border-radius: 6px; margin-bottom: 0.3rem; }
    .normal-row { background-color: #f9f9f9; padding: 0.4rem 0.8rem;
                  border-radius: 6px; margin-bottom: 0.3rem; }
    .alert-box { background-color: #fff3cd; border-left: 4px solid #FF9933;
                 padding: 0.8rem 1rem; border-radius: 6px; margin-bottom: 1rem; }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<div class="header-title">🛒 GrocerFlow</div>', unsafe_allow_html=True)
st.markdown('<div class="header-tagline">Powering your Kirana, digitally.</div>', unsafe_allow_html=True)

# ── Fetch active inventory ────────────────────────────────────────────────────
items = database.fetch_items(is_deleted=False)

# ── Welcome screen (first-run only) ──────────────────────────────────────────
if "show_welcome" not in st.session_state:
    st.session_state.show_welcome = True

if not items and st.session_state.show_welcome:
    st.markdown("""
    <div style="background-color:#fff8f0; border:2px solid #FF9933; border-radius:12px;
                padding:2rem; margin-bottom:2rem;">
        <h2 style="color:#FF9933;">👋 Welcome to GrocerFlow!</h2>
        <p style="font-size:1.1rem;">Here's how to get started:</p>
        <ol style="font-size:1.05rem; line-height:2;">
            <li>➕ <strong>Add your products</strong> — name, category, price and quantity</li>
            <li>📦 <strong>View your stock</strong> — see everything at a glance</li>
            <li>✏️ <strong>Update or remove items</strong> — keep your inventory accurate</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🚀 Get Started", type="primary"):
        st.session_state.show_welcome = False
        st.rerun()
    st.stop()

# ── Low Stock Alert section ───────────────────────────────────────────────────
low_stock_items = [i for i in items if i["quantity"] <= i["threshold"]]

if low_stock_items:
    st.markdown('<div class="alert-box"><strong>⚠️ Low Stock Alert</strong></div>', unsafe_allow_html=True)
    for item in low_stock_items:
        st.markdown(
            f'<div class="low-stock-row">🔴 <strong>{item["name"]}</strong> — '
            f'Qty: {item["quantity"]} (threshold: {item["threshold"]})</div>',
            unsafe_allow_html=True
        )
    st.write("")

# ── Categories ───────────────────────────────────────────────────────────────
CATEGORIES = [
    "Grains & Staples",
    "Cooking Oils & Ghee",
    "Spices & Masalas",
    "Dairy Products",
    "Snacks & Biscuits",
    "Beverages",
    "Personal Care",
    "Household Cleaning",
    "Frozen Foods",
    "Stationery & Misc",
    "Other",
]

# ── Add Item form ─────────────────────────────────────────────────────────────
if "show_add_form" not in st.session_state:
    st.session_state.show_add_form = False

col_btn, _ = st.columns([2, 8])
with col_btn:
    if st.button("➕ Add Item", type="primary"):
        st.session_state.show_add_form = True

if st.session_state.show_add_form:
    with st.form("add_item_form", clear_on_submit=True):
        st.subheader("Add New Item")
        name = st.text_input("Product Name")
        category = st.selectbox("Category", CATEGORIES)
        quantity = st.number_input("Quantity", min_value=0.0, step=1.0)
        price = st.number_input("Price (₹)", min_value=0.0, step=0.5)
        threshold = st.number_input("Low-Stock Threshold", min_value=0, step=1)

        col_save, col_cancel = st.columns([1, 1])
        with col_save:
            submitted = st.form_submit_button("💾 Save Item", type="primary")
        with col_cancel:
            cancelled = st.form_submit_button("Cancel")

        if submitted:
            if not name.strip():
                st.error("Product name cannot be empty.")
            else:
                database.add_item(name.strip(), category, quantity, price, int(threshold))
                st.session_state.show_add_form = False
                st.success(f"✅ '{name}' added to inventory!")
                st.rerun()

        if cancelled:
            st.session_state.show_add_form = False
            st.rerun()

# ── Inventory list ────────────────────────────────────────────────────────────
st.subheader("📦 Current Inventory")

if not items:
    st.info("No items yet! Add your first product to get started.")
else:
    # Column headers
    col1, col2, col3, col4, col5, col6, col7 = st.columns([3, 2, 1.5, 1.5, 1.5, 1, 1])
    col1.markdown("**Name**")
    col2.markdown("**Category**")
    col3.markdown("**Qty**")
    col4.markdown("**Price (₹)**")
    col5.markdown("**Threshold**")
    col6.markdown("")
    col7.markdown("")
    st.divider()

    for item in items:
        is_low = item["quantity"] <= item["threshold"]
        row_style = "low-stock-row" if is_low else "normal-row"

        col1, col2, col3, col4, col5, col6, col7 = st.columns([3, 2, 1.5, 1.5, 1.5, 1, 1])
        with col1:
            st.markdown(
                f'<div class="{row_style}">{item["name"]}</div>',
                unsafe_allow_html=True
            )
        with col2:
            st.markdown(
                f'<div class="{row_style}">{item["category"]}</div>',
                unsafe_allow_html=True
            )
        with col3:
            st.markdown(
                f'<div class="{row_style}">{item["quantity"]}</div>',
                unsafe_allow_html=True
            )
        with col4:
            st.markdown(
                f'<div class="{row_style}">₹{item["price"]}</div>',
                unsafe_allow_html=True
            )
        with col5:
            st.markdown(
                f'<div class="{row_style}">{item["threshold"]}</div>',
                unsafe_allow_html=True
            )
        with col6:
            st.button("✏️", key=f"edit_{item['id']}")
        with col7:
            st.button("🗑️", key=f"delete_{item['id']}")
