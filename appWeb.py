import cherrypy
import os
from BD_Appli_moto_utils import insertUsers, initBase, Check_login, Check_user,getKmVente, getPrixVente,UpdateKilometres, UpdatePrix, getByMarque, getMotoAnnee, getMoto, getMarque, getLieuxDeVente, getVente, deleteVentesByID, deleteLieuxByID, deleteMarqueByID, deleteMotoByID, insertMarqueCSV, insertLieuxDeVentesCSV, insertMotoCSV, insertVentesCSV, insertVentes, insertMarque, insertLieuxDeVentes, insertMoto

    
def check_login(username:str, password:str):
    res = Check_login(username, password)
    if len(res) == 1:
        return res[0]
    else:
        return False

def check_user(username:str):
    res = Check_user(username)
    if len(res) == 1:
        return res[0]
    else:
        return False

class AppMoto:

    def est_authentifie(self):
        return cherrypy.session.get('authentifie', False)

    def est_admin(self):
        username = cherrypy.session.get('username')
        password = cherrypy.session.get('password')
        if username == "admin" and password == "admin":
            return True
        else:
            return False    

    @cherrypy.expose    
    def index(self):
        if self.est_admin():
            # Si l'utilisateur est un administrateur, retourne la page avec la page d'insertion
            return open('templates/index_admin.html', encoding="utf8").read()
        elif self.est_authentifie():
            return open('templates/index_authentifie.html', encoding="utf8").read()
        else:
            return open('templates/index.html', encoding="utf8").read()  

    @cherrypy.expose    
    def affichages(self):
        motos = getMoto()
        marques = getMarque()
        lieux_de_vente = getLieuxDeVente()
        
        # Générer le tableau HTML pour les motos
        table_html_motos = "<table><thead><tr><th>ID</th><th>Cylindrée en cm³</th><th>Modèle</th><th>Marque</th><th>Année</th><th>Puissance en chevaux</th><th>Immatriculation</th><th>Prix neuf</th></tr></thead><tbody>"
        for moto in motos:
            table_html_motos += f"<tr><td>{moto[0]}</td><td>{moto[1]}</td><td>{moto[2]}</td><td>{moto[3]}</td><td>{moto[4]}</td><td>{moto[5]}</td><td>{moto[6]}</td><td>{moto[7]}</td></tr>"
        table_html_motos += "</tbody></table>"

        # Générer le tableau HTML pour les marques
        table_html_marques = "<table><thead><tr><th>ID</th><th>Nom de la marque</th><th>Nationalité</th></tr></thead><tbody>"
        for marque in marques:
            table_html_marques += f"<tr><td>{marque[0]}</td><td>{marque[1]}</td><td>{marque[2]}</td></tr>"
        table_html_marques += "</tbody></table>"

        # Générer le tableau HTML pour les lieux de vente
        table_html_lieux_de_vente = "<table><thead><tr><th>ID</th><th>Nom du lieu de vente</th><th>Adresse</th><th>Code Postal</th><th>Ville</th></tr></thead><tbody>"
        for lieu_de_vente in lieux_de_vente:
            table_html_lieux_de_vente += f"<tr><td>{lieu_de_vente[0]}</td><td>{lieu_de_vente[1]}</td><td>{lieu_de_vente[2]}</td><td>{lieu_de_vente[3]}</td><td>{lieu_de_vente[4]}</td></tr>"
        table_html_lieux_de_vente += "</tbody></table>"

        with open('templates/affichages.html', encoding="utf8") as file:
            page_content = file.read()

        years_dropdown = self.search_annee_dropdown()
        marques_dropdown = self.search_marques_dropdown()
        # Remplacer les marqueurs dans le fichier HTML par les tableaux générés
        page_content = page_content.replace("<!--table_motos-->", table_html_motos)
        page_content = page_content.replace("<!--table_marques-->", table_html_marques)
        page_content = page_content.replace("<!--table_lieux_de_vente-->", table_html_lieux_de_vente)
        page_content = page_content.replace("<!--dropdown_years-->", years_dropdown)
        page_content = page_content.replace("<!--dropdown_marques-->", marques_dropdown)

        return page_content
    
    @cherrypy.expose
    def searchByYear(self, year):
        motos = getMotoAnnee(year)
        # Convertir les données en texte brut
        result = "\n".join([f"{moto['modele']}, {moto['annee']}, {moto['marque']}, {moto['cylindree']}, {moto['puissance']}, {moto['immatriculation']}, {moto['prix_neuf']}" for moto in motos])
        return result

    @cherrypy.expose
    def searchByMarque(self, marque):
        motos = getByMarque(marque)
        # Convertir les données en texte brut
        result = "\n".join([f"{moto['modele']}, {moto['annee']}, {moto['marque']}, {moto['cylindree']}, {moto['puissance']}, {moto['immatriculation']}, {moto['prix_neuf']}" for moto in motos])
        return result
        
    @cherrypy.expose    
    def affichages_authentifie(self):
        motos = getMoto()
        marques = getMarque()
        lieux_de_vente = getLieuxDeVente()
        ventes = getVente()

        # Générer le tableau HTML pour les motos
        table_html_motos = "<table><thead><tr><th>ID</th><th>Cylindrée en cm³</th><th>Modèle</th><th>Marque</th><th>Année</th><th>Puissance en chevaux</th><th>Immatriculation</th><th>Prix neuf</th></tr></thead><tbody>"
        for moto in motos:
            table_html_motos += f"<tr><td>{moto[0]}</td><td>{moto[1]}</td><td>{moto[2]}</td><td>{moto[3]}</td><td>{moto[4]}</td><td>{moto[5]}</td><td>{moto[6]}</td><td>{moto[7]}</td></tr>"
        table_html_motos += "</tbody></table>"

        # Générer le tableau HTML pour les marques
        table_html_marques = "<table><thead><tr><th>ID</th><th>Nom de la marque</th><th>Nationalité</th></tr></thead><tbody>"
        for marque in marques:
            table_html_marques += f"<tr><td>{marque[0]}</td><td>{marque[1]}</td><td>{marque[2]}</td></tr>"
        table_html_marques += "</tbody></table>"

        # Générer le tableau HTML pour les lieux de vente
        table_html_lieux_de_vente = "<table><thead><tr><th>ID</th><th>Nom du lieu de vente</th><th>Adresse</th><th>Code Postal</th><th>Ville</th></tr></thead><tbody>"
        for lieu_de_vente in lieux_de_vente:
            table_html_lieux_de_vente += f"<tr><td>{lieu_de_vente[0]}</td><td>{lieu_de_vente[1]}</td><td>{lieu_de_vente[2]}</td><td>{lieu_de_vente[3]}</td><td>{lieu_de_vente[4]}</td></tr>"
        table_html_lieux_de_vente += "</tbody></table>"

        table_html_ventes = "<table><thead><tr><th>ID Vente</th><th>Prix d'occasion</th><th>Kilomètres</th><th>ID Moto</th><th>Marque</th><th>Modèle</th><th>Cylindrée</th><th>Année</th><th>Immatriculation</th><th>ID Lieux de Vente</th><th>Nom du Magasin</th><th>Adresse</th><th>Code Postal</th><th>Ville</th><th>Modifier</th></tr></thead><tbody>"
        for vente in ventes:
            table_html_ventes += f'<tr><td>{vente[0]}</td><td>{vente[1]}</td><td>{vente[2]}</td><td>{vente[3]}</td><td>{vente[4]}</td><td>{vente[5]}</td><td>{vente[6]}</td><td>{vente[7]}</td><td>{vente[8]}</td><td>{vente[9]}</td><td>{vente[10]}</td><td>{vente[11]}</td><td>{vente[12]}</td><td>{vente[13]}</td>'
            table_html_ventes += f'<td><form method="post" action="/modifier_prix"><input type="hidden" name="idVente" value="{vente[0]}"/>'
            table_html_ventes += f'<input type="number" step="0.01" min="0" name="nouveau_prix" placeholder="Nouveau Prix"/>'
            table_html_ventes += f'<input type="submit" value="Modifier"/></form></td></tr>'
        table_html_ventes += "</tbody></table>"




        with open('templates/affichages_authentifie.html', encoding="utf8") as file:
            page_content = file.read()

        years_dropdown = self.search_annee_dropdown()
        marques_dropdown = self.search_marques_dropdown()
        # Remplacer les marqueurs dans le fichier HTML par les tableaux générés
        page_content = page_content.replace("<!--table_motos-->", table_html_motos)
        page_content = page_content.replace("<!--table_marques-->", table_html_marques)
        page_content = page_content.replace("<!--table_lieux_de_vente-->", table_html_lieux_de_vente)
        page_content = page_content.replace("<!--table_ventes-->", table_html_ventes)
        page_content = page_content.replace("<!--dropdown_years-->", years_dropdown)
        page_content = page_content.replace("<!--dropdown_marques-->", marques_dropdown)


        return page_content
    
    @cherrypy.expose    
    def affichages_admin(self):
        motos = getMoto()
        marques = getMarque()
        lieux_de_vente = getLieuxDeVente()
        ventes = getVente()

        table_html_motos = "<table><thead><tr><th>ID</th><th>Cylindrée en cm³</th><th>Modèle</th><th>Marque</th><th>Année</th><th>Puissance en chevaux</th><th>Immatriculation</th><th>Prix neuf</th><th>Supprimer</th></tr></thead><tbody>"
        for moto in motos:
            table_html_motos += f"<tr><td>{moto[0]}</td><td>{moto[1]}</td><td>{moto[2]}</td><td>{moto[3]}</td><td>{moto[4]}</td><td>{moto[5]}</td><td>{moto[6]}</td><td>{moto[7]}</td>"
            table_html_motos += f'<td><form method="post" action="/delete_motos"><input type="hidden" name="idMoto" value="{moto[0]}"/><input type="submit" value="Supprimer"/></form></td></tr>'
        table_html_motos += "</tbody></table>"

        table_html_marques = "<table><thead><tr><th>ID</th><th>Nom de la marque</th><th>Nationalité</th><th>Supprimer</th></tr></thead><tbody>"
        for marque in marques:
            table_html_marques += f"<tr><td>{marque[0]}</td><td>{marque[1]}</td><td>{marque[2]}</td>"
            table_html_marques += f'<td><form method="post" action="/delete_marques"><input type="hidden" name="idMarque" value="{marque[0]}"/><input type="submit" value="Supprimer"/></form></td></tr>'
        table_html_marques += "</tbody></table>"

        table_html_lieux_de_vente = "<table><thead><tr><th>ID</th><th>Nom du lieu de vente</th><th>Adresse</th><th>Code Postal</th><th>Ville</th><th>Supprimer</th></tr></thead><tbody>"
        for lieu_de_vente in lieux_de_vente:
            table_html_lieux_de_vente += f"<tr><td>{lieu_de_vente[0]}</td><td>{lieu_de_vente[1]}</td><td>{lieu_de_vente[2]}</td><td>{lieu_de_vente[3]}</td><td>{lieu_de_vente[4]}</td>"
            table_html_lieux_de_vente += f'<td><form method="post" action="/delete_lieux_de_vente"><input type="hidden" name="idLieu" value="{lieu_de_vente[0]}"/><input type="submit" value="Supprimer"/></form></td></tr>'
        table_html_lieux_de_vente += "</tbody></table>"

        table_html_ventes = "<table><thead><tr><th>ID Vente</th><th>Prix d'occasion</th><th>Kilomètres</th><th>ID Moto</th><th>Marque</th><th>Modèle</th><th>Cylindrée</th><th>Année</th><th>Immatriculation</th><th>ID Lieux de Vente</th><th>Nom du Magasin</th><th>Adresse</th><th>Code Postal</th><th>Ville</th><th>Modifier</th><th>Supprimer</th></tr></thead><tbody>"
        for vente in ventes:
            table_html_ventes += f'<tr><td>{vente[0]}</td><td>{vente[1]}</td><td>{vente[2]}</td><td>{vente[3]}</td><td>{vente[4]}</td><td>{vente[5]}</td><td>{vente[6]}</td><td>{vente[7]}</td><td>{vente[8]}</td><td>{vente[9]}</td><td>{vente[10]}</td><td>{vente[11]}</td><td>{vente[12]}</td><td>{vente[13]}</td>'
            table_html_ventes += f'<td><form method="post" action="/modifier_km"><input type="hidden" name="idVente" value="{vente[0]}"/><input type="number" step="0.01" min="0" name="nouveau_km" placeholder="Nouveau kilomètrages"/><input type="submit" value="Modifier"/></form></td>'
            table_html_ventes += f'<td><form method="post" action="/delete_vente"><input type="hidden" name="idVente" value="{vente[0]}"/><input type="submit" value="Supprimer"/></form></td></tr>'
        table_html_ventes += "</tbody></table>"


        with open('templates/affichages_admin.html', encoding="utf8") as file:
            page_content = file.read()
 
        years_dropdown = self.search_annee_dropdown()
        marques_dropdown = self.search_marques_dropdown()
        page_content = page_content.replace("<!--table_motos-->", table_html_motos)
        page_content = page_content.replace("<!--table_marques-->", table_html_marques)
        page_content = page_content.replace("<!--table_lieux_de_vente-->", table_html_lieux_de_vente)
        page_content = page_content.replace("<!--table_ventes-->", table_html_ventes)
        page_content = page_content.replace("<!--dropdown_years-->", years_dropdown)
        page_content = page_content.replace("<!--dropdown_marques-->", marques_dropdown)

        return page_content
    
    def search_annee_dropdown(self):
        motos = getMoto()
        annees = []
        options = ""
        for moto in motos:
            if moto[4] not in annees:
                annees.append(moto[4])
                options += f"<option value='{moto[4]}'>{moto[4]}</option>"
        return options
    
    def search_marques_dropdown(self):
        marques = getMarque()
        options = ""
        for marque in marques:
            options += f"<option value='{marque[1]}'>{marque[1]}</option>"
        return options
   
    def get_marques_dropdown(self):
        marques = getMarque() 
        options = ""
        for marque in marques:
            options += f"<option value='{marque[0]}'>{marque[1]}</option>"
        return options
    
    def get_lieu_dropdown(self):
        lieux = getLieuxDeVente()  
        options = ""
        for lieu in lieux:
            options += f"<option value='{lieu[0]}'>{lieu[0]} : {lieu[1]} au {lieu[2]} {lieu[4]} {lieu[3]}</option>"
        return options
    
    def get_moto_dropdown(self):
        motos = getMoto()  
        options = ""
        for moto in motos:
            options += f"<option value='{moto[0]}'>{moto[0]} : {moto[3]} {moto[1]} {moto[2]} immatriculé {moto[6]}</option>"
        return options
    
    @cherrypy.expose
    def insertion(self):
        marques_dropdown = self.get_marques_dropdown()
        lieux_dropdown = self.get_lieu_dropdown()
        motos_dropdown = self.get_moto_dropdown()
        insertion_form = open('templates/insertion.html', encoding="utf8").read()
        insertion_form = insertion_form.replace("<!--marques_dropdown-->", marques_dropdown)
        insertion_form = insertion_form.replace("<!--lieux_dropdown-->", lieux_dropdown)
        insertion_form = insertion_form.replace("<!--motos_dropdown-->", motos_dropdown)

        return insertion_form
    
    @cherrypy.expose
    def insert_moto(self, modele, annee, cylindree, puissance, immatriculation, prix_neuf, idMarque):
        insertMoto(modele, annee, cylindree, puissance, immatriculation, prix_neuf, idMarque)
        return """
            <script>
            alert('Insertion de la moto avec succès');
            setTimeout(function() {
                window.location.href = '/insertion';
            }, 1000); // Rediriger après 1 seconde (1000 millisecondes)
            </script>
            """

    @cherrypy.expose
    def insert_ventes(self, prix_occasion, kilometres, idMoto, idLieu):
        insertVentes(prix_occasion, kilometres,idMoto, idLieu)
        return """
            <script>
            alert('Insertion de la vente avec succès');
            setTimeout(function() {
                window.location.href = '/insertion';
            }, 1000); // Rediriger après 1 seconde (1000 millisecondes)
            </script>
            """

    @cherrypy.expose
    def insert_lieux_de_ventes(self, adresse, codePostal, ville, nomMagasin):
        if nomMagasin.strip() == "":
            nomMagasin = "particulier"
        insertLieuxDeVentes(adresse, codePostal, ville, nomMagasin)
        return """
            <script>
            alert('Insertion du lieu de vente avec succès');
            setTimeout(function() {
                window.location.href = '/insertion';
            }, 1000); // Rediriger après 1 seconde (1000 millisecondes)
            </script>
            """


    @cherrypy.expose
    def insert_marque(self, nom, nationnalite):
        insertMarque(nom, nationnalite)
        return """
            <script>
            alert('Insertion de la marque avec succès');
            setTimeout(function() {
                window.location.href = '/insertion';
            }, 1000); // Rediriger après 1 seconde (1000 millisecondes)
            </script>
            """


    @cherrypy.expose
    @cherrypy.tools.allow(methods=['POST'])
    def upload_csv(self, file, category):
        # Enregistrer le fichier temporairement
        upload_path = os.path.join(os.getcwd(), 'uploads')
        if not os.path.exists(upload_path):
            os.makedirs(upload_path)
        upload_file_path = os.path.join(upload_path, file.filename)
        with open(upload_file_path, 'wb') as out:
            while True:
                data = file.file.read(8192)
                if not data:
                    break
                out.write(data)

        # Appeler la fonction d'insertion correspondante
        error_message = None
        try:
            if category == 'marques':
                insertMarqueCSV(upload_file_path)
            elif category == 'lieux':
                insertLieuxDeVentesCSV(upload_file_path)
            elif category == 'motos':
                insertMotoCSV(upload_file_path)
            elif category == 'ventes':
                insertVentesCSV(upload_file_path)
            else:
                raise cherrypy.HTTPError(400, "Catégorie invalide")
        except Exception as e:
            cherrypy.response.status = 400
            cherrypy.response.headers['Content-Type'] = 'text/plain'
            error_message = str(e)
        finally:
            os.remove(upload_file_path)

        if error_message:
            cherrypy.response.headers['Content-Type'] = 'text/plain'
            cherrypy.response.status = 400
            raise cherrypy.HTTPRedirect("/insertion")
        else:
            return """
            <script>
                alert("Insertion réussie");
                window.location.href = '/insertion';
            </script>
            """

    
    @cherrypy.expose
    @cherrypy.tools.allow(methods=['POST'])
    def delete_motos(self, idMoto):
        deleteMotoByID(idMoto)
        return """
            <script>
            alert('Moto supprimée avec succès');
            setTimeout(function() {
                window.location.href = '/affichages_admin';
            }, 1000); // Rediriger après 1 seconde (1000 millisecondes)
            </script>
            """
    
    @cherrypy.expose
    @cherrypy.tools.allow(methods=['POST'])
    def delete_marques(self, idMarque):
        deleteMarqueByID(idMarque)
        return """
            <script>
            alert('Marque supprimée avec succès');
            setTimeout(function() {
                window.location.href = '/affichages_admin';
            }, 1000); // Rediriger après 1 seconde (1000 millisecondes)
            </script>
            """
    
    @cherrypy.expose
    @cherrypy.tools.allow(methods=['POST'])
    def delete_lieux_de_vente(self, idLieu):
        deleteLieuxByID(idLieu)
        return """
            <script>
            alert('Lieux de vente supprimé avec succès');
            setTimeout(function() {
                window.location.href = '/affichages_admin';
            }, 1000); // Rediriger après 1 seconde (1000 millisecondes)
            </script>
            """
    
    @cherrypy.expose
    @cherrypy.tools.allow(methods=['POST'])
    def delete_vente(self, idVente):
        deleteVentesByID(idVente)
        return """
            <script>
            alert('Ventes supprimée avec succès');
            setTimeout(function() {
                window.location.href = '/affichages_admin';
            }, 1000); // Rediriger après 1 seconde (1000 millisecondes)
            </script>
            """
    
    @cherrypy.expose
    def modifier_prix(self, idVente, nouveau_prix):
        # Récupérer le prix actuel de la vente en utilisant la fonction getPrixVente
        prix_actuel = float(getPrixVente(idVente))
        
        # Vérifier si le nouveau prix est valide et supérieur au prix actuel
        if (nouveau_prix.isdigit() or (nouveau_prix.count('.') == 1 and nouveau_prix.replace('.', '').isdigit())) and float(nouveau_prix) > prix_actuel:
            # Mettre à jour le prix
            UpdatePrix(nouveau_prix, idVente)
            # JavaScript pour afficher un message de confirmation et rediriger
            return """
            <script>
            alert('Prix modifié avec succès');
            setTimeout(function() {
                window.location.href = '/affichages_authentifie';
            }, 1000); // Rediriger après 1 seconde (1000 millisecondes)
            </script>
            """
        else:
            # JavaScript pour afficher un message d'erreur et rediriger
            return """
            <script>
            alert('Le nouveau prix est invalide, inférieur ou égal au prix actuel');
            setTimeout(function() {
                window.location.href = '/affichages_authentifie';
            }, 1000); // Rediriger après 1 seconde (1000 millisecondes)
            </script>
            """
        
    @cherrypy.expose
    def modifier_km(self, idVente, nouveau_km):
        # Récupérer le prix actuel de la vente en utilisant la fonction getPrixVente
        prix_actuel = float(getKmVente(idVente))
        
        # Vérifier si le nouveau prix est valide et supérieur au prix actuel
        if (nouveau_km.isdigit() or (nouveau_km.count('.') == 1 and nouveau_km.replace('.', '').isdigit())) and float(nouveau_km) > prix_actuel:
            # Mettre à jour le prix
            UpdateKilometres(nouveau_km, idVente)
            # JavaScript pour afficher un message de confirmation et rediriger
            return """
            <script>
            alert('Km modifié avec succès');
            setTimeout(function() {
                window.location.href = '/affichages_admin';
            }, 1000); // Rediriger après 1 seconde (1000 millisecondes)
            </script>
            """
        else:
            # JavaScript pour afficher un message d'erreur et rediriger
            return """
            <script>
            alert('Le nouveau km est invalide, inférieur ou égal au prix actuel');
            setTimeout(function() {
                window.location.href = '/affichages_admin';
            }, 1000); // Rediriger après 1 seconde (1000 millisecondes)
            </script>
            """
            

    @cherrypy.expose()
    def login(self, username: str, password: str):
        login_res = check_login(username, password)
        if not login_res:
            # HTML avec JavaScript pour afficher une alerte et rediriger l'utilisateur
            return '''
                <html>
                    <head>
                        <script type="text/javascript">
                            alert("Login ou mot de passe incorrect");
                            window.location.href = "/#connexion";
                        </script>
                    </head>
                    <body>
                    </body>
                </html>
            '''
        else:
            cherrypy.session['authentifie'] = True
            cherrypy.session['username'] = username
            cherrypy.session['password'] = password
            raise cherrypy.HTTPRedirect("/")
                      
    @cherrypy.expose
    def signup(self, newUsername, newPassword):
        login_res = check_user(newUsername)        
        if not login_res:
            insertUsers(newUsername, newPassword)
            # HTML avec JavaScript pour afficher une alerte et rediriger l'utilisateur
            return '''
                <html>
                    <head>
                        <script type="text/javascript">
                            alert("Inscription de {} réussie !");
                            window.location.href = "/#connexion";
                        </script>
                    </head>
                    <body>
                    </body>
                </html>
            '''.format(newUsername)
        else:
            # Construire le contenu HTML avec le message d'inscription réussie
            return'''
                <html>
                    <head>
                        <script type="text/javascript">
                            alert("Nom d'utilisateur déjà pris");
                            window.location.href = "/#inscription";
                        </script>
                    </head>
                    <body>
                    </body>
                </html>
            '''
            
    @cherrypy.expose
    def logout(self):
        cherrypy.session['authentifie'] = False
        cherrypy.session['username'] = None
        cherrypy.session['password'] = None
        raise cherrypy.HTTPRedirect("/")
    
if __name__ == '__main__':
    rootPath = os.path.abspath(os.getcwd())
    print(f"la racine du site est :\n\t{rootPath}\n\tcontient : {os.listdir()}")
    initBase()
    cherrypy.quickstart(AppMoto(), '/', 'config.txt')