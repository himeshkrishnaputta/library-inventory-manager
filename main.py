import json
import logging
from pathlib import Path
from typing import Optional, List

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ===== Task 1: Book Class =====
class Book:
    def __init__(self, title: str, author: str, isbn: str, status: str = "available"):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.status = status
    
    def __str__(self) -> str:
        return f"'{self.title}' by {self.author} (ISBN: {self.isbn}) - {self.status.upper()}"
    
    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "status": self.status
        }
    
    def issue(self) -> bool:
        if self.is_available():
            self.status = "issued"
            logger.info(f"Book issued: {self.title}")
            return True
        return False
    
    def return_book(self) -> bool:
        if self.status == "issued":
            self.status = "available"
            logger.info(f"Book returned: {self.title}")
            return True
        return False
    
    def is_available(self) -> bool:
        return self.status == "available"
    
    {
    "books": [
        {
            "title": "The Great Gatsby",
            "author": "F. Scott Fitzgerald",
            "isbn": "978-0-7432-7356-5",
            "status": "available"
        },
        {
            "title": "To Kill a Mockingbird",
            "author": "Harper Lee",
            "isbn": "978-0-06-112008-4",
            "status": "issued"
        },
        {
            "title": "1984",
            "author": "George Orwell",
            "isbn": "978-0-451-52494-2",
            "status": "available"
        }
    ]
}

# ===== Task 2: Inventory Manager =====
class LibraryInventory:
    def __init__(self, filepath: str = "library_catalog.json"):
        self.filepath = Path(filepath)
        self.books: List[Book] = []
        self.load_catalog()
    
    def add_book(self, book: Book) -> bool:
        if not self.search_by_isbn(book.isbn):
            self.books.append(book)
            logger.info(f"Book added: {book.title}")
            self.save_catalog()
            return True
        logger.warning(f"Book with ISBN {book.isbn} already exists")
        return False
    
    def search_by_title(self, title: str) -> List[Book]:
        return [b for b in self.books if title.lower() in b.title.lower()]
    
    def search_by_isbn(self, isbn: str) -> Optional[Book]:
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None
    
    def display_all(self) -> None:
        if not self.books:
            print("no books in the inventory")
            return
        for i, book in enumerate(self.books, 1):
            print(f"{i}. {book}")
    
    def save_catalog(self) -> None:
        try:
            with open(self.filepath, 'w') as f:
                json.dump([b.to_dict() for b in self.books], f, indent=2)
            logger.info(f"Catalog saved to {self.filepath}")
        except Exception as e:
            logger.error(f"Failed to save catalog: {e}")
    
    def load_catalog(self) -> None:
        try:
            if self.filepath.exists():
                with open(self.filepath, 'r') as f:
                    data = json.load(f)
                    self.books = [Book(**item) for item in data]
                logger.info(f"Catalog loaded from {self.filepath}")
            else:
                logger.info("No existing catalog found. Starting fresh.")
        except json.JSONDecodeError:
            logger.error("Corrupted JSON file. Starting fresh.")
        except Exception as e:
            logger.error(f"Error loading catalog: {e}")

# ===== Task 4 & 5: CLI with Exception Handling =====
def main():
    inventory = LibraryInventory()
    
    while True:
        try:
            print("\n=== Library Inventory Manager ===")
            print("1. Add Book")
            print("2. Issue Book")
            print("3. Return Book")
            print("4. View All Books")
            print("5. Search by Title")
            print("6. Search by ISBN")
            print("7. Exit")
            
            choice = input("Enter your choice (1-7): ").strip()
            
            if choice == '1':
                try:
                    title = input("Enter book title: ").strip()
                    author = input("Enter author name: ").strip()
                    isbn = input("Enter ISBN: ").strip()
                    if title and author and isbn:
                        inventory.add_book(Book(title, author, isbn))
                        print("Book added successfully!")
                    else:
                        print("Error: All fields are required.")
                except Exception as e:
                    logger.error(f"Error adding book: {e}")
                    print(f"Error: {e}")
            
            elif choice == '2':
                try:
                    isbn = input("Enter ISBN of book to issue: ").strip()
                    book = inventory.search_by_isbn(isbn)
                    if book:
                        if book.issue():
                            inventory.save_catalog()
                            print("Book issued successfully!")
                        else:
                            print("Book is not available.")
                    else:
                        print("Book not found.")
                except Exception as e:
                    logger.error(f"Error issuing book: {e}")
                    print(f"Error: {e}")
            
            elif choice == '3':
                try:
                    isbn = input("Enter ISBN of book to return: ").strip()
                    book = inventory.search_by_isbn(isbn)
                    if book:
                        if book.return_book():
                            inventory.save_catalog()
                            print("Book returned successfully!")
                        else:
                            print("Book was not issued.")
                    else:
                        print("Book not found.")
                except Exception as e:
                    logger.error(f"Error returning book: {e}")
                    print(f"Error: {e}")
            
            elif choice == '4':
                inventory.display_all()
            
            elif choice == '5':
                try:
                    title = input("Enter title to search: ").strip()
                    results = inventory.search_by_title(title)
                    if results:
                        for book in results:
                            print(book)
                    else:
                        print("No books found.")
                except Exception as e:
                    logger.error(f"Error searching by title: {e}")
                    print(f"Error: {e}")
            
            elif choice == '6':
                try:
                    isbn = input("Enter ISBN to search: ").strip()
                    book = inventory.search_by_isbn(isbn)
                    if book:
                        print(book)
                    else:
                        print("Book not found.")
                except Exception as e:
                    logger.error(f"Error searching by ISBN: {e}")
                    print(f"Error: {e}")
            
            elif choice == '7':
                print("Thank you for using Library Inventory Manager. Goodbye!")
                logger.info("Application closed.")
                break
            
            else:
                print("Invalid choice. Please enter 1-7.")
        
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()