from flask import Flask, render_template, request
from main import Library

app = Flask(__name__)

# Route for the home page that displays available and borrowed books
@app.route('/')
def home():
    library = Library()
    available = library.list_available_books()  # Get the list of available books
    borrowed = library.list_borrowed_books()  # Get the list of borrowed books
    library.close()  # Close the database connection or resources
    return render_template('home.html', available=available, borrowed=borrowed)

# Route for the 'Add Book' page that displays all books
@app.route('/add')
def add():
    library = Library()
    all_books = library.list_books()  # List all books in the library
    library.close()  # Close the library resource after operation
    return render_template('add_book.html', all_books=all_books)

# Route to handle the form submission for adding a new book
@app.route('/submit_add', methods=['POST'])
def submit_add():
    title = request.form['title']  # Extract book title from form
    author = request.form['author']  # Extract author from form
    year = request.form['year']  # Extract publication year from form

    library = Library()
    message = library.add_book(title, author, year)  # Add the book to the library
    library.close()  # Ensure resource cleanup

    return render_template('report.html', message=message)  # Show a report to the user

# Route for borrowing a book, lists all available books
@app.route('/borrow')
def borrow():
    library = Library()
    message = library.list_available_books()  # Get available books for borrowing
    library.close()  # Close the library resource
    return render_template('borrow_book.html', message=message)

# Route to handle form submission for borrowing a book
@app.route('/submit_borrow', methods=['POST'])
def submit_borrow():
    title = request.form['title']  # Extract the title of the book to be borrowed
    borrower = request.form['borrower']  # Extract the borrower's name

    library = Library()
    message = library.borrow_book(title, borrower)  # Perform the borrowing operation
    library.close()  # Close the library resource

    return render_template('report.html', message=message)

# Route to return a borrowed book
@app.route('/return_book', methods=['POST'])
def return_book():
    library = Library()
    book_title = request.form.get('book_title')  # Get the book title from the form
    title = book_title.split(" by")[0].strip()  # Extract the title from the formatted string
    message = library.return_book(title)  # Return the book to the library
    library.close()  # Close the library resource

    return render_template('report.html', message=message)

# Run the app in debug mode when executed directly
if __name__ == '__main__':
    app.run(debug=True)
