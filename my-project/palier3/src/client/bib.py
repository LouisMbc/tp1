import socket
import pickle
from contextlib import contextmanager

class BiblioClient:
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        self.socket = None

    @contextmanager
    def connection(self):
        try:
            if not self.socket:
                self.connect()
            yield
        except Exception as e:
            print(f"Erreur de connexion: {e}")
            self.socket = None
            raise

    def connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            return True
        except Exception as e:
            print(f"Erreur de connexion: {e}")
            return False

    def send_request(self, action, data=None):
        with self.connection():
            request = {
                'action': action,
                'data': data or {}
            }
            self.socket.send(pickle.dumps(request))
            return pickle.loads(self.socket.recv(4096))

class Livre:
    def __init__(self, titre, auteur, tag=None, image_ascii=None):
        self.titre = titre
        self.auteur = auteur
        self.tag = tag
        self.image_ascii = image_ascii

    def to_dict(self):
        return {
            'titre': self.titre,
            'auteur': self.auteur,
            'tag': self.tag,
            'image_ascii': self.image_ascii
        }