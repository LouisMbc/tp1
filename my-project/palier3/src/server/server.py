import socket
import json
import pickle
from threading import Thread
from ..database.db import BiblioDatabase

class BiblioServer:
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.db = BiblioDatabase()

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
            except Exception as e:
                print(f"Erreur: {e}")
                break
        client.close()

    def process_request(self, request):
        action = request.get('action')
        data = request.get('data', {})
        
        try:
            if action == 'add':
                success = self.db.ajouter_livre(data)
                return {
                    'status': 'success' if success else 'error',
                    'message': 'Livre ajouté' if success else 'Erreur lors de l\'ajout'
                }
                
            elif action == 'remove':
                success = self.db.supprimer_livre(data['title'], data['author'])
                return {
                    'status': 'success' if success else 'error',
                    'message': 'Livre supprimé' if success else 'Livre non trouvé'
                }
                
            elif action == 'list':
                livres = self.db.liste_livres()
                return {
                    'status': 'success',
                    'data': livres
                }
                
            elif action == 'get_book':
                books = self.db.liste_livres()
                book = next((b for b in books if b['title'] == data['title']), None)
                return {
                    'status': 'success' if book else 'error',
                    'data': book,
                    'message': None if book else 'Livre non trouvé'
                }
                
            return {'status': 'error', 'message': 'Action non reconnue'}
            
        except Exception as e:
            return {'status': 'error', 'message': str(e)}