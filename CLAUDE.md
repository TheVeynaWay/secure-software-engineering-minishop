# CLAUDE.md

## Project Overview
This project is for Secure Software Engineering Phase 0.

We are building a small multi-user web application that will be handed to another group for security analysis.

Project Title:
MiniShop – Multi-User Mock Shopping Platform

IMPORTANT:
This is NOT a full production e-commerce system.
Keep the project small, understandable, and analyzable within one sitting.

---

## Core Requirements (MUST SATISFY)
The application must satisfy:

- At least 2 user roles (with server-side enforcement)
- Persistent data storage (SQLite)
- At least 2 forms with server-side validation
- At least 4 distinct pages
- At least 2 complete end-to-end workflows
- Use of AI tools must be documented in AI_USAGE.md

---

## Scope Control (VERY IMPORTANT)
Keep the system simple.

DO:
- Implement authentication
- Implement role-based access control
- Implement basic product browsing
- Implement order submission
- Implement admin management features

DO NOT:
- Add payment systems
- Add shipping logic
- Add email services
- Use complex frontend frameworks (React, etc.)
- Add third-party APIs unless explicitly requested

If a feature is not required for R1–R6, do NOT implement it.

---

## Tech Stack
- Backend: Flask (Python)
- Database: SQLite
- Frontend: Jinja templates + basic CSS
- Authentication: session-based login
- Password storage: hashed passwords only

---

## Data Model (High-Level)

### Users
- id
- username
- password (hashed)
- role (customer / admin)

### Products
- id
- name
- price
- description

### Orders
- id
- user_id
- product_id
- quantity
- status (pending / shipped / etc.)

---

## User Roles & Permissions

### Customer
- Register and log in
- View product list
- Place orders
- View their own order history

### Admin
- Add/edit/delete products
- View all orders
- Update order status

RULE:
All authorization MUST be enforced on the server side.
Never rely on frontend-only restrictions.

---

## Required Pages (Minimum)
- Login / Register Page
- Product Listing Page
- Cart / Order Page
- Order History Page
- Admin Dashboard

---

## Workflows

### Workflow 1: Customer Purchase Flow
1. User registers or logs in
2. User browses products
3. User adds item to cart or selects product
4. User submits order
5. Order is saved in database
6. User sees confirmation or order history

### Workflow 2: Admin Management Flow
1. Admin logs in
2. Admin adds or edits a product
3. Product is saved in database
4. Admin views all customer orders
5. Admin updates order status
6. Changes are reflected in the database and visible to users

---

## Security Rules (IMPORTANT)

- Never store passwords in plaintext
- Always hash passwords
- All forms must have server-side validation
- Never trust user input
- Do not rely on hidden fields for security
- Enforce role checks on the server side
- Use safe database queries (avoid raw string concatenation if possible)

NOTE:
The system does NOT need to be perfectly secure.
It should be realistic and analyzable for security testing.

---

## Coding Style Guidelines

- Keep code simple and readable
- Avoid unnecessary abstraction
- Prefer clear route names and small functions
- Add comments only when helpful
- Prioritize understandability over optimization

---

## Project Structure Preference

- app.py
- models.py (or integrated in app.py)
- templates/
- static/
- database (SQLite file)
- README.md
- AI_USAGE.md

---

## Documentation Rules

Whenever making meaningful changes:

Update README.md:
- Setup instructions
- Routes / pages
- Workflows
- Features

Update AI_USAGE.md:
- Prompts used
- Which parts were AI-generated
- What you modified or fixed
- Any security concerns you noticed

---

## Working Rules for Claude

When implementing features:

1. Check if the feature is required for R1–R6
2. Choose the simplest possible implementation
3. Do NOT over-engineer
4. Always enforce server-side authorization
5. Explain security-relevant decisions clearly
6. Keep the code easy for another student team to understand

---

## Additional Notes

- This project will be reviewed by another team
- Code must be understandable within one sitting
- Focus on clarity, correctness, and analyzability
- UI design is NOT important