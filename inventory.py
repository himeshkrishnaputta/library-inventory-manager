class Book:
    def __init__(self, title, isbn, author, quantity):
        self.title = title
        self.isbn = isbn
        self.author = author
        self.quantity = quantity

    def __str__(self):
        return f"Title: {self.title}, ISBN: {self.isbn}, Author: {self.author}, Quantity: {self.quantity}"


class LibraryInventory:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        """Add a book to the inventory"""
        self.books.append(book)
        print(f"Book '{book.title}' added successfully.")

    def search_by_title(self, title):
        """Search for books by title"""
        results = [book for book in self.books if title.lower() in book.title.lower()]
        return results if results else None

    def search_by_isbn(self, isbn):
        """Search for a book by ISBN"""
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None

    def display_all(self):
        """Display all books in the inventory"""
        if not self.books:
            print("no books in the inventory")
            return
        for book in self.books:
            print(book)