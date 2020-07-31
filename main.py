
from os import path# afin de vérifier si un fichier existe dans le répertoire
import logging.config #afin de faire du log
import logging# idem qu'au dessus
#from flask import Flask
from butter_cms import ButterCMS
from flask import Flask

client = ButterCMS('your_api_token')
from model import session as db  # python class who flush changes to database
#from flask_debugtoolbar import DebugToolbarExtension # afin de faire du debug dans flask
# for use the ini/config file :
log_file_path = path.join(path.dirname(path.abspath(__file__)), 'log.config') # associe le path.abspath(__file__) faisant référence au répertoire courant, au 'log.config' faisant référence au fichier du même nom grâce au path.join
logging.config.fileConfig(log_file_path) # configure des logs à partir du fichier passé en paramètre
log = logging.getLogger(__name__)  # return a logger which current class is the root logger


app = Flask(__name__)  # for Flask to knows where to look for templates and files # ici on instancie et crée un serveur flask
# app.debug = True  # to activate debugtoolbar in navigators #lié au debugtoolbar
# secret key is needed to keep the client-side sessions secure :
#app.config['SECRET_KEY'] = 'Tandis que les crachats rouges de la mitraille' #lié au debugtoolbar
#toolbar = DebugToolbarExtension(app) #lié au debugtoolbar

'''
    The @app.teardown_appcontext decorator will cause the supplied callback, cleanup, 
    to be executed when the current application context is torn down. This happens 
    after each request. That way we make sure to release the resources used by a 
    session after each request :
'''


@app.teardown_appcontext #ici on purge la cache de flask au démarrage du serveur
def cleanup(resp_or_exc):
    db.remove() # ici on vide la base de données


if __name__ == '__main__':  # check if main.py is called

    import controller
    #  for url routes registration with Flask :
    app.add_url_rule('/', 'welcome_home', view_func=controller.welcome_home)
    app.add_url_rule('/login_admin', 'login_admin', view_func=controller.login_admin, methods=['POST', 'GET'])
    app.add_url_rule('/login', 'login', view_func=controller.login, methods=['POST', 'GET'])
    app.add_url_rule('/home_admin', 'home_admin', view_func=controller.home_admin)
    app.add_url_rule('/client/add', 'add_client', view_func=controller.add_client, methods=['POST', 'GET'])
    app.add_url_rule('/client/add_admin', 'add_client_admin', view_func=controller.add_client_admin, methods=['POST', 'GET'])
    app.add_url_rule('/client/del', 'delete_client', view_func=controller.del_client, methods=['POST', 'GET'])
    app.add_url_rule('/client/del_account/<string:token>', 'delete_account', view_func=controller.del_account, methods=['POST', 'GET'])
    app.add_url_rule('/client/del_account_client/<string:token>', 'delete_account_client', view_func=controller.del_account_client,methods=['POST', 'GET'])
    app.add_url_rule('/client/file/<string:token>','client_file',view_func=controller.client_file, methods=['POST', 'GET'])
    app.add_url_rule('/client/file_client/<string:token>', 'client_file_client', view_func=controller.client_file_client,methods=['POST', 'GET'])
    app.add_url_rule('/client/account/<string:token>/<int:type>','add_account', view_func=controller.add_account) # voir commentaires dans la fonction add_account
    app.add_url_rule('/client/account_admin/<string:token>/<int:type>', 'add_account_admin',view_func=controller.add_account_admin)  # voir commentaires dans la fonction add_account
    try:
        log.info('Application starting')
        app.debug = True
        app.run(host='127.0.0.1', port=8080)
        log.info('Application end without exception')
    except Exception as ex:
        log.exception('Application end because of uncatching exception')
        pass

    print(client.posts.all({'page_size': 10, 'page': 1}))
