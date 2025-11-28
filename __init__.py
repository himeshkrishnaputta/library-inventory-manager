class LibraryInventoryManager:
    def __init__(self, library_name: str):
        """
        Initialize the Library Inventory Manager.
        
        Args:
            library_name (str): The name of the library
        """
        self.library_name = library_name
        self.books = {}  # Dictionary to store book_id: book_details
        self.members = {}  # Dictionary to store member_id: member_details
        self.checkouts = []  # List to track book checkouts
        
    def add_book(self, book_id: str, title: str, author: str, quantity: int):
        """Add a book to the inventory"""
        self.books[book_id] = {
            'title': title,
            'author': author,
            'quantity': quantity
        }
    
    def add_member(self, member_id: str, name: str):
        """Add a library member"""
        self.members[member_id] = {'name': name}