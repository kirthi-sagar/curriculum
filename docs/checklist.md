# Build Checklist

## Build Preferences

- **Git:** Commit after each item with message: `"Complete step N: [title]"`
- **Verification:** Run `streamlit run app.py` and visually confirm after each step
- **Check-in cadence:** Speed-run — minimal explanations, move fast

## Checklist

- [x] **1. Project setup — repo, file structure, and .gitignore**
  Spec ref: `spec.md > File Structure`
  What to build: Create a GitHub repo named `grocerflow`. Set up the full folder structure: `app.py`, `database.py`, `requirements.txt`, `.gitignore`, `.streamlit/secrets.toml`, and `docs/` folder. Add `.streamlit/secrets.toml` to `.gitignore`. Populate `requirements.txt` with `streamlit==1.55.0` and `supabase==2.28.2`. Leave `app.py` and `database.py` empty for now.
  Acceptance: Folder structure matches `spec.md > File Structure`. `secrets.toml` is listed in `.gitignore`. `requirements.txt` has both dependencies.
  Verify: Open `.gitignore` and confirm `secrets.toml` is listed. Push to GitHub and confirm the repo is visible but `secrets.toml` is not in the commit.

- [x] **2. Supabase table setup and credentials**
  Spec ref: `spec.md > Data Model > Supabase Table: inventory`
  What to build: In the Supabase dashboard, create a new project (if not already done). In the Table Editor, create a table named `inventory` with these columns: `id` (uuid, primary key, default `gen_random_uuid()`), `name` (text), `category` (text), `quantity` (numeric), `price` (numeric), `threshold` (int4, default 5), `is_deleted` (bool, default false), `created_at` (timestamptz, default `now()`). Copy the project URL and anon key from Project Settings > API. Add them to `.streamlit/secrets.toml` as `SUPABASE_URL` and `SUPABASE_KEY`.
  Acceptance: Table exists in Supabase with all 8 columns. `secrets.toml` has both values filled in.
  Verify: In the Supabase Table Editor, manually insert one test row. Confirm it appears in the table. Delete the test row.

- [ ] **3. Database layer — all Supabase functions in database.py**
  Spec ref: `spec.md > Database Layer — database.py`
  What to build: Write all 6 functions in `database.py`: `get_client()`, `fetch_items(is_deleted)`, `add_item(name, category, quantity, price, threshold)`, `update_item(item_id, name, category, quantity, price, threshold)`, `delete_item(item_id)`, `restore_item(item_id)`, `perm_delete_item(item_id)`. Add a basic `app.py` that imports `database.py`, calls `fetch_items(is_deleted=False)`, and prints the result with `st.write()`.
  Acceptance: `app.py` runs without errors. `st.write()` shows an empty list `[]` (since no items exist yet). No connection errors.
  Verify: Run `streamlit run app.py`. Confirm the browser shows an empty list with no error messages.

- [ ] **4. Inventory dashboard — item list, low stock alerts, and row highlighting**
  Spec ref: `spec.md > UI Layer — app.py > Inventory Dashboard`
  What to build: Build the main inventory view in `app.py`. Fetch all active items (`is_deleted=False`). If inventory is empty, show: "No items yet! Add your first product to get started." If items exist, render them in a table/list showing name, category, quantity, price, and threshold. Add the Low Stock Alert section at the top — only shown when at least one item has `quantity <= threshold`. Highlight low-stock rows using custom CSS injected with `st.markdown()`. Use saffron orange (`#FF9933`) and green (`#138808`) as accent colors.
  Acceptance: Matches `prd.md > Viewing Inventory` acceptance criteria. Empty state message shows when no items exist. Low stock section appears/disappears correctly. Low-stock rows change color.
  Verify: Manually insert 2 rows in Supabase (one with quantity below threshold, one above). Run the app. Confirm the low-stock row is highlighted and appears in the alert section. Confirm the normal row is not highlighted.

- [ ] **5. Welcome screen — first-run detection and onboarding banner**
  Spec ref: `spec.md > UI Layer — app.py > Welcome Screen`
  What to build: Before rendering the dashboard, check if inventory is empty. If empty AND `st.session_state.show_welcome` is not False, show the welcome banner: "Welcome to GrocerFlow! Here's how to get started:" with 3 steps listed and a "Get Started" button. Clicking the button sets `st.session_state.show_welcome = False` and reruns. If inventory has items, skip the banner entirely.
  Acceptance: Matches `prd.md > First-Run Experience` acceptance criteria. Welcome banner shows on first visit with empty inventory. "Get Started" dismisses it. Banner never shows when inventory has items.
  Verify: Clear the Supabase table. Run the app. Confirm welcome banner appears. Click "Get Started" — confirm it goes to the empty dashboard. Add a row in Supabase, refresh the app — confirm banner does not show.

- [ ] **6. Add Item form — form, validation, and save**
  Spec ref: `spec.md > UI Layer — app.py > Add Item Form`
  What to build: Add an "Add Item" button to the dashboard. Clicking it opens a `st.form()` with 5 fields: Name (`st.text_input`), Category (`st.selectbox` with the 11 CATEGORIES list from `spec.md`), Quantity (`st.number_input`, min 0), Price in ₹ (`st.number_input`, min 0.0), Low-Stock Threshold (`st.number_input`, min 0). Validate that Name is not empty before submitting. On submit, call `add_item()`, then rerun the app to refresh the list.
  Acceptance: Matches `prd.md > Adding Items` acceptance criteria. All 5 fields present. Category shows fixed dropdown. Empty name blocked. New item appears in list immediately after save.
  Verify: Run the app. Add a new item (e.g. "Basmati Rice", Grains & Staples, qty 8, ₹120, threshold 10). Confirm it appears in the inventory list. Add a second item with qty below its threshold — confirm low-stock alert appears.

- [ ] **7. Edit Item form — pre-filled form and update**
  Spec ref: `spec.md > UI Layer — app.py > Edit Item Form`
  What to build: Add an "Edit" button to each inventory row. Clicking sets `st.session_state.editing_id = item_id`. When `editing_id` is set, render an edit form pre-filled with that item's current values (same 5 fields). On save, call `update_item()`, clear `editing_id`, rerun. Low-stock status recalculates automatically on rerun.
  Acceptance: Matches `prd.md > Editing Items` acceptance criteria. Edit form pre-fills all current values. Changes save and reflect immediately. Changing quantity above threshold removes low-stock warning. Changing below threshold adds it.
  Verify: Edit Basmati Rice — change qty to 5 (below threshold 10). Confirm it joins the Low Stock section. Edit again — change qty to 50. Confirm it leaves the Low Stock section automatically.

- [ ] **8. Delete flow — confirmation prompt and soft delete**
  Spec ref: `spec.md > UI Layer — app.py > Delete Flow`
  What to build: Add a "Delete" button to each inventory row. Clicking sets `st.session_state.confirm_delete_id = item_id`. Render a confirmation prompt: "Are you sure you want to remove [item name]? It will be moved to Deleted Items." with "Yes, Remove" and "Cancel" buttons. "Yes, Remove" calls `delete_item()` (sets `is_deleted=True`), clears state, reruns. "Cancel" clears state, reruns.
  Acceptance: Matches `prd.md > Deleting Items` (soft delete part). Confirmation appears before delete. Item disappears from active inventory after confirm. Cancel does nothing.
  Verify: Delete an item. Confirm the confirmation prompt appears. Confirm "Yes, Remove" removes it from the list. Check Supabase Table Editor — confirm the row still exists with `is_deleted = true`.

- [ ] **9. Deleted Items section — view, restore, and permanent delete**
  Spec ref: `spec.md > UI Layer — app.py > Deleted Items Section`
  What to build: Add a `st.expander("Deleted Items")` at the bottom of the dashboard. Inside, fetch items where `is_deleted=True`. If empty, show "No deleted items." For each deleted item, show name, category, quantity, price, and two buttons: "Restore" and "Delete Permanently". "Restore" calls `restore_item()`, reruns. "Delete Permanently" sets `st.session_state.confirm_perm_delete_id = item_id`, shows a second confirmation ("This cannot be undone. Delete permanently?"), and calls `perm_delete_item()` on confirm.
  Acceptance: Matches `prd.md > Deleting Items` (restore and permanent delete). Deleted items section shows/hides correctly. Restore moves item back to active inventory. Permanent delete removes it completely with second confirmation.
  Verify: Open Deleted Items expander — confirm deleted item is listed. Click Restore — confirm item reappears in active inventory. Delete it again, then Delete Permanently — confirm it's gone from Supabase entirely.

- [ ] **10. Styling polish — colors, CSS, and final visual touches**
  Spec ref: `spec.md > UI Layer — app.py > Styling`
  What to build: Inject custom CSS via `st.markdown("<style>...</style>", unsafe_allow_html=True)`. Apply: saffron orange (`#FF9933`) and green (`#138808`) as accent colors. Low-stock row background: orange-red (`#FF6B35`). Add a header with "GrocerFlow" in bold and tagline "Powering your Kirana, digitally." Clean up button styles and spacing. Make the app feel colorful and modern — not like a spreadsheet.
  Acceptance: App looks colorful and lively. Header is visible. Low-stock rows stand out clearly. Overall aesthetic matches the design energy from `scope.md > Inspiration & References`.
  Verify: Run the app with a mix of normal and low-stock items. Take a screenshot. Does it look like a modern app a Kirana owner would be proud to use?

- [ ] **11. Deploy to Streamlit Community Cloud**
  Spec ref: `spec.md > Runtime & Deployment`
  What to build: Push the final code to GitHub (confirm `secrets.toml` is NOT in the commit). Go to [share.streamlit.io](https://share.streamlit.io), connect the GitHub repo, and deploy. In the Streamlit Cloud dashboard, go to App Settings > Secrets and add `SUPABASE_URL` and `SUPABASE_KEY`. Wait for the deploy to complete.
  Acceptance: App is live at a public `streamlit.app` URL. All features work identically to local. Data persists across browser sessions.
  Verify: Open the live URL in an incognito browser window. Add an item. Close the tab. Reopen — confirm the item is still there.

- [ ] **12. Prepare and record Devpost demo video**
  Spec ref: `prd.md > What We're Building` (the core flow to demonstrate)
  What to build: Record a 2-5 minute demo video following this script: (1) 30 sec — slides: "12 million Kirana stores in India are losing customers to quick-commerce. GrocerFlow gives them a digital inventory tool — simple, free, no commission." (2) 3 min — live app: open GrocerFlow, show welcome screen, click Get Started, add Basmati Rice, add Amul Butter below threshold (watch low-stock alert appear), edit Basmati Rice quantity up and down (watch alert appear/disappear), delete Amul Butter (show confirmation + Deleted Items), restore it. (3) 30 sec — close: "This is the first step toward a fully digital Kirana store. Built for owners, not against them." Use clear audio. Show the full browser window. Reference [Devpost's demo video tips](https://info.devpost.com/blog/6-tips-for-making-a-hackathon-demo-video).
  Acceptance: Video is 2-5 minutes. Problem is stated in the first 30 seconds. All core flows are shown working live. Audio is clear. A judge who knows nothing about the project understands what it does and why it matters.
  Verify: Watch the recording end to end. Would a judge who knows nothing about GrocerFlow understand what it does and why it matters within the first 60 seconds?
