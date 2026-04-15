from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from models import get_db, init_db

app = Flask(__name__)
app.secret_key = 'change-this-in-production'


# ---------------------------------------------------------------------------
# Auth helpers
# ---------------------------------------------------------------------------

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in first.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in first.', 'error')
            return redirect(url_for('login'))
        if session.get('role') != 'admin':
            flash('Admin access only.', 'error')
            return redirect(url_for('products'))
        return f(*args, **kwargs)
    return decorated


# ---------------------------------------------------------------------------
# Auth routes
# ---------------------------------------------------------------------------

@app.route('/')
def index():
    return redirect(url_for('products'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        # Server-side validation
        if not username or not password:
            flash('Username and password are required.', 'error')
            return render_template('register.html')
        if len(username) < 3:
            flash('Username must be at least 3 characters.', 'error')
            return render_template('register.html')
        if len(password) < 6:
            flash('Password must be at least 6 characters.', 'error')
            return render_template('register.html')

        db = get_db()
        existing = db.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone()
        if existing:
            db.close()
            flash('Username already taken.', 'error')
            return render_template('register.html')

        db.execute(
            'INSERT INTO users (username, password, role) VALUES (?, ?, ?)',
            (username, generate_password_hash(password), 'customer')
        )
        db.commit()
        db.close()
        flash('Account created. Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        if not username or not password:
            flash('Username and password are required.', 'error')
            return render_template('login.html')

        db = get_db()
        user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        db.close()

        if not user or not check_password_hash(user['password'], password):
            flash('Invalid username or password.', 'error')
            return render_template('login.html')

        session.clear()
        session['user_id'] = user['id']
        session['username'] = user['username']
        session['role'] = user['role']

        if user['role'] == 'admin':
            return redirect(url_for('admin_dashboard'))
        return redirect(url_for('products'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))


# ---------------------------------------------------------------------------
# Customer routes
# ---------------------------------------------------------------------------

@app.route('/products')
def products():
    db = get_db()
    product_list = db.execute('SELECT * FROM products').fetchall()
    db.close()
    return render_template('products.html', products=product_list)


@app.route('/order/<int:product_id>', methods=['GET', 'POST'])
@login_required
def order(product_id):
    db = get_db()
    product = db.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
    if not product:
        db.close()
        flash('Product not found.', 'error')
        return redirect(url_for('products'))

    if request.method == 'POST':
        quantity_str = request.form.get('quantity', '').strip()

        # Server-side validation
        if not quantity_str.isdigit() or int(quantity_str) < 1:
            flash('Quantity must be a positive number.', 'error')
            return render_template('order.html', product=product)

        quantity = int(quantity_str)
        db.execute(
            'INSERT INTO orders (user_id, product_id, quantity, status) VALUES (?, ?, ?, ?)',
            (session['user_id'], product_id, quantity, 'pending')
        )
        db.commit()
        db.close()
        flash('Order placed successfully!', 'success')
        return redirect(url_for('order_history'))

    db.close()
    return render_template('order.html', product=product)


@app.route('/orders')
@login_required
def order_history():
    db = get_db()
    orders = db.execute('''
        SELECT orders.id, products.name, products.price,
               orders.quantity, orders.status
        FROM orders
        JOIN products ON orders.product_id = products.id
        WHERE orders.user_id = ?
        ORDER BY orders.id DESC
    ''', (session['user_id'],)).fetchall()
    db.close()
    return render_template('order_history.html', orders=orders)


# ---------------------------------------------------------------------------
# Admin routes
# ---------------------------------------------------------------------------

@app.route('/admin')
@admin_required
def admin_dashboard():
    db = get_db()
    product_count = db.execute('SELECT COUNT(*) FROM products').fetchone()[0]
    order_count = db.execute('SELECT COUNT(*) FROM orders').fetchone()[0]
    db.close()
    return render_template('admin/dashboard.html',
                           product_count=product_count,
                           order_count=order_count)


@app.route('/admin/products')
@admin_required
def admin_products():
    db = get_db()
    product_list = db.execute('SELECT * FROM products').fetchall()
    db.close()
    return render_template('admin/products.html', products=product_list)


@app.route('/admin/products/add', methods=['GET', 'POST'])
@admin_required
def admin_add_product():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        price_str = request.form.get('price', '').strip()
        description = request.form.get('description', '').strip()

        # Server-side validation
        error = None
        if not name:
            error = 'Product name is required.'
        elif not price_str:
            error = 'Price is required.'
        else:
            try:
                price = float(price_str)
                if price <= 0:
                    error = 'Price must be greater than zero.'
            except ValueError:
                error = 'Price must be a valid number.'
        if not description:
            error = 'Description is required.'

        if error:
            flash(error, 'error')
            return render_template('admin/product_form.html', action='Add', product=None)

        db = get_db()
        db.execute('INSERT INTO products (name, price, description) VALUES (?, ?, ?)',
                   (name, price, description))
        db.commit()
        db.close()
        flash('Product added.', 'success')
        return redirect(url_for('admin_products'))

    return render_template('admin/product_form.html', action='Add', product=None)


@app.route('/admin/products/edit/<int:product_id>', methods=['GET', 'POST'])
@admin_required
def admin_edit_product(product_id):
    db = get_db()
    product = db.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
    if not product:
        db.close()
        flash('Product not found.', 'error')
        return redirect(url_for('admin_products'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        price_str = request.form.get('price', '').strip()
        description = request.form.get('description', '').strip()

        error = None
        if not name:
            error = 'Product name is required.'
        elif not price_str:
            error = 'Price is required.'
        else:
            try:
                price = float(price_str)
                if price <= 0:
                    error = 'Price must be greater than zero.'
            except ValueError:
                error = 'Price must be a valid number.'
        if not description:
            error = 'Description is required.'

        if error:
            db.close()
            flash(error, 'error')
            return render_template('admin/product_form.html', action='Edit', product=product)

        db.execute('UPDATE products SET name = ?, price = ?, description = ? WHERE id = ?',
                   (name, price, description, product_id))
        db.commit()
        db.close()
        flash('Product updated.', 'success')
        return redirect(url_for('admin_products'))

    db.close()
    return render_template('admin/product_form.html', action='Edit', product=product)


@app.route('/admin/products/delete/<int:product_id>', methods=['POST'])
@admin_required
def admin_delete_product(product_id):
    db = get_db()
    db.execute('DELETE FROM products WHERE id = ?', (product_id,))
    db.commit()
    db.close()
    flash('Product deleted.', 'success')
    return redirect(url_for('admin_products'))


@app.route('/admin/orders')
@admin_required
def admin_orders():
    db = get_db()
    orders = db.execute('''
        SELECT orders.id, users.username, products.name AS product_name,
               orders.quantity, orders.status
        FROM orders
        JOIN users    ON orders.user_id    = users.id
        JOIN products ON orders.product_id = products.id
        ORDER BY orders.id DESC
    ''').fetchall()
    db.close()
    return render_template('admin/orders.html', orders=orders)


@app.route('/admin/orders/update/<int:order_id>', methods=['POST'])
@admin_required
def admin_update_order(order_id):
    status = request.form.get('status', '').strip()
    allowed = {'pending', 'shipped', 'delivered', 'cancelled'}

    # Server-side validation
    if status not in allowed:
        flash('Invalid status.', 'error')
        return redirect(url_for('admin_orders'))

    db = get_db()
    db.execute('UPDATE orders SET status = ? WHERE id = ?', (status, order_id))
    db.commit()
    db.close()
    flash('Order status updated.', 'success')
    return redirect(url_for('admin_orders'))


# ---------------------------------------------------------------------------

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
