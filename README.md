# MiniShop – Multi-User Mock Shopping Platform

A small Flask + SQLite web application built for Secure Software Engineering Phase 0.

## Setup

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install flask
python app.py
```

Visit: http://127.0.0.1:5000

## Default Accounts

| Role  | Username | Password  |
|-------|----------|-----------|
| Admin | admin    | admin123  |

Customers can self-register at /register.

## Pages

| URL                         | Access    | Description              |
|-----------------------------|-----------|--------------------------|
| /products                   | Public    | Product listing          |
| /register                   | Public    | Create customer account  |
| /login                      | Public    | Login                    |
| /order/<id>                 | Customer  | Place an order           |
| /orders                     | Customer  | Order history            |
| /admin                      | Admin     | Dashboard                |
| /admin/products             | Admin     | Manage products          |
| /admin/products/add         | Admin     | Add product              |
| /admin/products/edit/<id>   | Admin     | Edit product             |
| /admin/orders               | Admin     | View and update orders   |

## Workflows

### Workflow 1 – Customer Purchase
1. Register or log in
2. Browse products at /products
3. Click Order on a product
4. Enter quantity and confirm
5. View order at /orders

### Workflow 2 – Admin Management
1. Log in as admin
2. Add/edit/delete products at /admin/products
3. View all customer orders at /admin/orders
4. Update order status (pending → shipped → delivered)

## Course Requirements

| #  | Requirement                          | How satisfied                              |
|----|--------------------------------------|--------------------------------------------|
| R1 | At least 2 user roles                | customer, admin (enforced server-side)     |
| R2 | Persistent storage                   | SQLite via sqlite3                         |
| R3 | At least 2 forms with server-side validation | Register, Login, Order, Add/Edit Product |
| R4 | At least 4 distinct pages            | 9 pages total                              |
| R5 | At least 2 end-to-end workflows      | Customer purchase, Admin management        |
| R6 | AI usage documented                  | See AI_USAGE.md                            |
