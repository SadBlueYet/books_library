from typing import Type
from repository import AbstractRepository


class Service:
    def __init__(self, repository: Type[AbstractRepository]) -> None:
        self.repository = repository

    def add_book(self, book: dict) -> None:
        self.repository.add_book(book)

    def get_books(self, filter_by: dict) -> list[dict]:
        return self.repository.get_books(filter_by)

    def update_book_status(self, book_id: int, status: str) -> None:
        self.repository.update_book_status(book_id, status)

    def delete_book(self, book_id: int) -> None:
        self.repository.delete_book(book_id)

    def get_all_books(self) -> list:
        return self.repository.get_all_books()
