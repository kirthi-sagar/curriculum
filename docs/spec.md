# GrocerFlow — Technical Spec

## Stack

| Tool | Version | Purpose | Docs |
|------|---------|---------|------|
| Python | 3.10+ | Core language | [python.org](https://www.python.org) |
| Streamlit | 1.55.0 | Web UI framework | [docs.streamlit.io](https://docs.streamlit.io) |
| supabase-py | 2.28.2 | Database client | [supabase.com/docs/reference/python/introduction](https://supabase.com/docs/reference/python/introduction) |
| Supabase | Free tier | Hosted PostgreSQL database | [supabase.com](https://supabase.com) |

Install dependencies:
```bash
pip install streamlit supabase
```

## Runtime & Deployment

- **Runtime:** Web app running in the browser
- **Local development:** `streamlit run app.py` → opens at `http://localhost:8501`
- **Production:** Streamlit Community Cloud ([share.streamlit.io](https://share.streamlit.io)) — free, one-click deploy from GitHub
- **Python requirement:** 3.10 or higher
- **Secrets required:** `SUPABASE_URL` and `SUPABASE_KEY` (stored in `.streamlit/secrets.toml` locally; added via Streamlit Cloud dashboard for production — never committed to GitHub)

## Architecture Overview

```
┌─────────────────────────────────┐
│         Browser (User)          │
│    Streamlit UI — app.py        │
│  Welcome │ Inventory │ Deleted  │
└────────────────┬────────────────┘
                 │ calls
┌────────────────▼────────────────┐
│         database.py             │
│  fetch_items() add_item()       │
│  update_item() delete_item()    │
│  restore_item() perm_delete()   │
└────────────────┬────────────────┘
                 │ supabase-py
┌────────────────▼────────────────┐
│   Supabase (PostgreSQL)         │
│   table: inventory              │
└─────────────────────────────────┘
```

**Data flow:**
1. User interacts with Streamlit UI in `app.py`
2. `app.py` calls a function from `database.py`
3. `database.py` sends a query to Supabase using supabase-py
4. Supabase returns data → `database.py` returns it to `app.py`
5. `app.py` re-renders the UI with updated data

## UI Layer — app.py

Implements all epics from `prd.md`. Single-file Streamlit app. All pages and sections are rendered from this file using Streamlit's built-in layout components.

### Welcome Screen

Implements `prd.md > First-Run Experience`.

- On first load, check if inventory is empty (call `fetch_items(is_deleted=False)`)
- If empty: render welcome banner with 3-step guide and "Get Started" button
  - Step 1: Add your products
  - Step 2: View your stock
  - Step 3: Update or remove items
- If items exist: skip welcome banner, go straight to inventory dashboard
- "Get Started" button sets `st.session_state.show_welcome = False` and reruns the app

### Inventory Dashboard

Implements `prd.md > Viewing Inventory`.

- Main view of all active items (`is_deleted = False`)
- Fetches items fresh from Supabase on every page load/rerun
- **Low Stock Alert section** (rendered at top):
  - Only shown if at least one item has `quantity <= threshold`
  - Lists all low-stock items by name with current quantity and threshold
  - Auto-hides when no items are below threshold
- **Inventory list** (rendered below alerts):
  - Each item displayed as a row showing: Name, Category, Quantity, Price (₹), Threshold
  - If `quantity <= threshold`: row background highlighted in orange/red using custom CSS via `st.markdown()`
  - Each row has Edit and Delete buttons

### Add Item Form

Implements `prd.md > Adding Items`.

- "Add Item" button visible on dashboard
- Clicking opens a form (use `st.form()`) with fields:
  - Name: `st.text_input()`
  - Category: `st.selectbox()` with fixed category list (see Data Model)
  - Quantity: `st.number_input()`, min value 0
  - Price (₹): `st.number_input()`, min value 0.0
  - Low-Stock Threshold: `st.number_input()`, min value 0
- All fields required — validate before calling `database.py`
- On submit: call `add_item()`, clear form, rerun app to refresh inventory list

### Edit Item Form

Implements `prd.md > Editing Items`.

- Each inventory row has an "Edit" button
- Clicking sets `st.session_state.editing_id = item_id` and reruns
- Edit form renders pre-filled with current item values (same 5 fields as Add)
- On save: call `update_item()`, clear `editing_id`, rerun
- Low-stock status recalculates automatically on rerun (comparison happens in render logic)

### Delete Flow

Implements `prd.md > Deleting Items`.

- Each row has a "Delete" button
- Clicking sets `st.session_state.confirm_delete_id = item_id` and reruns
- Confirmation prompt renders: "Are you sure you want to remove [item name]? It will be moved to Deleted Items."
- Two buttons: "Yes, Remove" and "Cancel"
  - "Yes, Remove": calls `delete_item()` (sets `is_deleted=True`), clears state, reruns
  - "Cancel": clears `confirm_delete_id`, reruns

### Deleted Items Section

Implements `prd.md > Deleting Items` (restore and permanent delete).

- Accessible via a collapsible `st.expander("Deleted Items")` at the bottom of the dashboard
- Fetches items where `is_deleted = True`
- If empty: shows "No deleted items."
- Each deleted item shows: Name, Category, Quantity, Price — plus two buttons:
  - "Restore": calls `restore_item()`, reruns
  - "Delete Permanently": triggers a second confirmation prompt ("This cannot be undone. Delete permanently?")
    - "Yes, Delete": calls `perm_delete_item()`, reruns
    - "Cancel": clears state, reruns

### Styling

- Custom CSS injected via `st.markdown("<style>...</style>", unsafe_allow_html=True)`
- Low-stock rows: orange/red background (`#FF6B35` or `#E63946`)
- App accent colors: saffron orange (`#FF9933`), fresh green (`#138808`), clean white background
- Header: GrocerFlow logo text in bold with tagline "Powering your Kirana, digitally."
- Font: Streamlit default (Inter) — clean and readable

## Database Layer — database.py

All Supabase interactions live here. `app.py` never calls Supabase directly — it always goes through these functions. This keeps the database logic isolated and easy to debug.

### Supabase Client Initialization

```python
import streamlit as st
from supabase import create_client, Client

def get_client() -> Client:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)
```

### fetch_items(is_deleted: bool)

Fetches all items where `is_deleted` matches the argument.
- Active inventory: `fetch_items(is_deleted=False)`
- Deleted items: `fetch_items(is_deleted=True)`
- Returns a list of dicts.

```python
supabase.table("inventory").select("*").eq("is_deleted", is_deleted).execute()
```

### add_item(name, category, quantity, price, threshold)

Inserts a new row into the `inventory` table with `is_deleted=False`.

### update_item(item_id, name, category, quantity, price, threshold)

Updates all fields for the row matching `item_id`.

### delete_item(item_id)

Soft delete — sets `is_deleted=True` for the row matching `item_id`.

### restore_item(item_id)

Sets `is_deleted=False` for the row matching `item_id`.

### perm_delete_item(item_id)

Hard delete — permanently removes the row matching `item_id`.
```python
supabase.table("inventory").delete().eq("id", item_id).execute()
```

## Data Model

### Supabase Table: `inventory`

Create this table in the Supabase dashboard (Table Editor) before running the app:

| Column | Type | Default | Notes |
|--------|------|---------|-------|
| id | uuid | `gen_random_uuid()` | Primary key, auto-generated |
| name | text | — | Product name |
| category | text | — | From fixed category list |
| quantity | numeric | — | Current stock level |
| price | numeric | — | Price in ₹ per unit |
| threshold | integer | 5 | Low-stock warning level |
| is_deleted | boolean | `false` | Soft delete flag |
| created_at | timestamptz | `now()` | Auto-generated |

### Fixed Category List

Used in `st.selectbox()` in the Add and Edit forms:

```python
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
```

### Session State Keys

Streamlit's `st.session_state` is used to track UI state across reruns:

| Key | Type | Purpose |
|-----|------|---------|
| `show_welcome` | bool | Whether to show the welcome screen |
| `editing_id` | str or None | ID of the item currently being edited |
| `confirm_delete_id` | str or None | ID of the item pending delete confirmation |
| `confirm_perm_delete_id` | str or None | ID of the item pending permanent delete confirmation |

## File Structure

```
grocerflow/
├── app.py                    # Main Streamlit app — all UI and page logic
├── database.py               # All Supabase interactions — never called directly from UI
├── requirements.txt          # Python dependencies (streamlit, supabase)
├── .streamlit/
│   └── secrets.toml          # Supabase credentials — NEVER commit to GitHub
├── .gitignore                # Must include .streamlit/secrets.toml
├── docs/
│   ├── scope.md              # Project scope
│   ├── prd.md                # Product requirements
│   └── spec.md               # This file
└── process-notes.md          # Learning journal
```

**`requirements.txt` contents:**
```
streamlit==1.55.0
supabase==2.28.2
```

**`.streamlit/secrets.toml` contents (local only):**
```toml
SUPABASE_URL = "your-project-url-here"
SUPABASE_KEY = "your-anon-key-here"
```

## Key Technical Decisions

1. **Supabase over CSV/JSON file:** File-based storage doesn't persist on Streamlit Community Cloud — data resets on every restart. Supabase is free, persistent, and requires no server setup. Tradeoff: requires a Supabase account and a one-time table creation step before build.

2. **Two-file structure (app.py + database.py):** Separating UI from database logic makes the code easier to debug. If the inventory isn't showing, you know to look in `database.py`. If a button isn't working, look in `app.py`. Tradeoff: slightly more files than a single-script approach, but worth it for clarity.

3. **Soft delete with `is_deleted` flag:** Instead of deleting rows from the database immediately, items are hidden by setting `is_deleted=True`. This enables the Deleted Items / Restore feature. Tradeoff: the table grows over time, but for a Kirana store's scale, this is irrelevant.

## Dependencies & External Services

| Service | Purpose | Free Tier | Docs |
|---------|---------|-----------|------|
| Supabase | Hosted PostgreSQL database | Yes — unlimited API requests, 500MB storage | [supabase.com/docs](https://supabase.com/docs) |
| Streamlit Community Cloud | App hosting & deployment | Yes — free for public repos | [docs.streamlit.io/deploy](https://docs.streamlit.io/deploy/streamlit-community-cloud) |
| GitHub | Source code hosting | Yes | [github.com](https://github.com) |

**No API keys needed beyond Supabase project URL and anon key.**

## Demo Flow

The spec is built to support this exact demo sequence:

1. Open GrocerFlow URL → Welcome screen with 3-step guide
2. Click "Get Started" → Empty inventory with "Add Item" prompt
3. Add *Basmati Rice* (Grains & Staples, qty 8, ₹120, threshold 10) → appears in list
4. Add *Amul Butter* (Dairy, qty 2, ₹55, threshold 5) → row turns orange, Low Stock Alert appears
5. Edit Basmati Rice → change qty to 5 → joins Low Stock section
6. Edit Basmati Rice again → change qty to 50 → disappears from Low Stock automatically
7. Delete Amul Butter → confirmation prompt → moves to Deleted Items
8. Open Deleted Items → Restore Amul Butter → back in active inventory

## Open Issues

- **Supabase table creation:** Learner must manually create the `inventory` table in Supabase dashboard before `/build`. This is the highest-risk step — will be handled explicitly in the first checklist item.
- **GitHub repo setup:** Learner needs a public GitHub repo connected to Streamlit Community Cloud. Must be set up before deployment checklist item.
- **`.gitignore` is critical:** `secrets.toml` must never be committed. The build must create `.gitignore` as one of the first steps.
