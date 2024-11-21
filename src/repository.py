import json
import os
from abc import ABC, abstractmethod

from config import LIBRARY_PATH


class AbstractRepository(ABC):
    @abstractmethod
    def add_book(self, book: dict) -> int:
        pass

    @abstractmethod
    def get_book(self, book_id: int) -> list[dict]:
        pass

    @abstractmethod
    def delete_book(self, book_id: int) -> None:
        pass

    @abstractmethod
    def get_all_books(self) -> list:
        pass


class JsonRepository:

    def __init__(self, library_path: str = LIBRARY_PATH):
        self.library_path = library_path

    def _load_books(self) -> dict[str, int | list]:
        """
        Load books from library file.
        :return:
            dict[str, int | list]: A dictionary with a single key "max_id" of type int
            and a key "books" of type list of dictionaries.
        """
        if not os.path.exists(self.library_path):
            return {"max_id": 0, "books": []}

        with open(self.library_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            if "max_id" not in data:
                data["max_id"] = 0
            return data

    def _save_books(self, data: dict) -> None:
        """
        Save the books to a JSON file.

        :param data: A dictionary with two keys: "max_id" and "books". 
        The value of "max_id" is the highest id of the books, and the value of "books"
        is a list of dictionaries, each containing the details of a book.
        :return: None
        """
        with open(self.library_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def add_book(self, book: dict) -> int:
        """
        Add a new book to the library.

        :param book: A dictionary containing the details of the book to add.
        :return: The ID of the added book.
        :raises ValueError: If the book is already in the library.
        """
        data = self._load_books()
        data["max_id"] += 1
        book["id"] = data["max_id"]
        data["books"].append(book)
        self._save_books(data)
        return book["id"]

    def get_books(self, filter_by: dict) -> list:
        """
        Retrieve all books from the library that match the given filter.
        :param filter_by: A dictionary containing values to filter books by.
        :return: A list of dictionaries, each representing a book with its details.
        """
        data = self._load_books()
        filtered_books = []

        for book in data["books"]:
            if all(book.get(key) == value for key, value in filter_by.items()):
                filtered_books.append(book)

        return filtered_books

    def delete_book(self, book_id: int) -> None:
        """
        Delete a book with the given book_id from the library.

        :param book_id: The ID of the book to delete.
        :raises ValueError: If no book with the given book_id is found.
        """
        data = self._load_books()
        original_length = len(data["books"])
        data["books"] = [book for book in data["books"] if book["id"] != book_id]

        if len(data["books"]) == original_length:
            raise ValueError(f"Book with ID {book_id} not found.")

        self._save_books(data)

    def update_book_status(self, book_id: int, status: str) -> None:
        """
        Update the status of a book with the given book_id.
        :param book_id: The ID of the book to update.
        :param status: The new status to assign to the book.
        :raises ValueError: If no book with the given book_id is found.
        """
        data = self._load_books()
        for book in data["books"]:
            if book["id"] == book_id:
                book["status"] = status
                self._save_books(data)
                return
        raise ValueError(f"Book with ID {book_id} not found.")

    def get_all_books(self) -> list[dict]:
        """
        Retrieve all books from the library.
        :return: A list of dictionaries, each representing a book with its details such as
        "id", "title", "author", "year", and "status".
        """
        data = self._load_books()
        return data["books"]
