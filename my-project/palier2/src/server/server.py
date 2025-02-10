import socket
import json
import pickle
from threading import Thread

class BookStore:
    def __init__(self):
        self.__books = []
        self.__next_id = 1
        
    def add(self, book_data):
        book_data['id'] = self.__next_id
        self.__next_id += 1
        self.__books.append(book_data)
        return True
        
    def remove(self, title, author):
        for book in self.__books[:]:
            if book['title'] == title and book['author'] == author:
                self.__books.remove(book)
                return True
        return False
        
    def list(self):
        return self.__books
            
    def get_book(self, title):
        for book in self.__books:
            if book['title'] == title:
                return book
        return None

class BiblioServer:
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        self.book_store = BookStore()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))

    def start(self):
        self.socket.listen(5)
        print(f"Serveur démarré sur {self.host}:{self.port}")
        
        while True:
            client, address = self.socket.accept()
            print(f"Nouveau client connecté: {address}")
            Thread(target=self.handle_client, args=(client,)).start()

    def handle_client(self, client):
        while True:
            try:
                data = client.recv(4096)
                if not data:
                    break
                
                request = pickle.loads(data)
                response = self.process_request(request)
                client.send(pickle.dumps(response))
            except:
                break
        client.close()

    def process_request(self, request):
        action = request.get('action')
        data = request.get('data', {})
        
        try:
            if action == 'add':
                success = self.book_store.add(data)
                return {
                    'status': 'success' if success else 'error',
                    'message': 'Livre ajouté' if success else 'Erreur lors de l\'ajout'
                }
                
            elif action == 'remove':
                success = self.book_store.remove(data['title'], data['author'])
                return {
                    'status': 'success' if success else 'error',
                    'message': 'Livre supprimé' if success else 'Livre non trouvé'
                }
                
            elif action == 'list':
                books = self.book_store.list()
                return {
                    'status': 'success',
                    'data': books
                }
                
            elif action == 'get_book':
                book = self.book_store.get_book(data['title'])
                return {
                    'status': 'success' if book else 'error',
                    'data': book,
                    'message': None if book else 'Livre non trouvé'
                }
                
            return {'status': 'error', 'message': 'Action non reconnue'}
            
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

def main():
    server = BiblioServer()
    server.start()

if __name__ == '__main__':
    main()