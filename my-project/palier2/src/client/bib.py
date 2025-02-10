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

    def ajouter_livre(self, livre):
        return self.send_request('ajouter_livre', {
            'titre': livre.titre,
            'auteur': livre.auteur,
            'tag': livre.tag,
            'image_ascii': livre.image_ascii
        })

    def supprimer_livre(self, titre, auteur):
        return self.send_request('supprimer_livre', {
            'titre': titre,
            'auteur': auteur
        })

    def liste_livres(self):
        return self.send_request('liste_livres')

class Livre:
    def __init__(self, titre, auteur, tag=None, image_ascii=None):
        self.titre = titre
        self.auteur = auteur
        self.tag = tag
        self.image_ascii = image_ascii