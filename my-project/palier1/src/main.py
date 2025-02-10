from bib import Livre, Bibliotheque

def menu():
    print("\n=== Bibliothèque Locale ===")    
    print("1. Ajouter un livre")
    print("2. Supprimer un livre")
    print("3. Afficher tous les livres")
    print("4. Afficher détail d'un livre")
    print("5. Sauvegarder la bibliothèque")
    print("6. Charger la bibliothèque")
    print("7. Quitter")
    return input("Choix: ")

def main():
    biblio = Bibliotheque()
    fichier_json = "../data/bibliotheque.json"
    
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
            
            livre = Livre(titre, auteur, tag=tag, image_ascii=image_ascii)
            biblio.ajouter_livre(livre)
            print("Livre ajouté avec succès")
            
        elif choix == "2":
            titre = input("Titre: ")
            auteur = input("Auteur: ")
            if biblio.supprimer_livre(titre, auteur):
                print("Livre supprimé")
            else:
                print("Livre non trouvé")
                
        elif choix == "3":
            biblio.afficher_tous_livres()
            
        elif choix == "4":
            titre = input("Titre du livre: ")
            biblio.afficher_detail_livre(titre)
            
        elif choix == "5":
            biblio.sauvegarder(fichier_json)
            print(f"Bibliothèque sauvegardée dans {fichier_json}")
            
        elif choix == "6":
            biblio.charger(fichier_json)
            print("Bibliothèque chargée")
            
        elif choix == "7":
            break
            
if __name__ == "__main__":
    main()