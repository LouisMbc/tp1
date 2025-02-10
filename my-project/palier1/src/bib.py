import json

class Livre:
    def __init__(self, titre, auteur, tag=None, image_ascii=None, contenu=None):
        self.titre = titre
        self.auteur = auteur
        self.tag = tag
        self.image_ascii = image_ascii
        self.contenu = contenu

    def __str__(self):
        return f"{self.titre} par {self.auteur}"
        
    def mettre_a_jour(self, titre=None, auteur=None, contenu=None):
        if titre:
            self.titre = titre
        if auteur:
            self.auteur = auteur
            if contenu:
                self.contenu = contenu
            
    def consulter(self):
        if self.contenu:
            return self.contenu
        return f"Livre: {self.titre} par {self.auteur}"        

    def to_dict(self):
        return {
            'titre': self.titre,
            'auteur': self.auteur,
            'tag': self.tag,
            'image_ascii': self.image_ascii,
            'contenu': self.contenu
        }

class Bibliotheque:
    def __init__(self):
        self.livres = []

    def ajouter_livre(self, livre):
        if self._verifier_livre(livre):
            self.livres.append(livre)
            return True
        return False

    def _verifier_livre(self, livre):
        return bool(livre.titre and livre.auteur)

    def supprimer_livre(self, titre, auteur):
        for livre in self.livres[:]:
            if livre.titre == titre and livre.auteur == auteur:
                self.livres.remove(livre)
                return True
        return False

    def chercher_livre(self, titre=None, auteur=None):
        return [livre for livre in self.livres 
                if (not titre or livre.titre == titre) and 
                (not auteur or livre.auteur == auteur)]

    def afficher_tous_livres(self):
        print("\nListe des livres:")
        for livre in self.livres:
            print(f"- {livre.titre} par {livre.auteur} (Tag: {livre.tag})")

    def afficher_detail_livre(self, titre):
        for livre in self.livres:
            if livre.titre == titre:
                print(f"\nDétails du livre '{livre.titre}':")
                print(f"Auteur: {livre.auteur}")
                print(f"Tag: {livre.tag}")
                if livre.image_ascii:
                    print("Image ASCII:")
                    print(livre.image_ascii)
                return
        print("Livre non trouvé")

    def sauvegarder(self, fichier):
        data = [livre.to_dict() for livre in self.livres]
        with open(fichier, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def charger(self, fichier):
        try:
            with open(fichier, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.livres = [Livre(**livre_data) for livre_data in data]
        except FileNotFoundError:
            print("Aucun fichier de sauvegarde trouvé")