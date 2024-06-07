from requete import mesRequetes,updateKilometres,updatePrix, GetPrixVente, GetKmVente, GetMotoAnnee, GetByMarque, check_user, check_login, InsertUsers, InsertMoto, InsertLieuxDeVentes, InsertMarque, InsertVentes, GetIdMarque, GetIdLieuxDeVentes, GetIdMoto, DeleteMotoByID, DeleteLieuxByID, DeleteMarqueByID, DeleteVentesByID


_dbConfig = {
        'driver' : "MySQL",
        'db' : 'moto',
        'host' : "localhost",
        'user' : "root",
        'passwd' : "",
        'port' : 3306    
    }

def majParamsConnexion() -> None:
    try :
        with open("config.txt") as f :
            for ligne in f :
                if ligne[0] == '#' or ligne[0] == '[' or len(ligne)<3 :
                    continue
                champs = ligne.split(':')
                _dbConfig[champs[0].strip()] = champs[1].strip().strip('"')
    except FileNotFoundError as e :
        print("'config.txt' absent, utilisation des valeurs par défaut")

def dbConnect():
    import pymysql
    db = pymysql.connect(host = _dbConfig['host'], user=_dbConfig['user'], passwd=_dbConfig['passwd'], port=int(_dbConfig['port']), db = _dbConfig['db'])
    cursor=db.cursor()
    return (db,db.cursor())

def createBaseMySQL() -> None :
    import pymysql
    db = pymysql.connect(host = _dbConfig['host'], user=_dbConfig['user'], passwd=_dbConfig['passwd'], port=int(_dbConfig['port']))
    cursor = db.cursor()
    cursor.execute(mesRequetes["drop"])
    cursor.execute(mesRequetes["createBase"])
    cursor.execute(mesRequetes["use"])
    cursor.execute(mesRequetes["createMoto"])
    cursor.execute(mesRequetes["createLieuxDeVentes"])
    cursor.execute(mesRequetes["createMarque"])
    cursor.execute(mesRequetes["createVentes"])
    cursor.execute(mesRequetes["createUsers"])
    cursor.execute(mesRequetes["insertAdmin"])
    cursor.execute(mesRequetes["keyVentes"])
    cursor.execute(mesRequetes["keyMoto"])


def initBase() -> None :
    """ Vérifie que la base existe, sinon propose de la créer en mode CLI.
            Jette une exception si paramètres de connexion incorrects """
    majParamsConnexion()     
    match _dbConfig['driver'].upper() :
        case "MYSQL" :
            try :
                import pymysql
                db = pymysql.connect(host=_dbConfig['host'], user=_dbConfig['user'], passwd=_dbConfig['passwd'], port=int(_dbConfig['port']), db =_dbConfig['db'] )
                cursor = db.cursor()
                cursor.execute(mesRequetes["getAllMoto"])
            except pymysql.err.OperationalError as e:
                print(e)
                if '1044' in str(e) :
                    print (f"Vérifiez les paramètres de connexion à la base {_dbConfig['db']}")
                    raise e
                elif '1049' in str(e):
                    choix = input("La base de données n'existe pas. Voulez-vous créer une base 'moto' standard ? (o/n) :")
                    if choix.upper() in ['O', 'OUI', 'Y', 'YES']:
                        createBaseMySQL()
                        print("Base de données créée avec succès.")
                    else:
                        raise e
        case _ :
            print (f"SGBDR {_dbConfig['driver'].upper()} non géré")
            raise ValueError
        

def execute(req: str, params: tuple = None):
    db, cursor = dbConnect()
    cursor.execute(req, params)
    res = None
    if "select" in req.lower():
        res = cursor.fetchall()
    else:
        db.commit()
        res = cursor.rowcount
    cursor.close()
    db.close()
    return res

#Insertion

def insertMoto(modele: str, annee: str, cylindree: str, puissance: str,immatriculation : str, prix_neuf: str, idMarque: str):
    req = InsertMoto(modele, annee, cylindree, puissance,immatriculation, prix_neuf, idMarque)
    execute(req)

def insertLieuxDeVentes(adresse: str, codePostal: str, ville: str , nomMagasin: str):
    req = InsertLieuxDeVentes(nomMagasin, adresse, codePostal, ville.capitalize())
    execute(req)

def insertMarque(nom : str, nationnalité : str):
    req = InsertMarque(nom.upper(), nationnalité.capitalize())
    execute(req)

def insertVentes(prix_occasion: str, kilomètres : str, idMoto: str, idLieu: str):
    req = InsertVentes(prix_occasion,kilomètres, idMoto, idLieu)
    execute(req)

def insertUsers(login: str, mdp : str):
    req = InsertUsers(login,mdp)
    execute(req)

#Modifications 

def UpdateKilometres(km : str, idVente : str):
    req = updateKilometres(km, idVente)
    execute(req)


def UpdatePrix(prix : str, idVente : str):
    req = updatePrix(prix, idVente)
    execute(req)

#insertion avec csv
import csv

def insertMarqueCSV(nom_fichier: str):
    try:
        with open(nom_fichier, 'r', newline='', encoding="utf8") as fichier_csv:
            spamreader = csv.reader(fichier_csv, delimiter=";")
            entete = next(spamreader) 
            if len(entete) != 2:
                raise ValueError("Le fichier CSV n'est pas au bon format. Assurez-vous qu'il contient deux colonnes : nom et nationalité.")
            for ligne in spamreader:
                if len(ligne) != 2:
                    raise ValueError("Le fichier CSV n'est pas au bon format. Assurez-vous que chaque ligne contient le nom et la nationalité.")
                nom = ligne[0].strip().upper()  # Supprimer les espaces et mettre en majuscules
                nationalite = ligne[1].strip().capitalize()  # Supprimer les espaces et mettre en majuscules
                insertMarque(nom, nationalite)
                
        # print("Insertion depuis le fichier CSV terminée avec succès.")
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Le fichier {nom_fichier} n'a pas été trouvé.")
    except Exception as e:
        raise e

def getIdMarque(nom_marque):
    try:
        req = GetIdMarque(nom_marque)  # Utilisez la fonction GetIdMarque du fichier de requêtes pour obtenir la requête SQL
        id_marque = execute(req)
        if id_marque:
            return id_marque[0][0]  # La requête SELECT retourne une liste de tuples, nous récupérons le premier élément de la première ligne
        else:
            raise ValueError("La marque spécifiée n'existe pas dans la base de données.")
    except Exception as e:
        print(f"Une erreur s'est produite lors de la récupération de l'ID de la marque : {e}")

def insertMotoCSV(nom_fichier):
    try:
        with open(nom_fichier, 'r', newline='') as fichier_csv:
            spamreader = csv.reader(fichier_csv, delimiter=";")
            entete = next(spamreader)  # Lire l'en-tête pour vérifier le format
            if len(entete) != 7:
                raise ValueError("Le fichier CSV n'est pas au bon format. Assurez-vous qu'il contient sept colonnes : modèle, année, cylindrée, puissance, immatriculation, prix neuf et nom de la marque.")
            for ligne in spamreader:
                if len(ligne) != 7:
                    raise ValueError("Le fichier CSV n'est pas au bon format. Assurez-vous que chaque ligne contient les informations nécessaires pour une moto.")
                
                # Extraction des données de la ligne
                modele = ligne[0].strip()
                annee = ligne[1].strip()
                cylindree = ligne[2].strip()
                puissance = ligne[3].strip()
                immatriculation = ligne[4].strip()
                prix_neuf = ligne[5].strip()
                nom_marque = ligne[6].strip()
                
                # Obtenir l'ID de la marque
                id_marque = getIdMarque(nom_marque)

                # Insérer la moto dans la base de données
                insertMoto(modele, annee, cylindree, puissance, immatriculation, prix_neuf, id_marque)
                
        # print("Insertion depuis le fichier CSV terminée avec succès")
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Le fichier {nom_fichier} n'a pas été trouvé.")
    except Exception as e:
        raise e

def insertLieuxDeVentesCSV(nom_fichier: str):
    try:
        with open(nom_fichier, 'r', newline='', encoding="utf8") as fichier_csv:
            spamreader = csv.reader(fichier_csv, delimiter=";")
            entete = next(spamreader) 
            if len(entete) != 4:
                raise ValueError("Le fichier CSV n'est pas au bon format. Assurez-vous qu'il contient quatre colonnes : nomMagasin, adresse, code postal et ville.")
            for ligne in spamreader:
                if len(ligne) != 4:
                    raise ValueError("Le fichier CSV n'est pas au bon format. Assurez-vous qu'il contient quatre colonnes : nomMagasin, adresse, code postal et ville.")
                nomMagasin = ligne[0].strip()
                adresse = ligne[1].strip()
                codePostal = ligne[2].strip()
                ville = ligne[3].strip()

                insertLieuxDeVentes(adresse, codePostal, ville, nomMagasin)    

        # print("Insertion depuis le fichier CSV terminée avec succès.")
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Le fichier {nom_fichier} n'a pas été trouvé.")
    except Exception as e:
        raise e

def getIdLieuxDeVentes(adresse):
    try:
        req = GetIdLieuxDeVentes(adresse)  
        id_Lieu = execute(req)
        if id_Lieu:
            return id_Lieu[0][0]  
        else:
            raise ValueError("La marque spécifiée n'existe pas dans la base de données.")
    except Exception as e:
        print(f"Une erreur s'est produite lors de la récupération de l'ID de la marque : {e}")

def getIdMoto(immatriculation):
    try:
        req = GetIdMoto(immatriculation)  
        id_Moto = execute(req)
        if id_Moto:
            return id_Moto[0][0]  
        else:
            raise ValueError("La marque spécifiée n'existe pas dans la base de données.")
    except Exception as e:
        print(f"Une erreur s'est produite lors de la récupération de l'ID de la marque : {e}")
        
def Check_login(login, mdp):
    query, values = check_login(login, mdp)
    res = execute(query, values)
    return res

def Check_user(login):
    query, values = check_user(login)
    res = execute(query, values)
    return res

def insertVentesCSV(nom_fichier: str):
    try:
        with open(nom_fichier, 'r', newline='', encoding="utf8") as fichier_csv:
            l=[]
            spamreader = csv.reader(fichier_csv, delimiter=";")
            entete = next(spamreader) 
            if len(entete) != 4:
                raise ValueError("Le fichier CSV n'est pas au bon format. Assurez-vous qu'il contient quatres colonnes : prix occasion, kilomètres, immatriculation et adresse.")
            for ligne in spamreader:
                if len(ligne) != 4:
                    raise ValueError("Le fichier CSV n'est pas au bon format. Assurez-vous qu'il contient quatres colonnes : prix occasion, kilomètres, immatriculation et adresse.")
                prixOccasion = ligne[0].strip()
                kilomètres = ligne[1].strip()
                immatriculation = ligne[2].strip()
                adresse = ligne[3].strip()
                
                
                id_moto = getIdMoto(immatriculation)
                if not id_moto:
                    raise ValueError(f"La moto avec l'immatriculation {immatriculation} n'a pas été trouvée dans la base de données.")
                
                
                id_lieu_vente = getIdLieuxDeVentes(adresse)
                if not id_lieu_vente:
                    raise ValueError(f"Le lieu de vente avec l'adresse {adresse} n'a pas été trouvé dans la base de données.")
                
                
                insertVentes(prixOccasion, kilomètres, id_moto, id_lieu_vente)

        # print("Insertion depuis le fichier CSV terminée avec succès.")
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Le fichier {nom_fichier} n'a pas été trouvé.")
    except Exception as e:
        raise e

#Suppresion 

def deleteMotoByID(idMoto: str):
    req = DeleteMotoByID(idMoto)
    execute(req)

def deleteLieuxByID(idLieu: str):
    req = DeleteLieuxByID(idLieu)
    execute(req)

def deleteMarqueByID(idMarque: str):
    req = DeleteMarqueByID(idMarque)
    execute(req)

def deleteVentesByID(idVente: str):
    req = DeleteVentesByID(idVente)
    execute(req)
    
#Affichage 

def getByMarque(nom):
    req = GetByMarque(nom)
    resultats = execute(req)
    motos = []
    for t in resultats:
        moto = {
            "modele": t[0],
            "annee": t[1],
            "cylindree": t[2],
            "puissance": t[3],
            "immatriculation": t[4],
            "prix_neuf": t[5],
            "marque": t[6]
        }
        motos.append(moto)
    return motos


def getMotoAnnee(annee):
    req = GetMotoAnnee(annee)
    resultats = execute(req)
    motos = []
    for t in resultats:
        moto = {
            "modele": t[0],
            "annee": t[1],
            "cylindree": t[2],
            "puissance": t[3],
            "immatriculation": t[4],
            "prix_neuf": t[5],
            "marque": t[6]
        }
        motos.append(moto)
    return motos




def getMarque() -> list :
    """ liste de tuples "marque" """
    req = mesRequetes["getAllMarque"]
    marques = []
    for t in execute(req) :
        marques.append(t)
    return marques

def marquesStr() -> str:
    """ Génère une chaîne de caractères avec une phrase pour chaque marque de moto dans la base. """
    marques = getMarque()
    marquesCh = ""
    for marque in marques:
        marquesCh += f"{marque[1]} est une marque de moto {marque[2]}.\n"
    return marquesCh

def marquesID() -> str:
    """ Génère une chaîne de caractères pour le nom des marques et leurs ID. """
    marques = getMarque()
    marquesCh = ""
    for marque in marques:
        marquesCh += f"{marque[0]} : {marque[1]}\n"
    return marquesCh


def getMoto() -> list :
    """ getEtudiants() -> liste de tuples "Etudiant"
    Rend le contenu de la base sous forme d'une liste de tuples.
    Attention, la date sera convertie en chaîne format ISO !!! """
    req = mesRequetes["getAllMoto"]
    motos = []
    for t in execute(req) :
        motos.append(t)
    return motos


def motoStr() -> str:
    """ Génère une chaîne de caractères avec une phrase pour chaque moto. """
    motos = getMoto()
    motoCh = ""
    for moto in motos:
        motoCh += f"La moto fait {moto[1]} cm³ son modèle est '{moto[2]}' de chez {moto[3]}, elle est de {moto[4]} fait {moto[5]} chevaux, son immatriculation est {moto[6]} et son prix neuf est de {moto[7]} €.\n"
    return motoCh


def motoID() -> str:
    """ Génère une chaîne de caractères avec une phrase pour chaque moto. """
    motos = getMoto()
    motoCh = ""
    for moto in motos:
        motoCh += f"{moto[0]} : {moto[3]} {moto[1]} {moto[2]} immatriculé {moto[6]}\n"
    return motoCh

def getLieuxDeVente() -> list :
    """ getEtudiants() -> liste de tuples "Etudiant"
    Rend le contenu de la base sous forme d'une liste de tuples.
    Attention, la date sera convertie en chaîne format ISO !!! """
    req = mesRequetes["getAllLdv"]
    LDV = []
    for t in execute(req) :
        LDV.append(t)
    return LDV

def lieuxDeVenteStr() -> str:
    """ Génère une chaîne de caractères avec une phrase pour chaque lieu de vente dans la base. """
    ldvs = getLieuxDeVente()
    LDVCh = ""
    for ldv in ldvs:
        if ldv[1] == 'particulier':
            LDVCh += f"Le lieu de vente est un particulier qui habite au {ldv[2]} à {ldv[4]} {ldv[3]}.\n"
        else:
            LDVCh += f"Le lieu de vente est un professionnel du magasin {ldv[1]} situé au {ldv[2]} à {ldv[4]} {ldv[3]}.\n"
    return LDVCh

def lieuID() -> str:
    """ Génère une chaîne de caractères avec une phrase pour chaque lieu de vente dans la base. """
    ldvs = getLieuxDeVente()
    LDVCh = ""
    for ldv in ldvs:
        LDVCh += f"{ldv[0]} : {ldv[1]} au {ldv[2]} {ldv[4]} {ldv[3]}\n"
    return LDVCh

def getVente() -> list :
    """ getEtudiants() -> liste de tuples "Etudiant"
    Rend le contenu de la base sous forme d'une liste de tuples.
    Attention, la date sera convertie en chaîne format ISO !!! """
    req = mesRequetes["getAllVente"]
    ventes = []
    for t in execute(req) :
        ventes.append(t)
    return ventes

def venteStr() -> str:
    """ Génère une chaîne de caractères avec une phrase pour chaque vente de moto dans la base. """
    ventes = getVente()
    venteCh = ""
    for vente in ventes:
        if vente[9] == "particulier":
            venteCh += f"Vente d'une {vente[6]} {vente[4]} {vente[5]} de {vente[7]} avec {vente[2]} km au prix de {vente[1]}€ chez un {vente[10]} au {vente[11]} à {vente[12]} {vente[13]}.\n"
        else:  
            venteCh += f"Vente d'une {vente[6]} {vente[4]} {vente[5]} de {vente[7]} avec {vente[2]} km au prix de {vente[1]}€ à {vente[10]} au {vente[11]} à {vente[12]} {vente[13]}.\n"
    return venteCh

def venteID():
    ventes = getVente()
    venteCh = ""
    for vente in ventes:
        if vente[9] == "particulier":
            venteCh += f"{vente[0]} : Vente d'une {vente[6]} {vente[4]} {vente[5]} de {vente[7]} avec {vente[2]} km au prix de {vente[1]}€ chez un {vente[10]} au {vente[11]} à {vente[12]} {vente[13]}.\n"
        else:  
            venteCh += f"{vente[0]} : Vente d'une {vente[6]} {vente[4]} {vente[5]} de {vente[7]} avec {vente[2]} km au prix de {vente[1]}€ à {vente[10]} au {vente[11]} à {vente[12]} {vente[13]}.\n"
    return venteCh

def getPrixVente(idVente):
    # Obtenir la requête SQL pour récupérer le prix de vente
    req_sql = GetPrixVente(idVente)
    result = execute(req_sql)
    if result:
        # Si la requête est un SELECT, fetchall() retournera une liste de tuples, nous prenons donc le premier élément du premier tuple
        return result[0][0]
    else:
        return None  
def getKmVente(idVente):
    req_sql = GetKmVente(idVente)
    result = execute(req_sql)
    if result:
        # Si la requête est un SELECT, fetchall() retournera une liste de tuples, nous prenons donc le premier élément du premier tuple
        return result[0][0]
    else:
        return None  
