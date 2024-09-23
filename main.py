import sqlite3
from datetime import datetime

class Library:
    def __init__(self, db_name="library.db"):
        # Initialize the connection to the SQLite database
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()  # Ensure tables are created upon initialization

    def create_tables(self):
        """Create the 'books' and 'borrows' tables if they don't already exist."""
        # Table for books
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS books (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                title TEXT NOT NULL,
                                author TEXT NOT NULL,
                                year INTEGER NOT NULL,
                                is_borrowed BOOLEAN NOT NULL DEFAULT 0)''')

        # Table for borrowing records
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS borrows (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                book_id INTEGER NOT NULL,
                                borrower TEXT NOT NULL,
                                borrow_date TEXT NOT NULL,
                                return_date TEXT,
                                FOREIGN KEY (book_id) REFERENCES books(id))''')
        self.conn.commit()  # Commit the changes to the database

    def add_book(self, title, author, year):
        """Add a new book to the library."""
        if not title or not author:
            return 'Enter the book information!'
        else:
            self.cursor.execute('''INSERT INTO books (title, author, year, is_borrowed)
                                   VALUES (?, ?, ?, ?)''', (title, author, year, False))
            self.conn.commit()
            return f"Book '{title}' has been added to the library."

    def borrow_book(self, title, borrower):
        """Borrow a book by title and record the borrower."""
        # Check if the book is available
        self.cursor.execute('SELECT id, is_borrowed FROM books WHERE title = ?', (title,))
        book = self.cursor.fetchone()

        if book is None:
            return f"Book '{title}' does not exist in the library."
        elif book[1]:
            return f"Book '{title}' is already borrowed."
        else:
            # Mark the book as borrowed
            book_id = book[0]
            borrow_date = datetime.now().strftime('%Y-%m-%d')
            self.cursor.execute('''INSERT INTO borrows (book_id, borrower, borrow_date)
                                   VALUES (?, ?, ?)''', (book_id, borrower, borrow_date))
            self.cursor.execute('''UPDATE books
                                   SET is_borrowed = ?
                                   WHERE id = ?''', (True, book_id))
            self.conn.commit()
            return f"Book '{title}' has been borrowed by {borrower}."

    def return_book(self, title):
        """Return a borrowed book by title."""
        # Find the book by title
        self.cursor.execute('SELECT id, is_borrowed FROM books WHERE title = ?', (title,))
        book = self.cursor.fetchone()

        if book is None:
            return f"Book '{title}' does not exist in the library."
        elif not book[1]:
            return f"Book '{title}' is not currently borrowed."
        else:
            # Mark the book as returned
            book_id = book[0]
            return_date = datetime.now().strftime('%Y-%m-%d')
            self.cursor.execute('''UPDATE borrows
                                   SET return_date = ?
                                   WHERE book_id = ? AND return_date IS NULL''', (return_date, book_id))
            self.cursor.execute('''UPDATE books
                                   SET is_borrowed = ?
                                   WHERE id = ?''', (False, book_id))
            self.conn.commit()
            return f"The book '{title}' has been returned."

    def list_available_books(self):
        """List all available books that are not currently borrowed."""
        self.cursor.execute('SELECT title, author, year FROM books WHERE is_borrowed = ?', (False,))
        books = self.cursor.fetchall()

        if books:
            return [f"{book[0]} by {book[1]} ({book[2]})" for book in books]
        else:
            return "No books are available at the moment."

    def list_borrowed_books(self):
        """List all borrowed books along with borrower information."""
        self.cursor.execute('''SELECT books.title, books.author, borrows.borrower, borrows.borrow_date
                               FROM books
                               JOIN borrows ON books.id = borrows.book_id
                               WHERE books.is_borrowed = ? AND borrows.return_date IS NULL''', (True,))
        books = self.cursor.fetchall()

        if books:
            return [f"{book[0]} by {book[1]}, borrowed by {book[2]} on {book[3]}" for book in books]
        else:
            return "No books are currently borrowed."

    def list_books(self):
        """List all books in the library regardless of borrowing status."""
        self.cursor.execute('SELECT title, author, year FROM books')
        books = self.cursor.fetchall()

        if books:
            return [f"{book[0]} by {book[1]} ({book[2]})" for book in books]
        else:
            return "No books are available at the moment."

    def close(self):
        """Close the connection to the database."""
        self.conn.close()
