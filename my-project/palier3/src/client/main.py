from bib import BiblioClient, Book
import sys

def menu():
    print("\n=== Bibliothèque 3-Tier ===")
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
        try:
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
                response = client.send_request('add', livre.to_dict())
                print(response.get('message'))
                
            elif choix == "2":
                titre = input("Titre: ")
                auteur = input("Auteur: ")
                response = client.send_request('remove', {
                    'title': titre,
                    'author': auteur
                })
                print(response.get('message'))
                
            elif choix == "3":
                response = client.send_request('list')
                if response['status'] == 'success':
                    for livre in response['data']:
                        print(f"- {livre['title']} par {livre['author']} (Tag: {livre['tag']})")
                else:
                    print("Erreur:", response.get('message'))
                    
            elif choix == "4":
                titre = input("Titre du livre: ")
                response = client.send_request('get_book', {'title': titre})
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
                
        except Exception as e:
            print(f"Erreur: {e}")
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nFermeture du programme")
        sys.exit(0)