import socket
import pickle

class BiblioClient:
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        self.socket = None

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect((self.host, self.port))
            return True
        except:
            return False

    def send_request(self, action, data=None):
        if not self.socket:
            if not self.connect():
                return {'status': 'error', 'message': 'Non connecté au serveur'}
        
        request = {
            'action': action,
            'data': data or {}
        }
        try:
            self.socket.send(pickle.dumps(request))
            response = pickle.loads(self.socket.recv(4096))
            return response
        except:
            return {'status': 'error', 'message': 'Erreur de communication'}

    def add(self, book):
        return self.send_request('add', book.to_dict())

    def remove(self, title, author):
        return self.send_request('remove', {
            'title': title,
            'author': author
        })

    def list(self):
        return self.send_request('list')

    def get_book(self, title):
        return self.send_request('get_book', {'title': title})

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