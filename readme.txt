Application SAE 23 thème moto

- Pour lancer l'application il faut d'abord compléter le fichier de config puis lancer le programme appWeb.py

- L'appli permet à toutes les personnes de voir les motos de la base, les lieux de vente et les marques. Si l'utilisateur se connecte en créant son compte il peut accéder à vente et donc modifier le prix d'occasion pour espérer avoir l'enchère. Pour finir l'administrateur peut tout faire sauf modifier le prix des enchères, mais il peut modifier leurs kilomètres, insérer des élements et des csv avec le bon format (exemple pour chaque table) il faut commencer par insérer des marques ensuite des lieux de ventes, des motos puis des ventes et pour finir il a la possibilité de supprimer toutes les choses de la base.

- La base à été modifier en changeant la puissance en float pour permettre de mettre (47,5 chevaux par exemple) et la table user à été rajouter pour gérer la partie login.

- Le fichier appWeb.py est mon application Web cherrypy, BD_Appli_moto_utils.py est le fichier qui permet d'executer toutes les requêtes et le fichier requete.py contient toutes les requetes de la base.

- Les quatres csv avec le bon format pour être insérer dans la base.

- Le fichier config.txt pour gérer les paramètres.

- moto.sql qui est le dump de ma base.

- Le favicon.ico pour mettre une petite image sympa :)

- Le rep templates qui contient tous les fichiers html.

- Le rep res avec le rep css pour mon fichier css, le rep js pour mon fichier javascript et le rep images pour mes images.