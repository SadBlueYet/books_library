from typing import Type

from config import BOOK_STATUSES
from src.repository import AbstractRepository


class UserInterface:
    def __init__(self, repository: Type[AbstractRepository]):
        self.repository = repository

    def show_menu(self):
        """Show the menu and handle user input."""
        while True:
            print("\n=== Menu ===")
            print("1. Add book")
            print("2. Find books")
            print("3. Delete book")
            print("4. Show all books")
            print("5. Update book status")
            print("0. Exit")

            choice = input("Select an option: ")
            try:
                print("\nPress Ctrl+C at any time to cancel.")
                if choice == "1":
                    self.add_book()
                elif choice == "2":
                    self.get_books()
                elif choice == "3":
                    self.delete_book()
                elif choice == "4":
                    self.show_all_books()
                elif choice == "5":
                    self.update_book_status()
                elif choice == "0":
                    print("Exiting...")
                    break
                else:
                    print("Invalid choice. Please try again.")
            except KeyboardInterrupt:
                pass

    def add_book(self):
        """Add a new book to the library."""
        print("\n=== Adding Book ===")
        title = input("Enter the title of the book\n>> ")
        author = input("Enter the author of the book\n>> ")
        year = input("Enter the year of publication\n>> ")

        if not title or not author or not year.isdigit() or int(year) < 0:
            print(
                "Invalid input. Please provide a valid title, author, and a non-negative year."
            )
            return

        self.repository.add_book(
            {"title": title, "author": author, "year": int(year), "status": "В наличии"}
        )
        print(f"Book '{title}' by {author} added successfully.")

    def get_books(self):
        """
        Find books in the library.

        This method asks the user to select a search criterion and enter a value.
        It then calls the `get_books` method of the repository and prints the
        results.
        """
        print("\n=== Find books ===")
        choice = input("1. Find by title\n2. Find by author\n3. Find by year\n>> ")
        match choice:
            case "1":
                title = input("Enter the title of the book\n>> ")
                books = self.repository.get_books({"title": title})
            case "2":
                author = input("Enter the author of the book\n>> ")
                books = self.repository.get_books({"author": author})
            case "3":
                year = input("Enter the year of publication\n>> ")
                if not year.isdigit() or int(year) < 0:
                    print("Invalid input. Please provide a valid non-negative year.")
                    return
                books = self.repository.get_books({"year": int(year)})
            case _:
                print("Invalid choice. Please try again.")
                return

        self._print_books_table(books)

    def delete_book(self):
        """Delete a book by its ID."""
        print("\n=== Deleting Book ===")
        book_id = input("Enter the ID of the book to delete\n>> ")
        if not book_id.isdigit():
            print("Book ID must be a number.")
            return

        try:
            self.repository.delete_book(int(book_id))
            print("Book deleted successfully.")
        except ValueError as e:
            print(e)

    def show_all_books(self):
        """
        Show all books.
        Prints a table of all books in the repository.
        """
        print("\n=== All books ===")
        books = self.repository.get_all_books()
        self._print_books_table(books)

    def update_book_status(self):
        """
        Update the status of a book.
        Asks the user to input the ID of the book and the new status.
        """
        print("\n=== Update book status ===")
        book_id = input("Enter the ID of the book to update\n>> ")
        status = input("Enter the new status\n>> ")
        if not book_id.isdigit() or status not in BOOK_STATUSES:
            print("Book ID must be a number. or invalid status. Please choose a valid status. (В наличии, Выдана)")
            return
        try:
            self.repository.update_book_status(int(book_id), status)
            print("Book status updated successfully.")
        except ValueError as e:
            print(e)

    def _print_books_table(self, books: list[dict]):
        """
        Prints books in a nice table format.
        Args:
            books: A list of book dictionaries with keys "id", "title", "author", "year", and "status".
        """
        if not books:
            print("No books found.")
            return

        headers = ["ID", "Title", "Author", "Year", "Status"]

        column_widths = {
            "ID": max(len(str(book.get("id", ""))) for book in books + [{"id": headers[0]}]),
            "Title": max(len(book.get("title", "")) for book in books + [{"title": headers[1]}]),
            "Author": max(len(book.get("author", "")) for book in books + [{"author": headers[2]}]),
            "Year": max(len(str(book.get("year", ""))) for book in books + [{"year": headers[3]}]),
            "Status": max(len(book.get("status", "")) for book in books + [{"status": headers[4]}]),
        }

        header_row = " | ".join(header.ljust(column_widths[header]) for header in headers)
        print(header_row)
        print("-" * len(header_row))

        for book in books:
            row = " | ".join(
                [
                    str(book.get("id", "")).ljust(column_widths["ID"]),
                    book.get("title", "").ljust(column_widths["Title"]),
                    book.get("author", "").ljust(column_widths["Author"]),
                    str(book.get("year", "")).ljust(column_widths["Year"]),
                    book.get("status", "Не указан").ljust(column_widths["Status"]),
                ]
            )
            print(row)
