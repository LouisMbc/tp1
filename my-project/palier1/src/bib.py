import json

class Book:
    def __init__(self, id, author, title, content=None, tag=None, image_ascii=None):
        self.__id = id
        self.__title = title
        self.__author = author
        self.__content = content
        self.__tag = tag
        self.__image_ascii = image_ascii
        
    def to_dict(self):
        return {
            'id': self.__id,
            'title': self.__title,
            'author': self.__author,
            'content': self.__content,
            'tag': self.__tag,
            'image_ascii': self.__image_ascii
        }

class BookStore:
    def __init__(self):
        self.__books = []
        self.__next_id = 1
        
    def add(self, book):
        book._Book__id = self.__next_id
        self.__next_id += 1
        self.__books.append(book)
        
    def remove(self, title, author):
        for book in self.__books[:]:
            if book._Book__title == title and book._Book__author == author:
                self.__books.remove(book)
                return True
        return False
        
    def list(self):
        for book in self.__books:
            print(f"- {book._Book__title} par {book._Book__author}")
            
    def get_book(self, title):
        for book in self.__books:
            if book._Book__title == title:
                return book
        return None

    def to_dict(self):
        return [book.to_dict() for book in self.__books]

class Library(BookStore):
    pass

class User:
    pass

class App:
    def __init__(self):
        self.__actions = {
            'ls': self.list_books,
            'new': self.new_book,
            'del': self.delete_book,
            'get': self.get_book,
            'save': self.save_to_disk,
            'load': self.load_from_disk
        }
        self.__book_store = BookStore()
        self.__library = Library()