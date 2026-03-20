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
