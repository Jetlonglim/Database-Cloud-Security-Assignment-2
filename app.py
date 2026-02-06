import logging
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
# FIX: Only importing BookForm now
from forms import BookForm 

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Secure Connection String to VM
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://db_admin:Admin123!@192.168.0.130/LibraryDB?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes'

db = SQLAlchemy(app)

# Configure audit logging for Task 5
logging.basicConfig(
    filename='audit.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    filemode='a'
)

# Focused Model: Only Book remains
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default='Available')

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'password'

with app.app_context():
    # This will create the Book table if it doesn't exist
    db.create_all()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']

    # Admin access check for Library Management
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        session['admin'] = True
        logging.info(f"Admin logged in successfully.")
        return redirect(url_for('index'))

    logging.warning(f"Failed login attempt: {username}")
    return "Invalid credentials", 403

@app.route('/dashboard')
def index():
    if not session.get('admin'):
        return redirect(url_for('login'))
    
    # Fetch only books for the dashboard
    books = Book.query.all()
    return render_template('index.html', books=books)

@app.route('/add-book', methods=['GET', 'POST'])
def add_book():
    if not session.get('admin'):
        return redirect(url_for('login'))
    
    form = BookForm()
    if form.validate_on_submit():
        new_book = Book(
            title=form.title.data, 
            author=form.author.data, 
            isbn=form.isbn.data
        )
        db.session.add(new_book)
        db.session.commit()
        
        # Security: Audit log tracks book additions
        logging.info(f"Admin added book: {form.title.data} (ISBN: {form.isbn.data})")
        return redirect(url_for('index'))
        
    return render_template('add_book.html', form=form)

@app.route('/edit-book/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    if not session.get('admin'):
        return redirect(url_for('login'))

    book = Book.query.get_or_404(book_id)
    form = BookForm(obj=book) # Pre-fills the form with current book data

    if form.validate_on_submit():
        book.title = form.title.data
        book.author = form.author.data
        book.isbn = form.isbn.data
        db.session.commit()
        
        # Security: Audit the update action
        logging.info(f"Admin updated book ID {book.id}: {book.title}")
        return redirect(url_for('index'))

    return render_template('edit_book.html', form=form, book=book)

@app.route('/delete-book/<int:book_id>')
def delete_book(book_id):
    if not session.get('admin'):
        return redirect(url_for('login'))
    
    book = Book.query.get_or_404(book_id)
    book_title = book.title
    
    db.session.delete(book)
    db.session.commit()
    
    # Security: Audit log tracks data removal
    logging.info(f"Admin deleted book: {book_title} (ID: {book_id})")
    
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    logging.info("Admin logged out.")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)