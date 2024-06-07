mesRequetes = {
    "drop" : "DROP DATABASE IF EXISTS moto",
    "createBase" : "CREATE DATABASE IF NOT EXISTS moto DEFAULT CHARACTER SET utf8",
    "use" : "USE moto",
    "createMoto" : "CREATE TABLE IF NOT EXISTS `moto` (`idMoto` int NOT NULL AUTO_INCREMENT,\
        `modèle` varchar(20) NOT NULL,\
        `année` year NOT NULL,\
        `cylindrée` int NOT NULL,\
        `puissance` float NOT NULL,\
        `immatriculation` varchar(9) NOT NULL,\
        `prix_neuf` float NOT NULL,\
        `marque` int NOT NULL,\
        PRIMARY KEY (`idMoto`),\
        KEY `marque` (`marque`)\
        ) ENGINE=InnoDB AUTO_INCREMENT=0;",
    "createLieuxDeVentes" : "CREATE TABLE IF NOT EXISTS `lieux_de_vente` (`idLieux` int NOT NULL AUTO_INCREMENT,\
        nomMagasin VARCHAR(50) CHARACTER SET utf8 NOT NULL DEFAULT 'particulier',\
        `adresse` varchar(70) NOT NULL,\
        `codePostal` int NOT NULL,\
        `ville` varchar(50) NOT NULL,\
        PRIMARY KEY (`idLieux`)\
        ) ENGINE=InnoDB AUTO_INCREMENT=0;",
    "createMarque" : "CREATE TABLE IF NOT EXISTS `marque` (`idMarque` int NOT NULL AUTO_INCREMENT,\
        `nom` varchar(20) NOT NULL,\
        `nationnalité` varchar(50) NOT NULL,\
        PRIMARY KEY (`idMarque`)\
        ) ENGINE=InnoDB AUTO_INCREMENT=0;",
    "createVentes" : "CREATE TABLE IF NOT EXISTS `ventes` (`idVente` int NOT NULL AUTO_INCREMENT,\
        `prix_occasion` float NOT NULL,\
        `kilomètres` float NOT NULL,\
        `moto` int NOT NULL,\
        `lieuxVente` int NOT NULL,\
        PRIMARY KEY (`idVente`),\
        KEY `ventes` (`lieuxVente`),\
        KEY `moto` (`moto`)\
        ) ENGINE=InnoDB AUTO_INCREMENT=0;",
    "createUsers" : "CREATE TABLE IF NOT EXISTS `users` (`idUsers` int NOT NULL AUTO_INCREMENT,\
        `login` varchar(20) NOT NULL,\
        `mdp` varchar(50) NOT NULL,\
        PRIMARY KEY (`idUsers`)\
        ) ENGINE=InnoDB AUTO_INCREMENT=0;",
    "keyMoto" : "ALTER TABLE `moto`\
        ADD CONSTRAINT `marque` FOREIGN KEY (`marque`) REFERENCES `marque` (`idMarque`) ON DELETE CASCADE ON UPDATE CASCADE;",
    "keyVentes":"ALTER TABLE `ventes`\
        ADD CONSTRAINT `moto` FOREIGN KEY (`moto`) REFERENCES `moto` (`idMoto`) ON DELETE CASCADE ON UPDATE CASCADE,\
        ADD CONSTRAINT `ventes` FOREIGN KEY (`lieuxVente`) REFERENCES `lieux_de_vente` (`idLieux`) ON DELETE CASCADE ON UPDATE CASCADE;",
    "getAllMoto" : "select moto.idMoto,moto.cylindrée,moto.modèle,marque.nom,moto.année,moto.puissance,moto.immatriculation,moto.prix_neuf from moto join marque on marque.idMarque=moto.marque;",
    "getAllMarque" : "select * from marque",
    "getAllLdv" : "select * from lieux_de_vente",
    "getAllVente" : "select idVente,prix_occasion,kilomètres, moto.idMoto,marque.nom, moto.modèle, moto.cylindrée, moto.année, moto.immatriculation, lieux_de_vente.idLieux, lieux_de_vente.nomMagasin, lieux_de_vente.adresse, lieux_de_vente.codePostal, lieux_de_vente.ville from ventes join moto on ventes.moto=moto.idMoto join lieux_de_vente on ventes.lieuxVente=lieux_de_vente.idLieux JOIN marque on moto.marque=marque.idMarque;",
    "getIdMarque" : "select idMarque from marque where nom = '{}';",
    "getMarque" : "select moto.modèle, moto.année, moto.cylindrée, moto.puissance, moto.immatriculation, moto.prix_neuf, marque.nom from moto join marque on moto.marque=marque.idMarque where marque.nom='{}'",
    "getMotoAnnee" : "select moto.modèle, moto.année, moto.cylindrée, moto.puissance, moto.immatriculation, moto.prix_neuf, marque.nom from moto join marque on moto.marque=marque.idMarque where moto.année='{}';",
    "getIdLieux" : "select idLieux from lieux_de_vente where adresse = '{}';",
    "getPrixVente": "SELECT prix_occasion from ventes where idVente = {};",
    "getKmVente": "select kilomètres from ventes where idVente = {};",
    "getIdMoto" : "select idMoto from moto where immatriculation = '{}';",
    "check_login" : "SELECT idUsers, login FROM users WHERE login={} AND mdp={}",
    "check_user" : "SELECT idUsers, login FROM users WHERE login={}",
    "updateKilometres" : "update ventes SET kilomètres = {} WHERE ventes.idVente={};",
    "updatePrix" : "update ventes SET prix_occasion = {} WHERE ventes.idVente={};",
    "insertMoto" : "insert into moto (modèle,année,cylindrée,puissance,immatriculation,prix_neuf,marque) values ('{}','{}','{}','{}','{}','{}','{}');",
    "insertLieuxDeVentes" : "insert into lieux_de_vente(nomMagasin,adresse, codePostal, ville) values ('{}','{}','{}','{}')",
    "insertMarque" : "insert into marque(nom, nationnalité) values ('{}','{}')",
    "insertVentes" : "insert into ventes(prix_occasion,kilomètres, moto, lieuxVente) values ('{}','{}','{}','{}')",
    "insertAdmin" : "insert into users(login, mdp) values('admin','admin')",
    "insertUsers" : "insert into users(login, mdp) values('{}','{}')",
    "deleteMotoByID" : "delete from moto where idMoto = {};",
    "deleteMarqueByID" : "delete from marque where idMarque = {};",
    "deleteLieuxByID" : "delete from lieux_de_vente where idLieux = {};",
    "deleteVentesByID" : "delete from ventes where idVente = {};"
}



def updateKilometres(km, idMoto):
    s = mesRequetes["updateKilometres"].format(km, idMoto)
    return s

def updatePrix(prix, idMoto):
    s = mesRequetes["updatePrix"].format(prix, idMoto)
    return s

def InsertMoto(modèle,année,cylindrée,puissance,immatriculation,prix_neuf,marque):
    s = mesRequetes["insertMoto"].format(modèle,année,cylindrée,puissance,immatriculation,prix_neuf,marque)
    return s

def InsertLieuxDeVentes(nomMagasin,adresse, codePostal, ville):
    s = mesRequetes["insertLieuxDeVentes"].format(nomMagasin,adresse, codePostal, ville.capitalize())
    return s

def InsertMarque(nom, nationnalité):
    s = mesRequetes["insertMarque"].format(nom.upper(), nationnalité.capitalize())
    return s

def InsertVentes(prix_occasion,kilomètres, moto, lieuxVente):
    s = mesRequetes["insertVentes"].format(prix_occasion, kilomètres, moto, lieuxVente)
    return s

def InsertUsers(login,mdp):
    s = mesRequetes["insertUsers"].format(login, mdp)
    return s

def GetIdMarque(nom):
    s = mesRequetes["getIdMarque"].format(nom.upper())
    return s

def GetByMarque(nom):
    s = mesRequetes["getMarque"].format(nom)
    return s

def GetMotoAnnee(annee):
    s = mesRequetes["getMotoAnnee"].format(annee)
    return s

def GetIdLieuxDeVentes(adresse):
    s = mesRequetes["getIdLieux"].format(adresse)
    return s

def GetIdMoto(immatriculation):
    s = mesRequetes["getIdMoto"].format(immatriculation)
    return s

def GetPrixVente(idVente):
    s = mesRequetes["getPrixVente"].format(idVente)
    return s
def GetKmVente(idVente):
    s = mesRequetes["getKmVente"].format(idVente)
    return s   

def check_login(login, mdp):
    s = mesRequetes["check_login"].format('%s', '%s')
    return s, (login, mdp)

def check_user(login):
    s = mesRequetes["check_user"].format('%s', '%s')
    return s, (login)

def DeleteMotoByID(idMoto):
    s = mesRequetes["deleteMotoByID"].format(idMoto)
    return s

def DeleteMarqueByID(idMarque):
    s = mesRequetes["deleteMarqueByID"].format(idMarque)
    return s

def DeleteLieuxByID(idLieux):
    s = mesRequetes["deleteLieuxByID"].format(idLieux)
    return s

def DeleteVentesByID(idVente):
    s = mesRequetes["deleteVentesByID"].format(idVente)
    return s
