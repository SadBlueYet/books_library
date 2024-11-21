# books_library

This is a library management system. It is a console application that allows you to store, retrieve, update and delete books in a library. The application is using a JSON file for data storage. The system allows you to view the list of books, add new books, delete books and update book status.

## Features

- Add new book
- Delete book
- Update book status
- View list of books

## How to Use the Library Management System

1. **Start the Application**: 
   - ```python main.py```

2. **Menu Options**:
   - **Add Book**: Select this option to add a new book to the library. You will be prompted to enter the book's title, author, and year of publication.
   - **Find Books**: Use this option to search for books by title, author, or year.
   - **Delete Book**: Choose this to remove a book from the library by entering its ID.
   - **Show All Books**: Displays a list of all the books currently in the library.
   - **Update Book Status**: Select this to change the status of a book (e.g., from "В наличии" to "Выдана").
   - **Exit**: Close the application.

3. **Controls**:
   - Input the corresponding number for the menu option you wish to select.
   - Follow the on-screen prompts and input instructions.
   - Use `Ctrl+C` at any time to cancel the current operation or exit the application.

4. **Data Storage**:
   - All book data is stored in a JSON file, ensuring persistent storage across sessions.