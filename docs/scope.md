# GrocerFlow

## Idea
A colorful, modern inventory management app for Kirana (neighborhood grocery) store owners to track stock, add items, update quantities, and remove products — all without a paper ledger.

## Who It's For
A Kirana store owner — typically a family-run small shop — who currently tracks inventory manually (pen, paper, memory). They're not tech-savvy, but they're smart and busy. Their core pain: not knowing what's in stock without physically checking. GrocerFlow gives them a digital answer in seconds.

## Inspiration & References
- [Stock and Inventory Simple (Android)](https://play.google.com/store/apps/details?id=com.stockmanagment.next.app&hl=en_US) — stripped-down inventory loop: add, update, alert. Proof that simple wins.
- [Sortly](https://www.sortly.com/) — mobile-first, visual product cards, clean UX. The gold standard for non-technical users.
- [GitHub — Kirana Inventory Management](https://github.com/sagar-kale/kirana-inventory-management-system) — someone built a version of this; useful for scope calibration.

**Design energy:** Colorful and lively, modern app feel. Think vibrant accent colors (saffron orange, turmeric yellow, or fresh green), clean card-based layout, readable fonts, and a UI that feels alive — not like a spreadsheet.

## Goals
- Give a Kirana owner a real digital tool they can open and immediately understand.
- Demonstrate the core GrocerFlow mission: empower local stores with tech, no commissions, no complexity.
- Build something the learner is proud to show — a working app with a real use case, not a toy.

## What "Done" Looks Like
A Streamlit web app where a store owner can:
1. See all current inventory items in a clean, visual list (name, category, quantity, price).
2. Add a new item (name, category, quantity, price).
3. Update the quantity of an existing item.
4. Delete an item from inventory.
5. See a visual low-stock warning for items below a set threshold.

The app opens in a browser, looks colorful and modern, and works end-to-end with data persisted in a local CSV or JSON file.

## What's Explicitly Cut
- **Customer-facing ordering** — out. This is a store owner tool only.
- **Wholesaler bidding** — out. Belongs to the full KiranaKart vision, not this MVP.
- **Analytics & insights dashboard** — out. No behavioral data, no charts, no market intelligence.
- **Barcode/QR scanning** — out. Valuable feature, but requires hardware integration; too complex for 3-4 hours.
- **User authentication/login** — out. Single-user local app, no accounts needed.
- **Multi-store support** — out. One store, one owner.
- **Delivery/pickup management** — out. Inventory only.

## Technical Experience
- **Level:** Complete beginner.
- **Knows:** Python basics (actively learning via Codecademy Learn Python 3).
- **Doesn't know:** Web frameworks, databases, HTML/CSS/JS, anything beyond core Python.
- **Tool:** Streamlit — Python-only web app framework, perfect for beginners. No HTML required.
- **Data storage:** CSV or JSON file (no database setup needed).
- **Wants to explore:** Building a real, usable app for the first time.

## Loose Implementation Notes
- **Framework:** Streamlit (`pip install streamlit`)
- **Data:** `inventory.csv` or `inventory.json` in project root — simple file I/O with pandas or the `csv` module.
- **Structure:** Single `app.py` file to start. Keep it simple.
- **Deployment:** Run locally with `streamlit run app.py` — no cloud deployment needed for hackathon.
- **Styling:** Streamlit supports custom CSS via `st.markdown()` — can inject color and card styles to hit the lively aesthetic.
