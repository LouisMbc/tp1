from bib import BiblioClient, Livre

def menu():
    print("\n=== Bibliothèque Client/Serveur ===")
    print("1. Ajouter un livre")
    print("2. Supprimer un livre")
    print("3. Afficher tous les livres")
    print("4. Quitter")
    return input("Choix: ")

def main():
    client = BiblioClient()
    
    if not client.connect():
        print("Impossible de se connecter au serveur")
        return
        
    print("Connecté au serveur")
    
    while True:
        choix = menu()
        if choix == "1":
            titre = input("Titre: ")
            auteur = input("Auteur: ")
            tag = input("Tag: ")
            print("Image ASCII (terminez par une ligne vide):")
            lignes = []
            while True:
                ligne = input()
                if not ligne:
                    break
                lignes.append(ligne)
            image_ascii = "\n".join(lignes) if lignes else None
            
            livre = Livre(titre, auteur, tag, image_ascii)
            response = client.ajouter_livre(livre)
            print(response.get('message'))
            
        elif choix == "2":
            titre = input("Titre: ")
            auteur = input("Auteur: ")
            response = client.supprimer_livre(titre, auteur)
            print(response.get('message'))
            
        elif choix == "3":
            response = client.liste_livres()
            if response['status'] == 'success':
                for livre in response['data']:
                    print(f"- {livre['titre']} par {livre['auteur']}")
            
        elif choix == "4":
            break

if __name__ == "__main__":
    main()