import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

import unittest

from config import TEST_LIBRARY_PATH
from src.repository import JsonRepository


class TestJsonRepository(unittest.TestCase):
    def setUp(self):
        self.repository = JsonRepository(TEST_LIBRARY_PATH)

    @classmethod
    def tearDownClass(cls):
        os.remove(TEST_LIBRARY_PATH)

    def test_a_load_books_empty(self):
        data = self.repository._load_books()
        self.assertEqual(data, {"max_id": 0, "books": []})

    def test_add_book(self):
        new_book = {"title": "Book 1", "author": "Author 1", "year": 2001, "status": "В наличии"}
        self.repository.add_book(new_book)
        expected_data = [{"id": 1, "title": "Book 1", "author": "Author 1", "year": 2001, "status": "В наличии"}]
        books = self.repository.get_books({"title": "Book 1"})
        self.assertEqual(books, expected_data)

    def test_delete_book(self):
        with self.assertRaises(ValueError):
            self.repository.delete_book(1000)
        new_book = {"title": "Book 2", "author": "Author 2", "year": 2002, "status": "В наличии"}
        book_id = self.repository.add_book(new_book)
        self.repository.delete_book(book_id)
        books = self.repository.get_books({"title": "Book 2"})
        self.assertEqual(books, [])

    def test_get_books(self):
        new_book = {"title": "Book 3", "author": "Author 3", "year": 2003, "status": "В наличии"}
        self.repository.add_book(new_book)
        result = self.repository.get_books({"author": "Author 3"})
        self.assertEqual(result, [new_book,])

    def test_z_get_all_books(self):
        result = self.repository.get_all_books()
        self.assertNotEqual(len(result), 0)

if __name__ == "__main__":
    unittest.main()
