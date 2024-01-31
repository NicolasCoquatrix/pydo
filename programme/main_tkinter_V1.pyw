# ==================================================
# region : IMPORTS

import mysql.connector
import datetime
import webbrowser

# Tkinter
from tkinter import Tk, ttk, PhotoImage, Frame, Canvas, Button, Label, Entry, StringVar, messagebox
from tkcalendar import DateEntry

# endregion : IMPORTS
# ==================================================


# ==================================================
# region : CONNECTION À LA BASE DE DONNÉES

# Paramétrage de la connection
config = {"user": "root", "password": "", "host": "localhost", "database": "pydo_coquatrix_nicolas"} # Host = 127.0.0.1
mydb = mysql.connector.connect(**config)
mydb.autocommit = True

# Initialisation du curseur
mycursor = mydb.cursor(dictionary=True)

mycursor.execute(f"CREATE TABLE IF NOT EXISTS etat(id_etat INT AUTO_INCREMENT,nom_etat VARCHAR(10),PRIMARY KEY(id_etat),UNIQUE(nom_etat));")
mycursor.execute(f"CREATE TABLE IF NOT EXISTS tache(id_tache INT AUTO_INCREMENT,libelle_tache VARCHAR(100) NOT NULL,date_creation_tache DATE NOT NULL,date_realisation_tache DATE,date_objectif_tache DATE,id_etat INT NOT NULL,PRIMARY KEY(id_tache),FOREIGN KEY(id_etat) REFERENCES etat(id_etat));")
mycursor.execute(f"INSERT IGNORE INTO etat (nom_etat) VALUES ('À faire'),('En cours'),('Terminée');")

# endregion : CONNECTION À LA BASE DE DONNÉES
# ==================================================


# ==================================================
# region : COULEURS

# Couleurs principales
color_main_light = "#7179AD" # Texte en noir
color_main_medium = "#525A8E" # Texte en blanc
color_main_dark = "#3C4168" # Texte en blanc

# Couleurs blanc / gris / noir
color_white = "#EFEFEF" # Texte en noir
color_gray_light = "#C2C2C2" # Texte en noir
color_gray_medium = "#999999" # Texte en noir
color_gray_dark = "#666666" # Texte en noir
color_black = "#222222" # Texte en blanc

# Couleurs rouge / vert
color_red_warnning = "#C91829" # Texte en blanc
color_red_dark = "#E73546" # Texte en noir
color_red_light = "#EE6D7A" # Texte en noir
color_green_dark = "#1BC487" # Texte en noir
color_green_light = "#3AE4A6" # Texte en noir

# Couleurs des status 
color_status_to_do = "#C2C2C2" # Texte en noir
color_status_in_progress = "#F9CDB3" # Texte en noir
color_status_finished = "#D2E7C6" # Texte en noir
color_status_late =  "#FFADAD" # Texte en noir

#endregion : COULEURS
# ==================================================


# ==================================================
# region : POLICES

# Police de titre
font_title = ["Poppins", 20, "bold"]

# Polices de corps (Grande)
font_body_hight = ["Roboto", 17]
font_body_hight_bold = ["Roboto", 17, "bold"]

# Polices de corps (Moyenne)
font_body_medium = ["Roboto", 14]
font_body_medium_bold = ["Roboto", 14, "bold"]

# Polices de corps (Petite)
font_body_low = ["Roboto", 11]
font_body_low_bold = ["Roboto", 11, "bold"]

# endregion : POLICES
# ==================================================


# ==================================================
# region :  FENÊTRE PRINCIPALE

window = Tk()
window.configure(bg=color_main_dark)
window.iconbitmap("../images/pydo_logo_50x50.ico")
window.title("PyDo - Nicolas Coquatrix")
window.minsize(450,105)

# endregion :  FENÊTRE PRINCIPALE
# ==================================================


# ==================================================
# region : IMAGES

# Logo
logo_icon = PhotoImage(file="../images/pydo_logo_50x50.png")

# Filtres
visibility_on_white_icon = PhotoImage(file="../images/visibility_on_white_24x24.png")
visibility_on_black_icon = PhotoImage(file="../images/visibility_on_black_24x24.png")
visibility_off_blue_icon = PhotoImage(file="../images/visibility_off_blue_24x24.png")
visibility_off_black_icon = PhotoImage(file="../images/visibility_off_black_24x24.png")

# Nouvelle tâche
new_task_white_icon = PhotoImage(file="../images/new_white_50x50.png")
new_task_black_icon = PhotoImage(file="../images/new_black_50x50.png")

# Status
to_do_icon = PhotoImage(file="../images/to_do_50x50.png")
in_progress_icon = PhotoImage(file="../images/in_progress_50x50.png")
finished_icon = PhotoImage(file="../images/finished_50x50.png")
in_modification = PhotoImage(file="../images/modification_50x50.png")
in_deletion = PhotoImage(file="../images/deleted_50x50.png")

# Infos
status_white_icon = PhotoImage(file="../images/status_white_24x24.png")
status_black_icon = PhotoImage(file="../images/status_black_24x24.png")
creation_date_white_icon = PhotoImage(file="../images/date_create_white_24x24.png")
creation_date_black_icon = PhotoImage(file="../images/date_create_black_24x24.png")
objectif_date_white_icon = PhotoImage(file="../images/date_objectif_white_24x24.png")
objectif_date_black_icon = PhotoImage(file="../images/date_objectif_black_24x24.png")
finish_date_white_icon = PhotoImage(file="../images/date_finish_white_24x24.png")
finish_date_black_icon = PhotoImage(file="../images/date_finish_black_24x24.png")

# Boutons
back_icon = PhotoImage(file="../images/back_24x24.png")
update_icon = PhotoImage(file="../images/update_24x24.png")
delete_icon = PhotoImage(file="../images/delete_24x24.png")
validate_icon = PhotoImage(file="../images/validate_24x24.png")

# Réseaux
linkedin_white_icon = PhotoImage(file="../images/linkedin_logo_white_30x30.png")
linkedin_black_icon = PhotoImage(file="../images/linkedin_logo_black_30x30.png")
github_white_icon = PhotoImage(file="../images/github_logo_white_30x30.png")
github_black_icon = PhotoImage(file="../images/github_logo_black_30x30.png")

# endregion : IMAGES
# ==================================================


# ==================================================
# region : FONCTIONS


# ========================================
# region : Fontions - Header


# ==============================
# region : Fontions - Filtres

def visibility_default(filter, status):
    if status == True:
        filter.config(image=visibility_on_white_icon, fg=color_white)
    elif status == False:
        filter.config(image=visibility_off_blue_icon, fg=color_main_light)

def visibility_hover(filter, status):
    if status == True:
        filter.config(image=visibility_on_black_icon, fg=color_black)
    elif status == False:
        filter.config(image=visibility_off_black_icon, fg=color_black)

# Filtre 'À faire'
def to_do_enter(event):
    visibility_hover(to_do_filter, to_do_status)

def to_do_leave(event):
    visibility_default(to_do_filter, to_do_status)

def to_do_click(event):
    global to_do_status
    to_do_status = not to_do_status
    visibility_default(to_do_filter, to_do_status)
    tasks_print()

# Filtre 'À faire'
def in_progress_enter(event):
    visibility_hover(in_progress_filter, in_progress_status)

def in_progress_leave(event):
    visibility_default(in_progress_filter, in_progress_status)

def in_progress_click(event):
    global in_progress_status
    in_progress_status = not in_progress_status
    visibility_default(in_progress_filter, in_progress_status)
    tasks_print()

# Filtre 'Terminée'
def finished_enter(event):
    visibility_hover(finished_filter, finished_status)

def finished_leave(event):
    visibility_default(finished_filter, finished_status)

def finished_click(event):
    global finished_status
    finished_status = not finished_status
    visibility_default(finished_filter, finished_status)
    tasks_print()

# endregion : Fontions - Filtres
# ==============================


# ==============================
# region : Fontions - Barre d'ajout

def new_task_default():
    new_task_button = Button(new_task_box, bg=color_white, activebackground=color_white, relief="flat", borderwidth=0, font=font_body_hight, fg=color_black, activeforeground=color_black, cursor="hand2", image=new_task_black_icon, text=" Ajouter une tâche", compound="left", padx=20, pady=20, anchor="w")
    new_task_button.pack(fill="both")
    new_task_button.bind("<Enter>", lambda event, new_task_button=new_task_button: new_task_enter(event, new_task_button))
    new_task_button.bind("<Leave>", lambda event, new_task_button=new_task_button: new_task_leave(event, new_task_button))
    new_task_button.bind("<Button-1>", lambda event, new_task_button=new_task_button, new_task_box=new_task_box: new_task_click(event, new_task_button, new_task_box))

def new_task_enter(event, new_task_button):
    new_task_button.config(bg=color_main_light, image=new_task_white_icon, fg=color_white)

def new_task_leave(event, new_task_button):
    new_task_button.config(bg=color_white, image=new_task_black_icon, fg=color_black)

def new_task_click(event, new_task_button, new_task_box):
    # Suppression de l'ancien bouton
    new_task_button.destroy()

    # Création du nouveau conteneur
    new_task_creation_box = Frame(new_task_box, bg=color_main_light, height=80)
    new_task_creation_box.pack_propagate(False)
    new_task_creation_box.pack(fill="both")

    # Icone
    new_task_icon_box = Canvas(new_task_creation_box, width=92, height=80, bg=color_main_light, highlightthickness=0)
    new_task_icon_box.create_image(46, 40, image=new_task_white_icon)
    new_task_icon_box.pack(side="left")

    # Infos
    new_task_infos_box = Frame(new_task_creation_box, bg=color_main_light)
    new_task_infos_box.pack(side="left", fill="x", expand=True)

    # Libéllé
    new_task_wording_box = Frame(new_task_infos_box, bg=color_main_light, height=30)
    new_task_wording_box.pack_propagate(False)
    new_task_wording_box.pack(side="top", fill="both", padx=(0,20))
    new_task_wording_label = Label(new_task_wording_box, bg=color_main_light, text="Libéllé :", font=font_body_medium_bold, fg=color_white)
    new_task_wording_label.pack(side="left")
    new_task_wording_validate_command = window.register(wording_max_character)
    new_task_wording_value = Entry(new_task_wording_box, bg=color_white, validate="key", validatecommand=(new_task_wording_validate_command, "%P"), width=60, font=font_body_medium, fg=color_black, insertbackground=color_black)
    new_task_wording_value.pack(side="left", padx=(8,0))

    # Datas
    new_task_data_box = Frame(new_task_infos_box, bg=color_main_light, height=30)
    new_task_data_box.pack_propagate(False)
    new_task_data_box.pack(side="bottom", fill="both")

    # Status
    new_task_status_box = Frame(new_task_data_box, bg=color_main_light, width=250, height=30)
    new_task_status_box.pack_propagate(False)
    new_task_status_box.pack(side="left", padx=(0,15))
    nex_task_status_icon = Canvas(new_task_status_box, width=26, height=26, bg=color_main_light, highlightthickness=0)
    nex_task_status_icon.create_image(13, 13, image=status_white_icon)
    nex_task_status_icon.pack(side="left")
    new_task_status_wording = Label(new_task_status_box, bg=color_main_light, text="Status :", font=font_body_low_bold, fg=color_white)
    new_task_status_wording.pack(side="left")
    new_task_status_text = Label(new_task_status_box, bg=color_main_light, text="À faire", font=font_body_low, fg=color_white)
    new_task_status_text.pack(side="left")

    # Date Création
    new_task_creation_date_box = Frame(new_task_data_box, bg=color_main_light, width=250, height=30)
    new_task_creation_date_box.pack_propagate(False)
    new_task_creation_date_box.pack(side="left", padx=(0,15))
    new_task_creation_date_icon = Canvas(new_task_creation_date_box, width=26, height=26, bg=color_main_light, highlightthickness=0)
    new_task_creation_date_icon.create_image(13, 13, image=creation_date_white_icon)
    new_task_creation_date_icon.pack(side="left")
    new_task_creation_date_wording = Label(new_task_creation_date_box, bg=color_main_light, text=f"Créé le :", font=font_body_low_bold, fg=color_white)
    new_task_creation_date_wording.pack(side="left")
    new_task_creation_date_text = Label(new_task_creation_date_box, bg=color_main_light, text=str(datetime.date.today()), font=font_body_low, fg=color_white)
    new_task_creation_date_text.pack(side="left")

    # Date objectif
    new_task_objectif_date_box = Frame(new_task_data_box, bg=color_main_light, width=250, height=30)
    new_task_objectif_date_box.pack_propagate(False)
    new_task_objectif_date_box.pack(side="left")
    new_task_objectif_date_icon = Canvas(new_task_objectif_date_box, width=26, height=26, bg=color_main_light, highlightthickness=0)
    new_task_objectif_date_icon.create_image(13, 13, image=objectif_date_white_icon)
    new_task_objectif_date_icon.pack(side="left")
    new_task_objectif_date_wording = Label(new_task_objectif_date_box, bg=color_main_light, text="Deadline :", font=font_body_low_bold, fg=color_white)
    new_task_objectif_date_wording.pack(side="left")
    new_task_objectif_date_value = DateEntry(new_task_objectif_date_box, bg=color_status_to_do, locale='fr_FR', relief="flat", font=font_body_low, fg=color_black, borderwidth=0, mindate=datetime.date.today(), showothermonthdays=False, background=color_main_medium, foreground=color_white, headersbackground=color_main_light, headersforeground=color_white, bordercolor=color_main_light, normalbackground=color_white, normalforeground=color_black, weekendbackground=color_white, weekendforeground=color_black, selectbackground=color_main_medium, selectforeground=color_white)
    new_task_objectif_date_value.pack(side="left")
    for date in new_task_objectif_date_value._top_cal.winfo_children():
        date.bind("<Enter>", calendar_enter)
        date.bind("<Leave>", calendar_leave)

    # Bouton 'Valider'
    validate_button = Button(new_task_creation_box, relief="flat", borderwidth=0, bg=color_green_dark, activebackground=color_green_dark, cursor="hand2", image=validate_icon, width=40, height=40)
    validate_button.pack(side="right", padx=(0,20))
    validate_button.bind("<Enter>", lambda event, validate_button=validate_button: validate_enter(event, validate_button))
    validate_button.bind("<Leave>", lambda event, validate_button=validate_button: validate_leave(event, validate_button))
    validate_button.bind("<Button-1>", lambda event, new_task_wording_value=new_task_wording_value, new_task_objectif_date_value=new_task_objectif_date_value, new_task_creation_box=new_task_creation_box: validate_click(event, new_task_wording_value, new_task_objectif_date_value, new_task_creation_box))

    # Bouton 'Annuler'
    cancel_button = Button(new_task_creation_box, relief="flat", borderwidth=0, bg=color_gray_dark, activebackground=color_gray_dark, cursor="hand2", image=back_icon, width=40, height=40)
    cancel_button.pack(side="right", padx=(0,20))
    cancel_button.bind("<Enter>", lambda event, cancel_button=cancel_button: cancel_enter(event, cancel_button))
    cancel_button.bind("<Leave>", lambda event, cancel_button=cancel_button: cancel_leave(event, cancel_button))
    cancel_button.bind("<Button-1>", lambda event, new_task_creation_box=new_task_creation_box: cancel_click(event, new_task_creation_box))

def cancel_enter(event, cancel_button):
    cancel_button.config(bg=color_gray_medium)

def cancel_leave(event, cancel_button):
    cancel_button.config(bg=color_gray_dark)

def cancel_click(event, new_task_creation_box):
    new_task_creation_box.destroy()
    new_task_default()

def wording_max_character(P):
    if len(P) <= 100:
        return True
    else:
        return False
    
def validate_enter(event, validate_button):
    validate_button.config(bg=color_green_light)

def validate_leave(event, validate_button):
    validate_button.config(bg=color_green_dark)

def validate_click(event, new_task_wording_value, new_task_objectif_date_value, new_task_creation_box):
    mycursor.execute(f"INSERT INTO tache (libelle_tache,date_creation_tache,date_objectif_tache,id_etat) VALUES ('{new_task_wording_value.get()}','{datetime.date.today()}','{new_task_objectif_date_value.get_date()}',1);")
    new_task_creation_box.destroy()
    new_task_default()
    tasks_print()

def calendar_enter(event):
    event.widget.config(cursor="hand2")

def calendar_leave(event):
    event.widget.config(cursor="")

# endregion : Fontions - Barre d'ajout
# ==============================


# endregion : Fontions - Herder
# ========================================


# ========================================
# region : Fonctions - Footer

# Bouton 'Linkedin'
def linkedin_enter(event):
    linkedin_button.config(image=linkedin_white_icon)

def linkedin_leave(event):
    linkedin_button.config(image=linkedin_black_icon)

def linkedin_click(event):
    webbrowser.open("https://www.linkedin.com/in/nicolas-coquatrix")

# Bouton 'Github'
def github_enter(event):
    github_button.config(image=github_white_icon)

def github_leave(event):
    github_button.config(image=github_black_icon)

def github_click(event):
    webbrowser.open("https://github.com/NicolasCoquatrix")

# endregion : Fonctions - Footer
# ========================================
    

# ========================================
# region : Fonctions - Main

# Scroll
def scroll(event):
    tasks_window.yview_scroll(int(-1 * (event.delta / 120)), "units")

def scroll_visibility(tasks_list):
    first_visible_line, last_visible_line = tasks_window.yview()
    if first_visible_line == 0.0 and last_visible_line == 1.0:
        tasks_window.unbind("<MouseWheel>")
        for task_frame in tasks_list:
            task_frame["task_button"].unbind("<MouseWheel>")
            task_frame["task_wording_label"].unbind("<MouseWheel>")
            task_frame["task_wording_box"].unbind("<MouseWheel>")
            task_frame["task_status_canvas"].unbind("<MouseWheel>")
            task_frame["task_status_wording"].unbind("<MouseWheel>")
            task_frame["task_status_text"].unbind("<MouseWheel>")
            task_frame["task_status_box"].unbind("<MouseWheel>")
            task_frame["task_creation_date_canvas"].unbind("<MouseWheel>")
            task_frame["task_creation_date_wording"].unbind("<MouseWheel>")
            task_frame["task_creation_date_text"].unbind("<MouseWheel>")
            task_frame["task_creation_date_box"].unbind("<MouseWheel>")
            task_frame["task_objectif_finish_date_canvas"].unbind("<MouseWheel>")
            task_frame["task_objectif_finish_date_wording"].unbind("<MouseWheel>")
            task_frame["task_objectif_finish_date_text"].unbind("<MouseWheel>")
            task_frame["task_objectif_finish_date_box"].unbind("<MouseWheel>")
            task_frame["task_data_box"].unbind("<MouseWheel>")
            task_frame["task_info_box"].unbind("<MouseWheel>")
            task_frame["task_delete_button"].unbind("<MouseWheel>")
            task_frame["task_update_button"].unbind("<MouseWheel>")
            task_frame["task_container"].unbind("<MouseWheel>")
            task_frame["task_box"].unbind("<MouseWheel>")
    else:
        tasks_window.bind("<MouseWheel>", scroll)
        for task_frame in tasks_list:
            task_frame["task_button"].bind("<MouseWheel>", scroll)
            task_frame["task_wording_label"].bind("<MouseWheel>", scroll)
            task_frame["task_wording_box"].bind("<MouseWheel>", scroll)
            task_frame["task_status_canvas"].bind("<MouseWheel>", scroll)
            task_frame["task_status_wording"].bind("<MouseWheel>", scroll)
            task_frame["task_status_text"].bind("<MouseWheel>", scroll)
            task_frame["task_status_box"].bind("<MouseWheel>", scroll)
            task_frame["task_creation_date_canvas"].bind("<MouseWheel>", scroll)
            task_frame["task_creation_date_wording"].bind("<MouseWheel>", scroll)
            task_frame["task_creation_date_text"].bind("<MouseWheel>", scroll)
            task_frame["task_creation_date_box"].bind("<MouseWheel>", scroll)
            task_frame["task_objectif_finish_date_canvas"].bind("<MouseWheel>", scroll)
            task_frame["task_objectif_finish_date_wording"].bind("<MouseWheel>", scroll)
            task_frame["task_objectif_finish_date_text"].bind("<MouseWheel>", scroll)
            task_frame["task_objectif_finish_date_box"].bind("<MouseWheel>", scroll)
            task_frame["task_data_box"].bind("<MouseWheel>", scroll)
            task_frame["task_info_box"].bind("<MouseWheel>", scroll)
            task_frame["task_delete_button"].bind("<MouseWheel>", scroll)
            task_frame["task_update_button"].bind("<MouseWheel>", scroll)
            task_frame["task_container"].bind("<MouseWheel>", scroll)
            task_frame["task_box"].bind("<MouseWheel>", scroll)

def tasks_window_resized(event):
    tasks_window_width = event.width
    tasks_list_box.config(width=tasks_window_width)

# Tâches
def tasks_print():
    # Réinitialisation de la fenêtre des tâches
    for widget in tasks_list_box.winfo_children():
        widget.destroy()
    
    # Requête SQL
    if to_do_status == True and in_progress_status == True and finished_status == True:
        mycursor.execute("SELECT tache.id_tache,tache.libelle_tache,etat.id_etat,etat.nom_etat,tache.date_creation_tache,tache.date_objectif_tache,tache.date_realisation_tache FROM tache INNER JOIN etat WHERE tache.id_etat = etat.id_etat ORDER BY CASE WHEN etat.id_etat IN (1, 2) THEN 0 WHEN etat.id_etat = 3 THEN 1 ELSE 2 END,CASE WHEN etat.id_etat IN (1, 2) THEN COALESCE(tache.date_objectif_tache, '9999-12-31') WHEN etat.id_etat = 3 THEN tache.date_realisation_tache END,tache.libelle_tache;")
    elif to_do_status == True and in_progress_status == True and finished_status == False:
        mycursor.execute("SELECT tache.id_tache,tache.libelle_tache,etat.id_etat,etat.nom_etat,tache.date_creation_tache,tache.date_objectif_tache,tache.date_realisation_tache FROM tache INNER JOIN etat WHERE tache.id_etat = etat.id_etat AND (tache.id_etat=1 OR tache.id_etat=2) ORDER BY CASE WHEN etat.id_etat IN (1, 2) THEN 0 WHEN etat.id_etat = 3 THEN 1 ELSE 2 END,CASE WHEN etat.id_etat IN (1, 2) THEN COALESCE(tache.date_objectif_tache, '9999-12-31') WHEN etat.id_etat = 3 THEN tache.date_realisation_tache END,tache.libelle_tache;")
    elif to_do_status == True and in_progress_status == False and finished_status == True:
        mycursor.execute("SELECT tache.id_tache,tache.libelle_tache,etat.id_etat,etat.nom_etat,tache.date_creation_tache,tache.date_objectif_tache,tache.date_realisation_tache FROM tache INNER JOIN etat WHERE tache.id_etat = etat.id_etat AND (tache.id_etat=1 OR tache.id_etat=3) ORDER BY CASE WHEN etat.id_etat IN (1, 2) THEN 0 WHEN etat.id_etat = 3 THEN 1 ELSE 2 END,CASE WHEN etat.id_etat IN (1, 2) THEN COALESCE(tache.date_objectif_tache, '9999-12-31') WHEN etat.id_etat = 3 THEN tache.date_realisation_tache END,tache.libelle_tache;")
    elif to_do_status == False and in_progress_status == True and finished_status == True:
        mycursor.execute("SELECT tache.id_tache,tache.libelle_tache,etat.id_etat,etat.nom_etat,tache.date_creation_tache,tache.date_objectif_tache,tache.date_realisation_tache FROM tache INNER JOIN etat WHERE tache.id_etat = etat.id_etat AND (tache.id_etat=2 OR tache.id_etat=3) ORDER BY CASE WHEN etat.id_etat IN (1, 2) THEN 0 WHEN etat.id_etat = 3 THEN 1 ELSE 2 END,CASE WHEN etat.id_etat IN (1, 2) THEN COALESCE(tache.date_objectif_tache, '9999-12-31') WHEN etat.id_etat = 3 THEN tache.date_realisation_tache END,tache.libelle_tache;")
    elif to_do_status == True and in_progress_status == False and finished_status == False:
        mycursor.execute("SELECT tache.id_tache,tache.libelle_tache,etat.id_etat,etat.nom_etat,tache.date_creation_tache,tache.date_objectif_tache,tache.date_realisation_tache FROM tache INNER JOIN etat WHERE tache.id_etat = etat.id_etat AND tache.id_etat=1 ORDER BY CASE WHEN etat.id_etat IN (1, 2) THEN 0 WHEN etat.id_etat = 3 THEN 1 ELSE 2 END,CASE WHEN etat.id_etat IN (1, 2) THEN COALESCE(tache.date_objectif_tache, '9999-12-31') WHEN etat.id_etat = 3 THEN tache.date_realisation_tache END,tache.libelle_tache;")
    elif to_do_status == False and in_progress_status == True and finished_status == False:
        mycursor.execute("SELECT tache.id_tache,tache.libelle_tache,etat.id_etat,etat.nom_etat,tache.date_creation_tache,tache.date_objectif_tache,tache.date_realisation_tache FROM tache INNER JOIN etat WHERE tache.id_etat = etat.id_etat AND tache.id_etat=2 ORDER BY CASE WHEN etat.id_etat IN (1, 2) THEN 0 WHEN etat.id_etat = 3 THEN 1 ELSE 2 END,CASE WHEN etat.id_etat IN (1, 2) THEN COALESCE(tache.date_objectif_tache, '9999-12-31') WHEN etat.id_etat = 3 THEN tache.date_realisation_tache END,tache.libelle_tache;")
    elif to_do_status == False and in_progress_status == False and finished_status == True:
        mycursor.execute("SELECT tache.id_tache,tache.libelle_tache,etat.id_etat,etat.nom_etat,tache.date_creation_tache,tache.date_objectif_tache,tache.date_realisation_tache FROM tache INNER JOIN etat WHERE tache.id_etat = etat.id_etat AND tache.id_etat=3 ORDER BY CASE WHEN etat.id_etat IN (1, 2) THEN 0 WHEN etat.id_etat = 3 THEN 1 ELSE 2 END,CASE WHEN etat.id_etat IN (1, 2) THEN COALESCE(tache.date_objectif_tache, '9999-12-31') WHEN etat.id_etat = 3 THEN tache.date_realisation_tache END,tache.libelle_tache;")
    to_do_list = mycursor.fetchall()

    tasks_list = []

    # Afficher la liste des tâches
    for i_task in range (len(to_do_list)) :
        # Création des variables
        task_id = int(to_do_list[i_task]["id_tache"])
        task_wording = str(to_do_list[i_task]["libelle_tache"])
        task_id_status = int(to_do_list[i_task]["id_etat"])
        task_status = str(to_do_list[i_task]["nom_etat"])
        task_creation_date = str(to_do_list[i_task]["date_creation_tache"])
        task_objectif_date = str(to_do_list[i_task]["date_objectif_tache"])
        task_finished_date = str(to_do_list[i_task]["date_realisation_tache"])

        # Modification des dates
        task_creation_date = ydm_to_dmy(task_creation_date)
        task_objectif_date = ydm_to_dmy(task_objectif_date)
        task_finished_date = ydm_to_dmy(task_finished_date)

        # Affectation des variables
        if task_id_status == 1:
            task_color_status = color_status_to_do
            task_icon = to_do_icon
            task_cursor = "hand2"
            task_date_icon = objectif_date_black_icon
            task_objectif_date_wording = "Deadline :"
            task_objectif_finished_date_text = task_objectif_date
        elif task_id_status == 2:
            task_color_status = color_status_in_progress
            task_icon = in_progress_icon
            task_cursor = "hand2"
            task_date_icon = objectif_date_black_icon
            task_objectif_date_wording = "Deadline :"
            task_objectif_finished_date_text = task_objectif_date
        elif task_id_status == 3:
            task_color_status = color_status_finished
            task_icon = finished_icon
            task_cursor = "arrow"
            task_date_icon = finish_date_black_icon
            task_objectif_date_wording = "Fait le :"
            task_objectif_finished_date_text = task_finished_date
        if to_do_list[i_task]["date_objectif_tache"] != None:
            if task_id_status != 3 and to_do_list[i_task]["date_objectif_tache"] < datetime.date.today():
                task_color_status = color_status_late

        # Création de la tâche
        task_box = Frame(tasks_list_box, bg=task_color_status, height=80)
        task_box.pack_propagate(False)
        task_box.pack(fill="both", pady=(0,2))
        task_container = Frame(task_box, bg=task_color_status, height=80)
        task_container.pack_propagate(False)
        task_container.pack(fill="both")

        # Bouton status
        task_button = Button(task_container, bg=task_color_status, activebackground=task_color_status, relief="flat", borderwidth=0, cursor=task_cursor, image=task_icon)
        task_button.pack(side="left", padx=20)
        task_button.bind("<Enter>", lambda event, task_id_status=task_id_status, task_button=task_button: task_enter(event, task_id_status, task_button))
        task_button.bind("<Leave>", lambda event, task_id_status=task_id_status, task_button=task_button: task_leave(event, task_id_status, task_button))
        task_button.bind("<Button-1>", lambda event, task_id_status=task_id_status, task_id=task_id: task_click(event, task_id_status, task_id))

        # Informations
        task_info_box = Frame(task_container, bg=task_color_status)
        task_info_box.pack(side="left", fill="x", expand=True, padx=(0,20))

        # Informations (Nom de la tâche)
        task_wording_box = Frame(task_info_box, bg=task_color_status, height=30)
        task_wording_box.pack_propagate(False)
        task_wording_box.pack(side="top", fill="both")
        task_wording_label = Label(task_wording_box, bg=task_color_status, text=task_wording, font=font_body_medium, fg=color_black)
        task_wording_label.pack(side="left")

        # Informations (Status et dates)
        task_data_box = Frame(task_info_box, bg=task_color_status, height=30)
        task_data_box.pack_propagate(False)
        task_data_box.pack(side="bottom", fill="both")

        # Informations (Status)
        task_status_box = Frame(task_data_box, bg=task_color_status, width=250, height=30)
        task_status_box.pack_propagate(False)
        task_status_box.pack(side="left", padx=(0,15))
        task_status_canvas = Canvas(task_status_box, width=26, height=26, bg=task_color_status, highlightthickness=0)
        task_status_canvas.create_image(13, 13, image=status_black_icon)
        task_status_canvas.pack(side="left")
        task_status_wording = Label(task_status_box, bg=task_color_status, text="Status :", font=font_body_low_bold, fg=color_black)
        task_status_wording.pack(side="left")
        task_status_text = Label(task_status_box, bg=task_color_status, text=task_status, font=font_body_low, fg=color_black)
        task_status_text.pack(side="left")

        # Informations (Date de création)
        task_creation_date_box = Frame(task_data_box, bg=task_color_status, width=250, height=30)
        task_creation_date_box.pack_propagate(False)
        task_creation_date_box.pack(side="left", padx=(0,15))
        task_creation_date_canvas = Canvas(task_creation_date_box, width=26, height=26, bg=task_color_status, highlightthickness=0)
        task_creation_date_canvas.create_image(13, 13, image=creation_date_black_icon)
        task_creation_date_canvas.pack(side="left")
        task_creation_date_wording = Label(task_creation_date_box, bg=task_color_status, text="Créé le :", font=font_body_low_bold, fg=color_black)
        task_creation_date_wording.pack(side="left")
        task_creation_date_text = Label(task_creation_date_box, bg=task_color_status, text=task_creation_date, font=font_body_low, fg=color_black)
        task_creation_date_text.pack(side="left")

        # Informations (Date objectif ou de clôture)
        task_objectif_finish_date_box = Frame(task_data_box, bg=task_color_status, width=250, height=30)
        task_objectif_finish_date_box.pack_propagate(False)
        task_objectif_finish_date_box.pack(side="left")
        task_objectif_finish_date_canvas = Canvas(task_objectif_finish_date_box, width=26, height=26, bg=task_color_status, highlightthickness=0)
        task_objectif_finish_date_canvas.create_image(13, 13, image=task_date_icon)
        task_objectif_finish_date_canvas.pack(side="left")
        task_objectif_finish_date_wording = Label(task_objectif_finish_date_box, bg=task_color_status, text=task_objectif_date_wording, font=font_body_low_bold, fg=color_black)
        task_objectif_finish_date_wording.pack(side="left")
        task_objectif_finish_date_text = Label(task_objectif_finish_date_box, bg=task_color_status, text=task_objectif_finished_date_text, font=font_body_low, fg=color_black)
        task_objectif_finish_date_text.pack(side="left")

        # Bouton 'Supprimer'
        task_delete_button = Button(task_container, relief="flat", borderwidth=0, bg=color_red_dark, activebackground=color_red_dark, cursor="hand2", image=delete_icon, width=40, height=40)
        task_delete_button.pack(side="right", padx=(0,20))
        task_delete_button.bind("<Enter>", lambda event, task_delete_button=task_delete_button: task_delete_enter(event, task_delete_button))
        task_delete_button.bind("<Leave>", lambda event, task_delete_button=task_delete_button: task_delete_leave(event, task_delete_button))
        task_delete_button.bind("<Button-1>", lambda event, task_wording=task_wording, task_id=task_id, task_container=task_container, task_box=task_box: task_delete_click(event, task_wording, task_id, task_container, task_box))

        # Bouton 'Modifier'
        task_update_button = Button(task_container, relief="flat", borderwidth=0, bg=color_main_medium, activebackground=color_main_medium, cursor="hand2", image=update_icon, width=40, height=40)
        task_update_button.pack(side="right", padx=(0,20))
        task_update_button.bind("<Enter>", lambda event, task_update_button=task_update_button: task_update_enter(event, task_update_button))
        task_update_button.bind("<Leave>", lambda event, task_update_button=task_update_button: task_update_leave(event, task_update_button))
        task_update_button.bind("<Button-1>", lambda event, task_box=task_box, task_container=task_container, task_wording=task_wording, task_id_status=task_id_status, task_creation_date=task_creation_date, task_objectif_date=task_objectif_date, task_finished_date=task_finished_date, task_color_status=task_color_status, task_id=task_id: task_update_click(event, task_box, task_container, task_wording, task_id_status, task_creation_date, task_objectif_date, task_finished_date, task_color_status, task_id))

        # Ajout à la liste pour le scroll
        tasks_list.append({"task_button": task_button, "task_wording_label": task_wording_label, "task_wording_box": task_wording_box, "task_status_canvas": task_status_canvas, "task_status_wording": task_status_wording, "task_status_text": task_status_text, "task_status_box": task_status_box, "task_creation_date_canvas": task_creation_date_canvas, "task_creation_date_wording": task_creation_date_wording, "task_creation_date_text": task_creation_date_text, "task_creation_date_box": task_creation_date_box, "task_objectif_finish_date_canvas": task_objectif_finish_date_canvas, "task_objectif_finish_date_wording": task_objectif_finish_date_wording, "task_objectif_finish_date_text": task_objectif_finish_date_text, "task_objectif_finish_date_box": task_objectif_finish_date_box, "task_data_box": task_data_box, "task_info_box": task_info_box, "task_delete_button": task_delete_button, "task_update_button": task_update_button, "task_container": task_container, "task_box": task_box})
    
    # Calculer la hauteur totale des éléments
    total_height = len(to_do_list) * 94.01

    # Définir la hauteur du Canvas en conséquence
    tasks_window.config(scrollregion=(0, 0, 0, total_height))

    # Vérifier la visibilité de la barre de défilement
    tasks_window.yview_moveto(0.0)
    # Forcer la mise à jour de la géométrie de la Frame
    tasks_list_box.update_idletasks()

    tasks_window.columnconfigure(0, weight=1)
    scroll_visibility(tasks_list)

def ydm_to_dmy(task_date):
    if task_date == "None":
        task_date = "Aucune"
    else:
        year = ""
        month = ""
        day = ""
        for i_character in range (len(task_date)):
            if i_character < 4:
                year += task_date[i_character]
            elif 4 < i_character < 7:
                month += task_date[i_character]
            elif i_character > 7:
                day += task_date[i_character]
        task_date = f"{day}/{month}/{year}"
        return task_date
    
def dmy_to_ydm(task_date):
    if task_date != "NULL":
        year = ""
        month = ""
        day = ""
        for i_character in range (len(task_date)):
            if i_character < 2:
                day += task_date[i_character]
            elif 2 < i_character < 5:
                month += task_date[i_character]
            elif i_character > 5:
                year += task_date[i_character]
        task_date = f"'{year}-{month}-{day}'"
        return task_date

# Bouton 'Status'
def task_enter(event,task_id_status, task_button):
    if task_id_status == 1:
        task_button.config(image=in_progress_icon)
    elif task_id_status == 2:
        task_button.config(image=finished_icon)

def task_leave(event, task_id_status, task_button):
    if task_id_status == 1:
        task_button.config(image=to_do_icon)
    elif task_id_status == 2:
        task_button.config(image=in_progress_icon)

def task_click(event, task_id_status, task_id):
    if task_id_status == 1:
        mycursor.execute(f"UPDATE tache SET id_etat=2 WHERE id_tache={task_id};")
        tasks_print()
    elif task_id_status == 2:
        mycursor.execute(f"UPDATE tache SET id_etat=3, date_realisation_tache='{datetime.date.today()}' WHERE id_tache={task_id};")
        tasks_print()

# Bouton 'Supprimer'
def task_delete_enter(event, task_delete_button):
    task_delete_button.config(bg=color_red_light)

def task_delete_leave(event, task_delete_button):
    task_delete_button.config(bg=color_red_dark)

def task_delete_validate_enter(event, task_delete_validate_button):
    task_delete_validate_button.config(bg=color_red_light)

def task_delete_validate_leave(event, task_delete_validate_button):
    task_delete_validate_button.config(bg=color_red_dark)

def task_delete_validate_click(event, task_id):
    mycursor.execute(f"DELETE FROM tache WHERE id_tache={task_id};")
    tasks_print()

def task_delete_cancel_click(event, task_delete_container, task_container_save):
    task_delete_container.destroy()
    task_container_save.pack(fill="both")

def task_delete_click(event, task_wording, task_id, task_container,task_box):
    task_container_save = task_container
    task_container.pack_forget()

    task_delete_container = Frame(task_box, bg=color_red_warnning, height=80)
    task_delete_container.pack_propagate(False)
    task_delete_container.pack(fill="both")

    # Icone
    task_delete_icon_box = Canvas(task_delete_container, width=92, height=80, bg=color_red_warnning, highlightthickness=0)
    task_delete_icon_box.create_image(46, 40, image=in_deletion)
    task_delete_icon_box.pack(side="left")

    # Infos
    task_delete_infos_box = Frame(task_delete_container, bg=color_red_warnning)
    task_delete_infos_box.pack(side="left", fill="x", expand=True)

    # Message
    task_delete_wording_box = Frame(task_delete_infos_box, bg=color_red_warnning, height=30)
    task_delete_wording_box.pack_propagate(False)
    task_delete_wording_box.pack(side="top", fill="both", padx=(0,20))
    task_delete_wording_label = Label(task_delete_wording_box, bg=color_red_warnning, text="Êtes vous sur de vouloir supprimer cette tâche ? Cette action est irréversible !", font=font_body_medium_bold, fg=color_white)
    task_delete_wording_label.pack(side="left")

    # Tâche
    task_delete_data_box = Frame(task_delete_infos_box, bg=color_red_warnning, height=30)
    task_delete_data_box.pack_propagate(False)
    task_delete_data_box.pack(side="bottom", fill="both")
    task_delete_wording_label = Label(task_delete_data_box, bg=color_red_warnning, text=f"'{task_wording}'", font=font_body_medium, fg=color_white)
    task_delete_wording_label.pack(side="left")

    # Bouton 'Valider'
    task_delete_validate_button = Button(task_delete_container, relief="flat", borderwidth=0, bg=color_red_dark, activebackground=color_red_dark, cursor="hand2", image=delete_icon, width=40, height=40)
    task_delete_validate_button.pack(side="right", padx=(0,20))
    task_delete_validate_button.bind("<Enter>", lambda event, task_delete_validate_button=task_delete_validate_button: task_delete_validate_enter(event, task_delete_validate_button))
    task_delete_validate_button.bind("<Leave>", lambda event, task_delete_validate_button=task_delete_validate_button: task_delete_validate_leave(event, task_delete_validate_button))
    task_delete_validate_button.bind("<Button-1>", lambda event, task_id=task_id: task_delete_validate_click(event, task_id))

    # Bouton 'Annuler'
    task_delete_cancel_button = Button(task_delete_container, relief="flat", borderwidth=0, bg=color_gray_dark, activebackground=color_gray_dark, cursor="hand2", image=back_icon, width=40, height=40)
    task_delete_cancel_button.pack(side="right", padx=(0,20))
    task_delete_cancel_button.bind("<Enter>", lambda event, cancel_button=task_delete_cancel_button: cancel_enter(event, cancel_button))
    task_delete_cancel_button.bind("<Leave>", lambda event, cancel_button=task_delete_cancel_button: cancel_leave(event, cancel_button))
    task_delete_cancel_button.bind("<Button-1>",lambda event, task_delete_container=task_delete_container, task_container_save=task_container_save: task_delete_cancel_click(event, task_delete_container, task_container_save))

# Bouton 'Update'
def task_cancel_button_click(event, task_modif_container, task_container_save):
    task_modif_container.destroy()
    task_container_save.pack(fill="both")
    
def task_update_enter(event, task_update_button):
    task_update_button.config(bg=color_main_light)

def task_update_leave(event, task_update_button):
    task_update_button.config(bg=color_main_medium)

def print_cloture_date(event, task_modif_finished_date_box, task_modif_status_list):
    if task_modif_status_list.get() == "Terminée":
        task_modif_finished_date_box.pack(side="left")
    else : 
        task_modif_finished_date_box.pack_forget()

def task_validate_click(event, task_modif_container, task_container_save, task_modif_wording_value, task_modif_creation_date_value, task_modif_finished_date_value, task_modif_objectif_date_value, task_modif_status_list, task_id):
    creation_date = task_modif_creation_date_value.get()
    finished_date = task_modif_finished_date_value.get()
    objectif_date = task_modif_objectif_date_value.get()
    if task_modif_status_list.get() == "À faire":
        task_modif_status = 1
        finished_date = "NULL"
    elif task_modif_status_list.get() == "En cours":
        task_modif_status = 2
        finished_date = "NULL"
    elif task_modif_status_list.get() == "Terminée":
        task_modif_status = 3
        finished_date = dmy_to_ydm(finished_date)
    creation_date = dmy_to_ydm(creation_date)
    objectif_date = dmy_to_ydm(objectif_date)
    mycursor.execute(f"UPDATE tache SET libelle_tache='{task_modif_wording_value.get()}', date_creation_tache={creation_date}, date_realisation_tache={finished_date}, date_objectif_tache={objectif_date}, id_etat={task_modif_status} WHERE id_tache={task_id};")
    task_modif_container.destroy()
    task_container_save.pack(fill="both")
    tasks_print()

def task_update_click(event, task_box, task_container, task_wording, task_id_status, task_creation_date, task_objectif_date, task_finished_date, task_color_status, task_id):
    task_container_save = task_container
    task_container.pack_forget()

    task_modif_container = Frame(task_box, bg=task_color_status, height=80)
    task_modif_container.pack_propagate(False)
    task_modif_container.pack(fill="both")

    # Icone
    task_modif_icon_box = Canvas(task_modif_container, width=92, height=80, bg=task_color_status, highlightthickness=0)
    task_modif_icon_box.create_image(46, 40, image=in_modification)
    task_modif_icon_box.pack(side="left")

    # Infos
    task_modif_infos_box = Frame(task_modif_container, bg=task_color_status)
    task_modif_infos_box.pack(side="left", fill="x", expand=True)

    # Libéllé
    task_modif_wording_box = Frame(task_modif_infos_box, bg=task_color_status, height=30)
    task_modif_wording_box.pack_propagate(False)
    task_modif_wording_box.pack(side="top", fill="both", padx=(0,20))
    task_modif_wording_label = Label(task_modif_wording_box, bg=task_color_status, text="Libéllé :", font=font_body_medium_bold, fg=color_black)
    task_modif_wording_label.pack(side="left")
    task_modif_wording_validate_command = window.register(wording_max_character)
    task_modif_wording_value = Entry(task_modif_wording_box, bg=color_white, validate="key", validatecommand=(task_modif_wording_validate_command, "%P"), width=60, font=font_body_medium, fg=color_black, insertbackground=color_black)
    task_modif_wording_value.insert(0, task_wording)
    task_modif_wording_value.pack(side="left", padx=(8,0))

    # Datas
    task_modif_data_box = Frame(task_modif_infos_box, bg=task_color_status, height=30)
    task_modif_data_box.pack_propagate(False)
    task_modif_data_box.pack(side="bottom", fill="both")

    # Status
    task_modif_status_box = Frame(task_modif_data_box, bg=task_color_status, width=250, height=30)
    task_modif_status_box.pack_propagate(False)
    task_modif_status_box.pack(side="left", padx=(0,15))
    task_modif_status_icon = Canvas(task_modif_status_box, width=26, height=26, bg=task_color_status, highlightthickness=0)
    task_modif_status_icon.create_image(13, 13, image=status_black_icon)
    task_modif_status_icon.pack(side="left")
    task_modif_status_wording = Label(task_modif_status_box, bg=task_color_status, text="Status :", font=font_body_low_bold, fg=color_black)
    task_modif_status_wording.pack(side="left")
    task_modif_status_options = ["À faire", "En cours", "Terminée"]
    task_modif_status_list = ttk.Combobox(task_modif_status_box, values=task_modif_status_options, width=13, font=font_body_low, state="readonly")
    task_modif_status_list.set(task_modif_status_options[task_id_status-1])

    task_modif_status_list.bind("<<ComboboxSelected>>", lambda event, task_modif_status_list=task_modif_status_list: print_cloture_date(event, task_modif_finished_date_box, task_modif_status_list))
    task_modif_status_list.pack(side="left")

    # Date Création
    task_modif_creation_date_box = Frame(task_modif_data_box, bg=task_color_status, width=250, height=30)
    task_modif_creation_date_box.pack_propagate(False)
    task_modif_creation_date_box.pack(side="left", padx=(0,15))
    task_modif_creation_date_icon = Canvas(task_modif_creation_date_box, width=26, height=26, bg=task_color_status, highlightthickness=0)
    task_modif_creation_date_icon.create_image(13, 13, image=creation_date_black_icon)
    task_modif_creation_date_icon.pack(side="left")
    task_modif_creation_date_wording = Label(task_modif_creation_date_box, bg=task_color_status, text=f"Créé le :", font=font_body_low_bold, fg=color_black)
    task_modif_creation_date_wording.pack(side="left")
    task_modif_creation_date_value = DateEntry(task_modif_creation_date_box, bg=task_color_status, locale='fr_FR', relief="flat", font=font_body_low, fg=color_black, borderwidth=0, showothermonthdays=False, background=color_main_medium, foreground=color_white, headersbackground=color_main_light, headersforeground=color_white, bordercolor=color_main_light, normalbackground=color_white, normalforeground=color_black, weekendbackground=color_white, weekendforeground=color_black, selectbackground=color_main_medium, selectforeground=color_white)
    task_modif_creation_date_value.set_date(task_creation_date)
    task_modif_creation_date_value.config(maxdate=datetime.date.today())
    task_modif_creation_date_value.pack(side="left")
    for date in task_modif_creation_date_value._top_cal.winfo_children():
        date.bind("<Enter>", calendar_enter)
        date.bind("<Leave>", calendar_leave)

    # Date objectif
    task_modif_objectif_date_box = Frame(task_modif_data_box, bg=task_color_status, width=250, height=30)
    task_modif_objectif_date_box.pack_propagate(False)
    task_modif_objectif_date_box.pack(side="left", padx=(0,15))
    task_modif_objectif_date_icon = Canvas(task_modif_objectif_date_box, width=26, height=26, bg=task_color_status, highlightthickness=0)
    task_modif_objectif_date_icon.create_image(13, 13, image=objectif_date_black_icon)
    task_modif_objectif_date_icon.pack(side="left")
    task_modif_objectif_date_wording = Label(task_modif_objectif_date_box, bg=task_color_status, text="Deadline :", font=font_body_low_bold, fg=color_black)
    task_modif_objectif_date_wording.pack(side="left")
    task_modif_objectif_date_value = DateEntry(task_modif_objectif_date_box, bg=task_color_status, locale='fr_FR', relief="flat", font=font_body_low, fg=color_black, borderwidth=0, showothermonthdays=False, background=color_main_medium, foreground=color_white, headersbackground=color_main_light, headersforeground=color_white, bordercolor=color_main_light, normalbackground=color_white, normalforeground=color_black, weekendbackground=color_white, weekendforeground=color_black, selectbackground=color_main_medium, selectforeground=color_white)
    task_modif_objectif_date_value.set_date(task_objectif_date)
    task_modif_objectif_date_value.config(mindate=datetime.date.today())
    task_modif_objectif_date_value.pack(side="left")
    for date in task_modif_objectif_date_value._top_cal.winfo_children():
        date.bind("<Enter>", calendar_enter)
        date.bind("<Leave>", calendar_leave)

    # Date de clôture
    task_modif_finished_date_box = Frame(task_modif_data_box, bg=task_color_status, width=250, height=30)
    task_modif_finished_date_box = Frame(task_modif_data_box, bg=task_color_status, width=250, height=30)
    task_modif_finished_date_box.pack_propagate(False)
    task_modif_finished_date_icon = Canvas(task_modif_finished_date_box, width=26, height=26, bg=task_color_status, highlightthickness=0)
    task_modif_finished_date_icon.create_image(13, 13, image=objectif_date_black_icon)
    task_modif_finished_date_icon.pack(side="left")
    task_modif_finished_date_wording = Label(task_modif_finished_date_box, bg=task_color_status, text="Fait le :", font=font_body_low_bold, fg=color_black)
    task_modif_finished_date_wording.pack(side="left")
    task_modif_finished_date_value = DateEntry(task_modif_finished_date_box, bg=task_color_status, locale='fr_FR', relief="flat", font=font_body_low, fg=color_black, borderwidth=0, showothermonthdays=False, background=color_main_medium, foreground=color_white, headersbackground=color_main_light, headersforeground=color_white, bordercolor=color_main_light, normalbackground=color_white, normalforeground=color_black, weekendbackground=color_white, weekendforeground=color_black, selectbackground=color_main_medium, selectforeground=color_white)
    task_modif_finished_date_value.set_date(task_finished_date)
    task_modif_finished_date_value.config(maxdate=datetime.date.today())
    task_modif_finished_date_value.pack(side="left")
    for date in task_modif_finished_date_value._top_cal.winfo_children():
        date.bind("<Enter>", calendar_enter)
        date.bind("<Leave>", calendar_leave)
    print_cloture_date(event, task_modif_finished_date_box, task_modif_status_list)

    # Bouton 'Valider'
    task_modif_validate_button = Button(task_modif_container, relief="flat", borderwidth=0, bg=color_green_dark, activebackground=color_green_dark, cursor="hand2", image=validate_icon, width=40, height=40)
    task_modif_validate_button.pack(side="right", padx=(0,20))
    task_modif_validate_button.bind("<Enter>", lambda event, validate_button=task_modif_validate_button: validate_enter(event, validate_button))
    task_modif_validate_button.bind("<Leave>", lambda event, validate_button=task_modif_validate_button: validate_leave(event, validate_button))
    task_modif_validate_button.bind("<Button-1>", lambda event, task_modif_container=task_modif_container, task_container_save=task_container_save, task_modif_wording_value=task_modif_wording_value, task_modif_creation_date_value=task_modif_creation_date_value, task_modif_finished_date_value=task_modif_finished_date_value, task_modif_objectif_date_value=task_modif_objectif_date_value, task_modif_status_list=task_modif_status_list, task_id=task_id: task_validate_click(event, task_modif_container, task_container_save, task_modif_wording_value, task_modif_creation_date_value, task_modif_finished_date_value, task_modif_objectif_date_value, task_modif_status_list, task_id))

    # Bouton 'Annuler'
    task_modif_cancel_button = Button(task_modif_container, relief="flat", borderwidth=0, bg=color_gray_dark, activebackground=color_gray_dark, cursor="hand2", image=back_icon, width=40, height=40)
    task_modif_cancel_button.pack(side="right", padx=(0,20))
    task_modif_cancel_button.bind("<Enter>", lambda event, cancel_button=task_modif_cancel_button: cancel_enter(event, cancel_button))
    task_modif_cancel_button.bind("<Leave>", lambda event, cancel_button=task_modif_cancel_button: cancel_leave(event, cancel_button))
    task_modif_cancel_button.bind("<Button-1>", lambda event, task_modif_container=task_modif_container, task_container_save=task_container_save: task_cancel_button_click(event, task_modif_container, task_container_save))

# endregion : Fonctions - Main
# ========================================


# endregion : FONCTIONS
# ==================================================
    

# ==================================================
# region : PROGRAMME


# ========================================
# region : Programme - Header
    
header_box = Frame(window, bg=color_main_dark)
header_box.pack(side="top", fill="both")

# ==============================
# region : Programme - Logo et Titre
logo_title_box = Frame(header_box, bg=color_main_dark)
logo_title_box.pack()

# Logo
logo = Canvas(logo_title_box, bg=color_main_dark, width=80, height=80, highlightthickness=0)
logo.create_image(40, 40, image=logo_icon)
logo.pack(side="left")

# Titre
title = Label(logo_title_box, bg=color_main_dark, text="PyDo", font=font_title, fg=color_white)
title.pack(side="left")
# endregion : Programme - Logo et Titre
# ==============================


# ==============================
# region : Programme - Barre de filtre

filter_box = Frame(window, bg=color_main_medium)
filter_box.pack(fill="both")
buttons_box = Frame(filter_box, bg=color_main_medium)
buttons_box.pack(anchor="center")

# Filtre 'À faire'
to_do_filter = Button(buttons_box, bg=color_main_medium, activebackground=color_main_medium, relief="flat", borderwidth=0, font=font_body_medium, fg=color_white, activeforeground=color_main_light, cursor="hand2", image=visibility_on_white_icon, text="À faire", compound="left", padx=5)
to_do_status = True
to_do_filter.bind("<Enter>", to_do_enter)
to_do_filter.bind("<Leave>", to_do_leave)
to_do_filter.bind("<Button-1>", to_do_click)
to_do_filter.pack(side="left")

# Séparateur
separator = Frame(buttons_box, width=1, height=20, bg=color_black)
separator.pack(side="left", padx=20)

# Filtre 'En cours'
in_progress_filter = Button(buttons_box, bg=color_main_medium, activebackground=color_main_medium, relief="flat", borderwidth=0, font=font_body_medium, fg=color_white, activeforeground=color_main_light, cursor="hand2", image=visibility_on_white_icon, text="En cours", compound="left", padx=5)
in_progress_status = True
in_progress_filter.bind("<Enter>", in_progress_enter)
in_progress_filter.bind("<Leave>", in_progress_leave)
in_progress_filter.bind("<Button-1>", in_progress_click)
in_progress_filter.pack(side="left")

# Séparateur
separator = Frame(buttons_box, width=1, height=20, bg=color_black)
separator.pack(side="left", padx=20)

# Filtre 'Terminée'
finished_filter = Button(buttons_box, bg=color_main_medium, activebackground=color_main_medium, relief="flat", borderwidth=0, font=font_body_medium, fg=color_main_light, activeforeground=color_main_light, cursor="hand2", image=visibility_off_blue_icon, text="Terminée", compound="left", padx=5)
finished_status = False
finished_filter.bind("<Enter>", finished_enter)
finished_filter.bind("<Leave>", finished_leave)
finished_filter.bind("<Button-1>", finished_click)
finished_filter.pack(side="left")

# endregion : Programme - Barre de filtre
# ==============================


# ==============================
# region : Programme - Barre d'ajout

new_task_box = Frame(window, bg=color_white, height=80)
new_task_box.pack_propagate(False)
new_task_box.pack(fill="both", pady=(0,2))
new_task_default()

# endregion : Programme - Barre d'ajout
# ==============================


# endregion : Programme - Header
# ========================================


# ========================================
# region : Programme - Footer

footer = Frame(window, bg=color_main_light)
footer.pack(side="bottom", fill="both")
footer_box = Frame(footer, bg=color_main_light)
footer_box.pack(anchor="center")

# Bouton 'Linkedin'
linkedin_button = Button(footer_box, relief="flat", borderwidth=0, bg=color_main_light, activebackground=color_main_light, cursor="hand2", image=linkedin_black_icon)
linkedin_button.pack(side="left", padx=5)
linkedin_button.bind("<Enter>", linkedin_enter)
linkedin_button.bind("<Leave>", linkedin_leave)
linkedin_button.bind("<Button-1>", linkedin_click)

# Crédits
credits = Label(footer_box, bg=color_main_light, text="Développé par", font=font_body_low, height=2, fg=color_black)
credits.pack(side="left")
name = Label(footer_box, bg=color_main_light, text="Nicolas Coquatrix", font=font_body_low_bold, height=2, fg=color_black)
name.pack(side="left")

# Bouton 'Github'
github_button = Button(footer_box, relief="flat", borderwidth=0, bg=color_main_light, activebackground=color_main_light, cursor="hand2", image=github_black_icon)
github_button.pack(side="left", padx=5)
github_button.bind("<Enter>", github_enter)
github_button.bind("<Leave>", github_leave)
github_button.bind("<Button-1>", github_click)


# endregion : Programme - Footer
# ========================================


# ========================================
# region : Programme - Main

tasks_window = Canvas(window, bg=color_main_dark, highlightthickness=0)
tasks_window.pack(side="left", fill="both", expand=True)
tasks_list_box = Frame(tasks_window, bg=color_main_dark, height=9999, width=1800)
tasks_list_box.pack_propagate(False)
tasks_window.create_window((0, 0), window=tasks_list_box, anchor="nw")
tasks_list_box.bind("<MouseWheel>", scroll)
tasks_window.bind("<Configure>", tasks_window_resized)
tasks_print()

# endregion : Programme - Main
# ========================================


# endregion : PROGRAMME
# ==================================================


# ==================================================
# region : DÉMARRAGE DU PROGRAMME

window.mainloop()

# endregion : DÉMARRAGE DU PROGRAMME
# ==================================================


# Développé par Nicolas Coquatrix