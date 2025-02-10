import socket
import json
import pickle
from threading import Thread

class BiblioServer:
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        self.bibliotheque = {}  # {client_id: Bibliotheque()}
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
                action = request.get('action')
                response = self.process_request(request)
                
                client.send(pickle.dumps(response))
            except:
                break
        
        client.close()

    def process_request(self, request):
        action = request.get('action')
        data = request.get('data', {})
        
        if action == 'ajouter_livre':
            # Logique d'ajout de livre
            return {'status': 'success', 'message': 'Livre ajouté'}
        elif action == 'supprimer_livre':
            # Logique de suppression
            return {'status': 'success', 'message': 'Livre supprimé'}
        elif action == 'liste_livres':
            # Retourner la liste des livres
            return {'status': 'success', 'data': []}
        
        return {'status': 'error', 'message': 'Action non reconnue'}

def main():
    server = BiblioServer()
    server.start()

if __name__ == '__main__':
    main()