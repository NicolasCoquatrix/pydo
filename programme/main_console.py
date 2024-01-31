## IMPORTS
import mysql.connector
import datetime


## CONNEXION À LA BASE DE DONNÉE
config = {
    'user': 'root',
    'password': '',
    'host': 'localhost', #127.0.0.1
    'database': 'pydo'
}
mydb = mysql.connector.connect(**config)
mydb.autocommit = True

# Initialiser du curseur
mycursor = mydb.cursor(dictionary=True)

mycursor.execute(f"CREATE TABLE IF NOT EXISTS etat(id_etat INT AUTO_INCREMENT,nom_etat VARCHAR(10),PRIMARY KEY(id_etat),UNIQUE(nom_etat));")
mycursor.execute(f"CREATE TABLE IF NOT EXISTS tache(id_tache INT AUTO_INCREMENT,libelle_tache VARCHAR(100) NOT NULL,date_creation_tache DATE NOT NULL,date_realisation_tache DATE,date_objectif_tache DATE,id_etat INT NOT NULL,PRIMARY KEY(id_tache),FOREIGN KEY(id_etat) REFERENCES etat(id_etat));")
mycursor.execute(f"INSERT IGNORE INTO etat (nom_etat) VALUES ('À faire'),('En cours'),('Terminée');")


## FONTIONS 
def menu_print():
    print("\n\nMENU :\nSaissisez votre choix au clavier et appuyez sur la touche 'Entrée' pour valider.\n\n1 - Ajouter une tâche\n2 - Démarrer une tâche\n3 - Terminer une tâche\n4 - Supprimer une tâche\n5 - Modifier une tâche\n6 - Quitter")
    choice_possibilities = ["1","2","3","4","5","6"]
    while True :
        try :
            menu_choice = input("\nVotre choix : ")
            if menu_choice not in choice_possibilities :
                raise Exception
            return menu_choice
        except Exception :
            print("\n🚫  Erreur : Merci de saisir un choix valide.")

def input_string_not_empty(text_print,error_message):
    while True :
        try :
            text = input(text_print)
            if text == "":
                raise Exception
            return text
        except Exception :
            print(error_message)

def string_escaped(text):
    new_text = ""
    for i_letter in range (len(text)):
        if text[i_letter] == "'" or text[i_letter] == "\\" or text[i_letter] == "%" or text[i_letter] == "$" :
            new_text += f"\{text[i_letter]}"
        else :
            new_text += text[i_letter]
    return new_text

def input_date(text_print):
    numbers = ["0","1","2","3","4","5","6","7","8","9"]
    error_message_format = "\n🚫  Erreur : Merci de saisir la date dans le bon format."
    error_message_past = "\n🚫  Erreur : Merci de ne pas saisir une date dans le passé."
    while True :
        try :
            # Saisire la date
            date = input(text_print)
            year = ""
            actuel_year = datetime.date.today().year
            month = ""
            actuel_month = datetime.date.today().month
            day = ""
            actuel_day = datetime.date.today().day
            # Vérifier le format
            if date == "":
                return
            elif len(date) != 10:
                print(error_message_format)
                raise Exception
            for i_year in range(0,4):
                if date[i_year] not in numbers:
                    print(error_message_format)
                    raise Exception
                else:
                    year += date[i_year]
            if date[4] != "-":
                print(error_message_format)
                raise Exception
            for i_month in range(5,7):
                if date[i_month] not in numbers:
                    print(error_message_format)
                    raise Exception
                else:
                    month += date[i_month]
            if date[7] != "-":
                print(error_message_format)
                raise Exception
            for i_day in range(8,10):
                if date[i_day] not in numbers:
                    print(error_message_format)
                    raise Exception
                else:
                    day += date[i_day]
            year = int(year)
            month = int(month)
            day = int(day)
            # Vérifier le mois (max 12) et le jour (max 31)
            if month < 0 or month > 12:
                print(error_message_format)
                raise Exception
            if day < 0 or day > 31:
                print(error_message_format)
                raise Exception
            # Vérifier la date
            if year < actuel_year :
                print(error_message_past)
                raise Exception
            elif year == actuel_year:
                if month < actuel_month :
                    print(error_message_past)
                    raise Exception
                elif month == actuel_month :
                    if day < actuel_day :
                        print(error_message_past)
                        raise Exception
            return date
        except Exception :
            pass

def input_choice(choice_possibilities):
    while True :
        try :
            input_choice = input("\nVotre choix : ")
            if input_choice not in choice_possibilities :
                raise Exception
            return input_choice
        except Exception :
            print("\n🚫  Erreur : Merci de saisir un choix valide.")

def input_yes_or_no():
    while True :
        try :
            y_n_choice = input("\nSaissisez 'Y' pour 'OUI' ou 'N' pour 'NON' : ").lower()
            if y_n_choice != "y" and y_n_choice != "n" :
                raise Exception
            return y_n_choice
        except Exception :
            print("\n🚫  Erreur : Merci de saisir 'Y' ou 'N'.")


##PROGRAMME
program_end = False
# Selectionner la liste des tâches à faire et en cours
mycursor.execute("SELECT libelle_tache,nom_etat FROM tache INNER JOIN etat WHERE tache.id_etat = etat.id_etat AND (tache.id_etat=1 OR tache.id_etat=2) ORDER BY nom_etat,date_creation_tache,libelle_tache;")
to_do_list = mycursor.fetchall()
# Afficher la liste des tâches à faire et en cours
print("\n\nTO DO LIST :\n")
if len(to_do_list) == 0:
    print("Il n'y a pas de tâche à faire ou en cours.")
else:
    for i_task in range (len(to_do_list)) :
        print(f"{to_do_list[i_task]['nom_etat']} - {to_do_list[i_task]['libelle_tache']}")

# Afficher le menu
menu_choice = menu_print()

# Actions du choix du menu
while program_end == False :
    # Ajouter une tâche
    if menu_choice == "1" :
        print("\n\nAJOUTER UNE TÂCHE :")
        # Saisir le libéllé
        wording = input_string_not_empty("\nSaisir le libéllé : ","\n🚫  Erreur : Merci de saisir un libéllé.")
        wording_escaped = string_escaped(wording)
        # Définir la date de création
        date_creation = datetime.date.today()
        # Saisir la date objectif
        date_target = input_date("\nSaisir la date de réalisation souhaité sous la forme 'AAAA-MM-JJ' (champ facultatif, à laisser vide pour ne pas fixer d'objectif) : ")
        # Enregistrer dans la base de donnée
        mycursor.execute(f"INSERT INTO tache (libelle_tache,date_creation_tache,date_objectif_tache) VALUES ('{wording_escaped}','{date_creation}','{date_target}');")
        # Confirmer l'ajout
        print (f"\n✔️  '{wording}' a bien été ajouté à votre liste de tâches.")
        # Afficher le menu
        menu_choice = menu_print()

    # Démarrer une tâche
    elif menu_choice == "2" :
        print("\n\nDÉMARRER UNE TÂCHE :\nQuelle tâche voulez-vous démmarrer ?\n")
        # Selectionner la liste des tâches à faire
        mycursor.execute("SELECT id_tache,libelle_tache FROM tache WHERE tache.id_etat=1 ORDER BY libelle_tache;")
        to_do_list = mycursor.fetchall()
        # Afficher la liste des tâches à faire
        choice_possibilities = []
        if len(to_do_list) == 0:
            print("Il n'y a pas de tâche à démarrer.")
        else:
            choice_combination = []
            for i_task in range (len(to_do_list)) :
                counter = str(i_task+1)
                print(f"{counter} - {to_do_list[i_task]['libelle_tache']}")
                choice_combination += [[counter,to_do_list[i_task]['id_tache']]]
                choice_possibilities += [counter]
            # Saisir le choix
            started_choice = input_choice(choice_possibilities)
            for i_task in range (len(to_do_list)) :
                if started_choice == choice_combination[i_task][0]:
                    started_task = to_do_list[i_task]['libelle_tache']
                    started_reel_choice = choice_combination[i_task][1]
            mycursor.execute(f"UPDATE tache SET id_etat=2 WHERE id_tache={started_reel_choice};")
            # Confirmer le démarrage
            print (f"\n✔️  '{started_task}' a bien été démarré.") 
        # Afficher le menu
        menu_choice = menu_print()
    
    # Finaliser une tâche
    elif menu_choice == "3" :
        print("\n\nFINALISER UNE TÂCHE :\nQuelle tâche voulez-vous finaliser ?\n")
        # Selectionner la liste des tâches en cours
        mycursor.execute("SELECT id_tache,libelle_tache FROM tache WHERE tache.id_etat=2 ORDER BY libelle_tache;")
        to_do_list = mycursor.fetchall()
        # Afficher la liste des tâches en cours
        choice_possibilities = []
        if len(to_do_list) == 0:
            print("Il n'y a pas de tâche à finaliser.")
        else:
            choice_combination = []
            for i_task in range (len(to_do_list)) :
                counter = str(i_task+1)
                print(f"{counter} - {to_do_list[i_task]['libelle_tache']}")
                choice_combination += [[counter,to_do_list[i_task]['id_tache']]]
                choice_possibilities += [counter]
            # Saisir le choix
            finalized_choice = input_choice(choice_possibilities)
            for i_task in range (len(to_do_list)) :
                if finalized_choice == choice_combination[i_task][0]:
                    finalized_task =  to_do_list[i_task]['libelle_tache']
                    finalized_reel_choice = choice_combination[i_task][1]
            date_finalization = datetime.date.today()
            mycursor.execute(f"UPDATE tache SET id_etat=3,date_realisation_tache='{date_finalization}' WHERE id_tache={finalized_reel_choice};")
            # Confirmer la finalisation
            print (f"\n✔️  '{finalized_task}' a bien été finalisé.") 
        # Afficher le menu
        menu_choice = menu_print()

    # Supprimer une tâche
    elif menu_choice == "4" :
        print("\n\nSUPPRIMER UNE TÂCHE :\nQuelle tâche voulez-vous supprimer ?\n")
        # Selectionner la liste des tâches
        mycursor.execute("SELECT id_tache,nom_etat,libelle_tache FROM tache INNER JOIN etat WHERE tache.id_etat = etat.id_etat ORDER BY id_tache;")
        to_do_list = mycursor.fetchall()
        # Afficher la liste des tâches
        choice_possibilities = []
        if len(to_do_list) == 0:
            print("Il n'y a pas de tâche à supprimer.")
        else:
            choice_combination = []
            for i_task in range (len(to_do_list)) :
                counter = str(i_task+1)
                print(f"{counter} - {to_do_list[i_task]['nom_etat']} - {to_do_list[i_task]['libelle_tache']}")
                choice_combination += [[counter,to_do_list[i_task]['id_tache']]]
                choice_possibilities += [counter]
            # Saisir le choix
            deleted_choice = input_choice(choice_possibilities)
            for i_task in range (len(to_do_list)) :
                if deleted_choice == choice_combination[i_task][0]:
                    deleted_task =  to_do_list[i_task]['libelle_tache']
                    deleted_reel_choice = choice_combination[i_task][1]
            print (f"\n⚠️  Êtes-vous dur de vouloir supprimer le tâche '{deleted_task}' ? Cette action est irréversible !")
            y_n_choice = input_yes_or_no()
            if y_n_choice == "y":
                mycursor.execute(f"DELETE FROM tache WHERE id_tache={deleted_reel_choice};")
                # Confirmer la suppréssion
                print (f"\n✔️  '{deleted_task}' a bien été supprimé.")
            elif y_n_choice == "n":
                print (f"\n✖️  '{deleted_task}' n'a pas été supprimé.")
        # Afficher le menu
        menu_choice = menu_print()

    # Modifier une tâche
    elif menu_choice == "5" :
        print("\n\nMODIFIER UNE TÂCHE :\nQuelle tâche voulez-vous modifier ?\n")
        # Selectionner la liste des tâches
        mycursor.execute("SELECT id_tache,nom_etat,libelle_tache,date_objectif_tache FROM tache INNER JOIN etat WHERE tache.id_etat = etat.id_etat ORDER BY id_tache;")
        to_do_list = mycursor.fetchall()
        # Afficher la liste des tâches
        choice_possibilities = []
        if len(to_do_list) == 0:
            print("Il n'y a pas de tâche à modifier.")
        else:
            choice_combination = []
            for i_task in range (len(to_do_list)) :
                counter = str(i_task+1)
                print(f"{counter} - {to_do_list[i_task]['nom_etat']} - {to_do_list[i_task]['libelle_tache']}")
                choice_combination += [[counter,to_do_list[i_task]['id_tache']]]
                choice_possibilities += [counter]
            # Saisir le choix
            modified_choice = input_choice(choice_possibilities)
            for i_task in range (len(to_do_list)) :
                if modified_choice == choice_combination[i_task][0]:
                    modified_task =  to_do_list[i_task]['libelle_tache']
                    modified_reel_choice = choice_combination[i_task][1]
                    modified_date_task = to_do_list[i_task]['date_objectif_tache']
                    modified_status_task = to_do_list[i_task]['nom_etat']
                    if modified_date_task == None:
                        modified_date_task = "Pas de date de réalisation souhaité."
            # Modifier le libéllé
            print(f"\nVoulez vous modifier le libéllé : '{modified_task}' ?")
            y_n_choice = input_yes_or_no()
            if y_n_choice == "y":
                new_wording = input_string_not_empty("\nSaisir le nouveau libéllé : ","\n🚫  Erreur : Merci de saisir un libéllé.")
                new_wording_escaped = string_escaped(new_wording)
                mycursor.execute(f"UPDATE tache SET libelle_tache='{new_wording_escaped}' WHERE id_tache={modified_reel_choice};")
                # Confirmer la modification du libéllé
                print (f"\n✔️  '{modified_task}' a bien été modifié en '{new_wording}'.") 
            # Modifier la date objectif
            print(f"\nVoulez vous modifier la date de réalisation souhaité : '{modified_date_task}' ?")
            y_n_choice = input_yes_or_no()
            if y_n_choice == "y":
                new_date_target = input_date("\nSaisir la nouvelle date de réalisation souhaité sous la forme 'AAAA-MM-JJ' (champ facultatif, à laisser vide pour ne pas fixer d'objectif) : ")
                if new_date_target == None:
                    new_date_target = "0000-00-00"
                mycursor.execute(f"UPDATE tache SET date_objectif_tache={new_date_target} WHERE id_tache={modified_reel_choice};")
                # Confirmer la modification de la date objectif
                if new_date_target == "0000-00-00":
                    new_date_target = "Pas de date de réalisation souhaité."
                print (f"\n✔️  '{modified_date_task}' a bien été modifié en '{new_date_target}'.") 
            # Modifier l'état
            print(f"\nVoulez vous modifier l'état : '{modified_status_task}' ?")
            y_n_choice = input_yes_or_no()
            if y_n_choice == "y":
                print("\nVeuillez choisir le nouvel état :\n1 - À faire\n2 - En cours\n3 - Terminée")
                choice_possibilities = ["1","2","3"]
                new_status = input_choice(choice_possibilities)
                mycursor.execute(f"UPDATE tache SET id_etat={new_status} WHERE id_tache={modified_reel_choice};")
                # Confirmer la modification de l'état
                if new_status == "1":
                    new_status = "À faire"
                elif new_status == "2":
                    new_status = "En cours"
                elif new_status == "3":
                    new_status = "Terminée"
                print (f"\n✔️  '{modified_status_task}' a bien été modifié en '{new_status}'.") 
        # Afficher le menu
        menu_choice = menu_print()

    # Clôture du programme
    elif menu_choice == "6" :
        print("\n\n\n💻 Programmé par Nicolas Coquatrix.\n\n\n")
        program_end = True