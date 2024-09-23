<!-- @format -->

# Library Management System

This project is a simple **Library Management System** built using **Flask**, a lightweight web framework for Python. The system allows users to manage a collection of books, track borrowed books, and perform common operations like adding, borrowing, and returning books.

## Features

- **List Available Books**: View a list of books that are currently available for borrowing.
- **List Borrowed Books**: View the details of books that have been borrowed, including the borrower's name and the date of borrowing.
- **Add New Books**: Add new books to the library collection by providing a title, author, and publication year.
- **Borrow Books**: Borrow books from the library by specifying the borrower's name and the title of the book.
- **Return Books**: Return borrowed books to the library.

## Technologies Used

- **Flask**: The backend framework used to manage routes and logic.
- **SQLite**: A lightweight database for storing book and borrow records.
- **Bootstrap**: Used for the frontend to create a clean, responsive UI.
- **Jinja2**: The template engine used for rendering HTML pages.

## Installation

To run this project locally, follow the steps below:

1. **Clone the repository**:

   ```bash
   git clone https://github.com/AliFathi1325/Library_Management_System_Flask.git
   ```

2. **Navigate to the project directory**:

   ```bash
   cd library-management-system
   ```

3. **Create a virtual environment** (optional but recommended):

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install the required dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

5. **Run the Flask application**:

   ```bash
   python app.py
   ```

6. Open your browser and go to `http://127.0.0.1:5000` to view the Library Management System.

## Usage

1. **Home Page**: The homepage displays available and borrowed books.
2. **Add a Book**: Navigate to `/add` to add a new book to the library.
3. **Borrow a Book**: Borrow a book from the library by entering the borrower's name and the title of the book.
4. **Return a Book**: Return a borrowed book by entering the book title.

## Database Schema

The system uses **SQLite** as the database with the following schema:

- **books**:

  - `id`: Integer (Primary Key)
  - `title`: Text (Title of the book)
  - `author`: Text (Author of the book)
  - `year`: Integer (Publication year)
  - `is_borrowed`: Boolean (Indicates if the book is currently borrowed)

- **borrows**:
  - `id`: Integer (Primary Key)
  - `book_id`: Foreign Key (References books)
  - `borrower`: Text (Name of the person borrowing the book)
  - `borrow_date`: Text (Date the book was borrowed)
  - `return_date`: Text (Date the book was returned)
