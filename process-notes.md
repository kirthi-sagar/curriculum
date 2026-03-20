# Process Notes

## /build

### Step 4: Inventory dashboard — item list, low stock alerts, and row highlighting
- Built: Full inventory dashboard with column headers, per-row color highlighting (orange/red for low stock), Low Stock Alert section at top, header with GrocerFlow branding and tagline.
- Verification: Basmati Rice (qty 8, threshold 10) showed highlighted in orange/red and appeared in Low Stock Alert section. Amul Butter (qty 15, threshold 5) showed normally.
- Knowledge check answer: "when quantity goes above the threshold" — correct.
- Issues: Typo in CSS class string (`{row_style"` missing closing brace) caught and fixed before running.
- Learner engagement: None flagged.

### Step 3: Database layer — all Supabase functions in database.py
- Built: All 7 functions in database.py (get_client, fetch_items, add_item, update_item, delete_item, restore_item, perm_delete_item). Basic app.py with st.write() to test connection.
- Verification: Browser showed empty list [] with no errors.
- Knowledge check answer: "so that database errors are easier to find" — correct.
- Issues: secrets.toml values were missing quotes (TOML format requires strings in quotes). Fixed by wrapping values in double quotes.
- Learner engagement: Ran commands in chat instead of terminal — now understood the agent runs them directly.

### Step 2: Supabase table setup and credentials
- Built: inventory table created in Supabase with all 8 columns. Credentials added to secrets.toml.
- Verification: Test row inserted and appeared in Table Editor. Row deleted successfully.
- Knowledge check answer: Asked for an example rather than answering directly. Explained with Basmati Rice example after prompting.
- Issues: None.
- Learner engagement: No issues with Supabase dashboard navigation.

### Step 1: Project setup — repo, file structure, and .gitignore
- Built: app.py, database.py, requirements.txt, .gitignore (with secrets.toml protected), .streamlit/secrets.toml placeholder. All docs artifacts committed too.
- Verification: Committed and pushed to GitHub fork (kirthi-sagar/curriculum). secrets.toml not in commit.
- Knowledge check answer: "so that my Supabase credentials are not exposed publicly" — correct and clear.
- Issues: Learner unfamiliar with running terminal commands; was typing commands in chat. Resolved by running git commands directly via Bash tool.
- Learner engagement: Asked for help with terminal commands — good self-awareness about being a beginner.

## /checklist

**Sequencing decisions:**
- Step 1 (project setup) before everything — .gitignore for secrets.toml is critical, must come first
- Step 2 (Supabase table) before database.py — can't write functions without knowing the schema
- Step 3 (database layer) before UI — all UI depends on these functions
- Step 4 (dashboard) before forms — need somewhere to display items before adding them
- Step 5 (welcome screen) after dashboard — depends on the dashboard existing
- Steps 6-9 (forms and delete) in dependency order — add before edit/delete
- Step 10 (styling) last before deploy — functionality before aesthetics
- Step 11 (deploy) second-to-last — everything working locally before pushing
- Step 12 (demo video) always last

**Build preferences:**
- Check-in cadence: speed-run (minimal explanations)
- Git: commit after each step
- Verification: visual confirmation after each step

**Item count:** 12 items, estimated ~4 hours total. Tight for a beginner but achievable.

**Demo video planning:**
- Learner initially described the full KiranaKart vision, not the GrocerFlow demo. Redirected to the actual app. Demo script provided with clear 30sec/3min/30sec structure.
- "Wow moment": low-stock alert appearing automatically when quantity drops below threshold.

**Active shaping:**
- Learner correctly identified database/Supabase as the right starting point without prompting.
- Preferred speed-run cadence — confident and ready to build.
- Accepted proposed order without pushback.

## /spec

**Technical decisions made:**
- Supabase chosen over CSV/JSON for data persistence — Streamlit Community Cloud doesn't persist file writes between restarts. Learner chose Option A (real database) without hesitation.
- Streamlit Community Cloud for deployment — learner wants a live URL, not local demo. Free, one-click deploy from GitHub.
- Two-file structure (app.py + database.py) — UI and database logic separated for debuggability.
- Soft delete via `is_deleted` boolean flag — cleanly supports Deleted Items / Restore feature.

**Learner confidence:**
- Confident on scope and what to build. Less certain on technical details (deferred to agent on all stack decisions).
- Had a Supabase account already — reduced setup friction.

**Active shaping:**
- Learner deferred almost entirely to agent on architecture decisions.
- One strong moment: when asked about the demo flow, learner pivoted to the big KiranaKart vision. Agent redirected to the actual app demo. Learner accepted the redirect and confirmed the proposed demo script.
- Category list entirely agent-compiled from web research; learner approved without changes.

**Stack:** Python 3.10+ / Streamlit 1.55.0 / supabase-py 2.28.2 / Supabase free tier / Streamlit Community Cloud

**Self-review findings surfaced:**
- Supabase table must be created manually before build — flagged as highest-risk step
- `.gitignore` for secrets.toml is critical — flagged explicitly
- GitHub repo setup required before deployment

## /prd

**What the learner added vs scope doc:**
- Introduced soft-delete pattern (Recycle Bin) — items move to Deleted Items section before permanent removal. Strong instinct for data safety.
- Added restore functionality from Deleted Items back to active inventory.
- Per-item low-stock threshold (not store-wide) — more nuanced than scope doc assumed.
- Dual low-stock visual: row color change + separate alert section at top of page.
- Full field editing (all 5 fields editable, not just quantity).
- Welcome banner with 3-step guide (Version A+) instead of step-by-step wizard.

**"What if" questions that surprised them:**
- Restore from Deleted Items — learner hadn't initially mentioned restore, only delete permanently. Added it when prompted.
- Auto-clearing low-stock alerts — learner confirmed automatic behavior (no manual dismiss needed).

**Scope guard moments:**
- Authentication (Clerk, Google, email signup) crept back in. Firmly cut with rationale: beginner, 3-4 hours, single-user local tool. Learner accepted.
- Step-by-step onboarding wizard (Version B) — learner initially chose it. Redirected to Version A+ (welcome banner). Learner accepted. Version B moved to "What we'd add with more time."

**Active shaping:**
- Soft-delete with restore was entirely learner-initiated — a genuinely thoughtful UX decision.
- Auth creep was the one moment where the agent had to override learner preference; learner accepted without pushback.
- Category dropdown (fixed list vs free text) — learner chose fixed list, good call for consistency.

## /scope

**How the idea evolved:**
Learner arrived with a well-developed concept — GrocerFlow/KiranaKart — complete with a full ecosystem vision (customers, wholesalers, analytics, bidding, monetization strategy, even a brand manifesto). The broader vision is genuinely impressive and mission-driven: empower local Kirana stores without taking commission. Through conversation, the learner self-selected the right MVP slice: basic inventory management only. The project name settled on GrocerFlow for the hackathon MVP.

**Pushback received:**
- The KiranaKart doc revealed a 2-year roadmap. Learner was gently redirected: "this is a 2-year roadmap, not a 3-4 hour hackathon." Learner accepted this without resistance — they had already pre-scoped it correctly in their opening message.
- Several features explicitly cut: customer ordering, wholesaler bidding, analytics, barcode scanning, auth, multi-store. Learner had already intuited most of these cuts.

**References that resonated:**
- Stock and Inventory Simple — simple inventory loop validation
- Sortly — clean mobile-first UX inspiration
- GitHub Kirana Inventory project — scope calibration

**Technical experience:**
Complete beginner. Learning Python via Codecademy (Learn Python 3). No web development experience. Recommended Streamlit as Python-only framework — no HTML/CSS/JS required. Data storage: CSV or JSON file.

**Design direction:**
Colorful and lively, modern app feel. Vibrant accent colors (saffron orange, turmeric yellow, fresh green), card-based layout.

**Active shaping:**
Learner drove the direction strongly. They arrived with a pre-scoped MVP ("focus only on the basic store inventory workflow"), a full vision document, a clear philosophy, and a design instinct. The agent primarily validated and refined rather than invented. The core decisions — what to build, what to cut, the no-commission mission — were all learner-initiated.
