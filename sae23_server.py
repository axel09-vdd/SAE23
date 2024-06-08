from appWeb import * 
import cherrypy
import os


if __name__ == '__main__':
    initBase()
    rootPath = os.path.abspath(os.getcwd())
    print(f"La racine du site est :\n\t{rootPath}\n\tContient : {os.listdir()}")

    # On essaie de se connecter dès le lancement du serveur
    dbConnect()  # Assurez-vous que dbConnect() est défini dans randomquotes pour gérer la connexion à la base de données

    conf = {
        'global': {
            'server.socket_host': '127.0.0.1',
            'server.socket_port': 8080,
        },
        '/': {
            'tools.staticdir.root': os.path.abspath(os.getcwd()),
            'tools.sessions.on': True,
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './res',
        },
        '/static/css': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './res/css',
        },
        '/static/images': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './res/images',
        },
        '/static/js': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './res/js',
        },
        '/favicon.ico': {
            'tools.staticfile.on': True,
            'tools.staticfile.filename': os.path.join(os.path.abspath(os.getcwd()), 'favicon.ico'),
        }
    }

    cherrypy.quickstart(AppMoto(), '/', conf)
