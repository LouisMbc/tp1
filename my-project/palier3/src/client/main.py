from bib import BiblioClient, Livre
import sys

def menu():
    print("\n=== Bibliothèque 3-Tier ===")
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
                
                livre = Livre(titre, auteur, tag, image_ascii)
                response = client.send_request('ajouter_livre', livre.to_dict())
                print(response.get('message'))
                
            elif choix == "2":
                titre = input("Titre: ")
                auteur = input("Auteur: ")
                response = client.send_request('supprimer_livre', {
                    'titre': titre,
                    'auteur': auteur
                })
                print(response.get('message'))
                
            elif choix == "3":
                response = client.send_request('liste_livres')
                if response['status'] == 'success':
                    for livre in response['data']:
                        print(f"- {livre['titre']} par {livre['auteur']} (Tag: {livre['tag']})")
                else:
                    print("Erreur:", response.get('message'))
                    
            elif choix == "4":
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