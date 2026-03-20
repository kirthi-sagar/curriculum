# GrocerFlow — Product Requirements

## Problem Statement
Kirana store owners — small, family-run neighborhood grocery shops — manage their inventory manually using paper ledgers, notebooks, or memory. This means they can't know what's in stock without physically checking shelves, leading to over-ordering, stockouts, and wasted time. GrocerFlow gives them a simple digital tool to track inventory in real time, so they always know exactly what they have and what's running low.

## User Stories

### Epic: First-Run Experience

- As a first-time user, I want to be welcomed and shown how the app works so that I know what to do without needing help.
  - [ ] App opens to a welcome banner: "Welcome to GrocerFlow! Here's how to get started:"
  - [ ] Banner lists 3 steps: "1. Add your products → 2. View your stock → 3. Update or remove items"
  - [ ] A prominent "Get Started" button takes the owner to the inventory dashboard
  - [ ] If inventory is empty, the dashboard shows a friendly empty state: "No items yet! Add your first product to get started." with a clear "Add Item" button
  - [ ] If inventory already has items, the dashboard shows the inventory list directly (no welcome banner on return visits)

### Epic: Viewing Inventory

- As a store owner, I want to see all my stock in a clean list so that I know what I have at a glance.
  - [ ] Inventory dashboard shows all active items in a list/card layout
  - [ ] Each item displays: name, category, quantity, price, and low-stock threshold
  - [ ] Items at or below their low-stock threshold are highlighted with a color change on the entire row (red or orange)
  - [ ] A "Low Stock Alert" section appears at the top of the page listing all items at or below threshold
  - [ ] When a low-stock item's quantity is updated above its threshold, it automatically disappears from the Low Stock Alert section and the row color returns to normal
  - [ ] If no items are low on stock, the Low Stock Alert section is hidden

### Epic: Adding Items

- As a store owner, I want to add a new product to my inventory so that I can track it going forward.
  - [ ] An "Add Item" button is clearly visible on the dashboard
  - [ ] Clicking it opens an add item form with fields: Name, Category (dropdown), Quantity, Price, Low-Stock Threshold
  - [ ] Category is a fixed dropdown of common Kirana categories (e.g. Grains & Pulses, Dairy, Snacks, Beverages, Spices, Personal Care, Cleaning Supplies, Frozen Foods, Other)
  - [ ] All fields are required — form cannot be submitted with any field empty
  - [ ] On successful save, the new item appears immediately in the inventory list
  - [ ] Form clears after successful submission, ready for another entry

### Epic: Editing Items

- As a store owner, I want to edit any detail of an existing product so that I can keep my inventory accurate.
  - [ ] Each item in the inventory list has an "Edit" button
  - [ ] Clicking Edit opens a form pre-filled with the item's current values: Name, Category, Quantity, Price, Low-Stock Threshold
  - [ ] The owner can change any or all fields
  - [ ] On save, the inventory list updates immediately with the new values
  - [ ] Low-stock status recalculates automatically after an edit (if quantity is updated above threshold, warning clears; if below, warning appears)

### Epic: Deleting Items

- As a store owner, I want a safe way to remove products from my inventory so that I don't accidentally lose important data.
  - [ ] Each item has a "Delete" button
  - [ ] Clicking Delete shows a confirmation prompt: "Are you sure you want to remove [item name]? It will be moved to Deleted Items."
  - [ ] Confirming moves the item to a Deleted Items section (soft delete) — it is NOT permanently removed
  - [ ] The item disappears from the active inventory list immediately
  - [ ] A "Deleted Items" section is accessible from the dashboard (e.g. via a tab or expandable section)
  - [ ] In Deleted Items, each item shows its name, category, quantity, and price, with two actions: "Restore" and "Delete Permanently"
  - [ ] "Restore" moves the item back to the active inventory list
  - [ ] "Delete Permanently" removes the item completely with a second confirmation prompt: "This cannot be undone. Delete permanently?"
  - [ ] If Deleted Items section is empty, it shows: "No deleted items."

## What We're Building
Everything required for a complete, working inventory tool in 3-4 hours:

1. **Welcome screen** — first-run banner with 3-step guide and "Get Started" button
2. **Inventory dashboard** — card/list view of all active items (name, category, quantity, price, threshold)
3. **Low Stock Alert section** — auto-updates as quantities change; hides when nothing is low
4. **Row color highlighting** — visual warning on items at or below their threshold
5. **Add Item form** — all 5 fields, fixed category dropdown, validation, clears on submit
6. **Edit Item form** — pre-filled with existing values, all fields editable
7. **Soft delete flow** — confirmation prompt → Deleted Items section
8. **Deleted Items section** — restore or permanently delete with second confirmation
9. **Data persistence** — all changes saved to a local file so data survives app restarts

## What We'd Add With More Time
Features worth building if the core is done early (good candidates for `/iterate`):

- **Search/filter inventory** — search by name or filter by category
- **Sort inventory** — sort by name, quantity, or category
- **Step-by-step onboarding wizard** — guided walkthrough for brand-new users (Version B from planning)
- **Restock suggestions** — flag items that have been low for more than X days
- **Export to CSV** — let the owner download their inventory as a spreadsheet
- **Item count summary** — total products, total value of stock, number of low-stock items shown as summary cards at top of dashboard

## Non-Goals
These are explicitly out of scope for this build:

- **Authentication/login** — no signup, no email, no Google, no Clerk. The app opens directly to the dashboard. A single-user local tool doesn't need accounts.
- **Customer-facing ordering** — GrocerFlow is a store owner tool only. No customer browsing or checkout.
- **Barcode/QR scanning** — valuable but requires hardware integration; out of scope for a 3-4 hour build.
- **Analytics & reporting** — no charts, no demand trends, no behavioral insights. That belongs to the full GrocerFlow vision.
- **Multi-store support** — one store, one owner, one inventory list.

## Open Questions
- **Category list:** What are the exact Kirana categories to include in the dropdown? (Needs answering before `/spec` — will define the fixed list)
- **Price format:** Should price be stored per unit? What currency symbol to display (₹ assumed)? (Can decide in `/spec`)
- **Low-stock threshold default:** Should new items default to a threshold of 0 (no warning) or a suggested value like 5 or 10? (Can decide in `/spec`)
