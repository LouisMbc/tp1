from bib import BiblioClient, Book

def menu():
    print("\n=== Bibliothèque Client/Serveur ===")
    print("1. Ajouter un livre")
    print("2. Supprimer un livre")
    print("3. Afficher tous les livres")
    print("4. Afficher détail d'un livre")
    print("5. Quitter")
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
            
            livre = Book(0, auteur, titre, tag=tag, image_ascii=image_ascii)
            response = client.add(livre)
            print(response.get('message'))
            
        elif choix == "2":
            titre = input("Titre: ")
            auteur = input("Auteur: ")
            response = client.remove(titre, auteur)
            print(response.get('message'))
            
        elif choix == "3":
            response = client.list()
            if response['status'] == 'success':
                for livre in response['data']:
                    print(f"- {livre['title']} par {livre['author']}")
            else:
                print("Erreur:", response.get('message'))
                
        elif choix == "4":
            titre = input("Titre du livre: ")
            response = client.get_book(titre)
            if response['status'] == 'success':
                book = response['data']
                print(f"\nDétails du livre:")
                print(f"Titre: {book['title']}")
                print(f"Auteur: {book['author']}")
                print(f"Tag: {book['tag']}")
                if book['image_ascii']:
                    print("Image ASCII:")
                    print(book['image_ascii'])
            else:
                print("Livre non trouvé")
                
        elif choix == "5":
            break

if __name__ == "__main__":
    main()