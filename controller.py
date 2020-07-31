
import logging
from model import Client, SavingAccount, DebitAccount, BankAccount, TotalAccounts #on importe les classes du model
from model import session as db # importe la variale session du fichier model renomme db
from flask import render_template, request, redirect, url_for # url_for récupère l'url lié à l'etiquette donner en paramètre
import hashlib
import random
import string

log = logging.getLogger(__name__)# on instancie le loggeur (programme qui va faire les logs)



def home_admin():
    log.info('Controler home admin starts')# on crée un message dans le log au niveau de gravité le plus bas c a d info
    clients = db.query(Client).order_by(Client.lastname) # soumet une requête à la base de données à l'aide de la méthode query à laquelle on passe en paramètre une classe faisant référence à une table de la base de données, order_by, méthode qui permet de trié suivant un champ de la table ici last_name(Client.last_name)
    return render_template("home.html", clients=clients)# la variable clients fait référence à la donnée que l'on va injecter dans la page html home.htlm au niveau de la variable clients dans la même page, on peut mettre autant de champs ou de mots clés (nom de variable qui ne sont pas soumis) que l'on veut séparés par une virgule

def welcome_home():
    log.info('Controler welcome home starts')
    return  render_template("welcome_home.html")

def generate_token():
    tmp = ""
    list = string.ascii_letters
    list_add_with_digit = list + string.digits
    for i in range(20):
        tmp += random.choice(list_add_with_digit)
    return tmp


def add_client():       #fonction d'ajout de client
    log.info('Controler add_clients starts')
    if request.method == 'POST':
        # TODO check that firstname and lastname are defined
        client_email =db.query(Client).filter_by(email=request.form['email']).first()
        if client_email is None:
            client = Client(             # ici in instancie un objet client (de la classe client)
                request.form['firstname'],
                request.form['lastname'],
                request.form['email'],
                generate_token(),
                request.form['password'])
            db.add(client)
            db.commit()
            return redirect(url_for('client_file_client', token=client.token))
        if request.form['email'] == client_email.email:
            return render_template('redirect_add_client.html')
    else:
        return render_template('add_client.html')

def add_client_admin():
    log.info('Controler add_clients_admin starts')
    if request.method == 'POST':
        # TODO check that firstname and lastname are defined
        client_email =db.query(Client).filter_by(email=request.form['email']).first()
        if client_email is None:
            client = Client(             # ici in instancie un objet client (de la classe client)
                request.form['firstname'],
                request.form['lastname'],
                request.form['email'],
                generate_token(),
                request.form['password'])
            #print(client.password)
            db.add(client)
            db.commit()
            return redirect(url_for('client_file', token=client.token))
        if request.form['email'] == client_email.email:
            return render_template('redirect_add_client.html')
    else:
        return render_template('add_client_admin.html')

def del_client():
    log.info('Controle del_clients starts')
    if request.method == 'POST':
        # si la méthode du formaulaire est post on interroge la table Client avec comme contrainte le prénom et le nom de l'utilisateur
        client_account= db.query(Client).filter_by(firstname=request.form['firstname']).filter_by(lastname=request.form['lastname'])#.filter_by(email=request.form['email'])
        #ensuite on récupère sous forme tuples la ligne du client
        client= db.execute(client_account).fetchone()
        #si le client n'existe pas on redirige l'utilisateur sur un page d'erreur
        if client is None:
            return render_template('redirectory_delete_client.html')


        else:
            #si il existe on récupère on id en interrogeant la table Client on récupère son id à l'indcice 0
            client_id = db.query(Client).get(client[0])
            #ensuite on interroge la table Bankaccount possédant tous les ocmptes bancaires du client à l'aide de  l'id du client,
            # ensuite on supprime le client de la table Bankaccount
            db.query(BankAccount).filter_by(client_id=client_id.client_id).delete()
            # enusite on supprime l'id du client existant dans la table Client, il n'y a plus de trace de lui
            db.delete(client_id)

            db.commit()
            return redirect(url_for('home_admin'))
    else:
        return render_template('delete_client.html')


def get_amount(): # pour récupérer le montant (la valeur que l'on rentre)
    try:
        amount = float(request.form['amount'])# on va tenter (try) de récupèrer la valeur du champ input ayant pour nom amount que l'on convertit en float
    except ValueError as v:                   # avec le except on récupère un objet de type ValueError(erreur de type valeur) que l'on nomme v (noter ici qu'il ne sera pas utlisé) et donc si on récupère la bonne exception on évite que le programme plante, à noter également que si l'on appel une fonction dans le bloc try et que celle-ci opère une exception qui n'est pas protège dans le coprs de lafonction dite et quelle corresponder au type d'execption du bloc except alors elle sera quand même levée par cette dernière
        raise ValueError('Please, enter only digits in amount.') #le raise lève une exception ici de type ValueError seulment si l'on rentre dans l'except et renvois un message, à noter que si l'on finit par le mot raise uniquement cela qu'on relève la même exception qu'auparavant
    if amount == 0:
        raise ValueError('Amount must not be zero (0).')
    elif amount < 0:
        raise ValueError('Amount must be positive.')
    else:
        return amount


"""def convert_to_client(row_proxy):
    tmp =[row_proxy[0], row_proxy[1], row_proxy[2], row_proxy[3], row_proxy[4]]
    result= db.query(Client).filter_by(client_id=row_proxy[0])
    result_id = db.execute(result).fetchone()
    print(result_id[0])
    client = db.query(BankAccount).filter_by(client_id=result_id[0])
    client_exe = db.execute(client).fetchone()
    print(client_exe)
    return client_exe

def get_client_by_token(token):
    req = db.query(Client).filter_by(token=token)
    result = db.execute(req).fetchone()
    client = convert_to_client(result)
    return client"""


def get_client_using_Token(token): #récupère un id à parir d'un token, sert à authentifier un client
    client_id = db.query(Client).filter_by(token=token)
    result= db.execute(client_id).fetchone()
    #print(result)
    result_id= result[0]
    return result_id
    #print(result_id)


def login():
    log.info('Controle login starts')
    if request.method == 'POST':
        client = db.query(Client).filter_by(email = request.form['email'], password=hashlib.sha256(bytes(request.form['password'],"utf_8")).hexdigest() ).first()
                 #and db.query(Client).filter_by(password=hashlib.sha256(bytes(request.form['password'],"utf_8")).hexdigest()).first()
                 #db.query(Client).filter_by(firstname= request.form['firstname'])  \
                 #and db.query(Client).filter_by(lastname = request.form['lastname'])\
        #print(client)
        if client is None:
            return render_template('redirectory_login.html')

        #print(client)
        return redirect(url_for('client_file_client', token=client.token))

    else:
        return render_template('login.html')

def login_admin():
    log.info('Controle login_admin starts')
    admin_password = hashlib.sha256(bytes("admin", "utf-8")).hexdigest()

    if request.method == 'POST':
        if hashlib.sha256(bytes(request.form['password_admin'], "utf-8")).hexdigest() == admin_password:
            #print(admin_password)
            #print(hashlib.sha256(bytes(request.form['password_admin'], "utf-8")).hexdigest())
            return redirect(url_for('home_admin'))
        else:
            return render_template('redirectory_login_admin.html')

    return render_template('login_admin.html')


def iterate_credit_account(token):
    sum = 0

    id_client = get_client_using_Token(token)
    accounts = db.query(BankAccount).filter_by(client_id=id_client).all()
    client = db.query(Client).get(id_client)
    # total_account = TotalAccounts(client,token)
    for account in accounts:
        #print(account)
        #print("\nsum credit {} ".format(sum))
        #print("balance credit {}\n".format(account.get_account_balance()))
        sum += account.get_account_balance()
    db.add(client)
    db.commit()
    return sum


def client_file(token):               #ici on consulte la fiche client
    log.info('Controler client_file starts')
    #req = db.query(Client).filter_by(token=token)#.filter_by(token)# ici grace à db.query(Client) on parcours la table client et on récupère le client qui correspond au get(client_id) (l'id du client donc le client qui a pour id, l'id demandé c a d passé en paramètre)
    #result = db.execute(req).fetchone()
    #client = convert_to_client(result)
    id_client = get_client_using_Token(token)
    client = db.query(Client).get(id_client)
    #print(client)
    account_client= client.accounts
    #print(account_client)
    #total =0
    total = iterate_credit_account(token)


    if request.method == 'POST': # si la requête que le serveur a reçu est post( request.method fait référence à une variable contenu dans request qui contient le mode post ou get ou delete ect...)
        account_number = request.form['account_number']# ici on récupère la valeur du input account_number, qui va déterminer le type de compte
        #account = db.query(BankAccount).get(account_number)# ici on va chercher dans la table BankAccount la ligne correspondante à l'account_number
        #print(account_number)
        account = db.query(BankAccount).filter_by(number=account_number).first()
        #total_account = TotalAccounts(client,token)
        #iterate_account(token)
        total = 0
        if request.form['action'] == 'interest': # va faire la distinction entre les bouttons débit ou interest, ici si la valeur du boutton vaut interest on rentre dans la condition
            earned = account.interest()# ici l'objet courant (en fonction de l'account_number, soit de type saving_account soit de type debit_account dans le cas du if c'est un saving) on lui applique la méthode interest de la classe saving_account
            account.credit(earned)# ici comme l'objet account de type saving_account hérite de BankAccount on peut accéder donc à la méthode credit dans laquelle on passe en paramètre le resultat de interest contenue dans earned
            #total = total_account.total_amount(token)
            total=iterate_credit_account(token)
            #print(total)
        else:
            try:
                amount = get_amount()# ici on tente de récupèrer le montant que l'on a rentrer
            except ValueError as ve: # si il n'arrive pas à convertir en float
                return render_template('client_file.html', client=account_client, error=ve)# ici on retourne la page html client_file.html au niveau de laquelle on injecte dans les variables client et error accessibles depuis la page html, on leur pattribut comme valeur pour client la variable client définit plus haut qui contient le client en cours, et dans error le message d'erreur définit dans exception
            if request.form['action'] == 'credit':# ici on verifie quel boutton a été cliquer (c a d que l'on vérifie si la velur de la clé action est bien credit)
                account.credit(amount) #dans ce cas on ajoute amount à l'account
                #print(account)
                #total= total_account.total_amount(token)
                total = iterate_credit_account(token)
            else:
                account.debit(amount)# sinon on débite amount d'account
                #total= total_account.total_amount(token)
                #print(client)
                total = iterate_credit_account(token)
                #current_sum = total
        #db.commit()# ici on commit la base de données et on enregistre les modifs de l'account
    #print(request.method)
    #print("Total : {}".format(total))
    return render_template('client_file.html', client=client , accounts=account_client, token=token, name=total)# on rend le résultat avec le nouveau solde dans la page html (client à comme paramètre une variable de classe account[] qui met à jour à chaque fois la liste  des comptes (saving et debit account)

def client_file_client(token):               #ici on consulte la fiche client
    log.info('Controler client_file_client starts')
    #req = db.query(Client).filter_by(token=token)#.filter_by(token)# ici grace à db.query(Client) on parcours la table client et on récupère le client qui correspond au get(client_id) (l'id du client donc le client qui a pour id, l'id demandé c a d passé en paramètre)
    #result = db.execute(req).fetchone()
    #client = convert_to_client(result)
    id_client = get_client_using_Token(token)
    client = db.query(Client).get(id_client)
    #print(client)
    account_client= client.accounts
    print(account_client)
    #print(account_client)
    #total =0
    total = iterate_credit_account(token)


    if request.method == 'POST': # si la requête que le serveur a reçu est post( request.method fait référence à une variable contenu dans request qui contient le mode post ou get ou delete ect...)
        account_number = request.form['account_number']# ici on récupère la valeur du input account_number, qui va déterminer le type de compte
        #account = db.query(BankAccount).get(account_number)# ici on va chercher dans la table BankAccount la ligne correspondante à l'account_number
        #print(account_number)
        account = db.query(BankAccount).filter_by(number=account_number).first()
        #total_account = TotalAccounts(client,token)
        #iterate_account(token)
        total = 0
        if request.form['action'] == 'interest': # va faire la distinction entre les bouttons débit ou interest, ici si la valeur du boutton vaut interest on rentre dans la condition
            earned = account.interest()# ici l'objet courant (en fonction de l'account_number, soit de type saving_account soit de type debit_account dans le cas du if c'est un saving) on lui applique la méthode interest de la classe saving_account
            account.credit(earned)# ici comme l'objet account de type saving_account hérite de BankAccount on peut accéder donc à la méthode credit dans laquelle on passe en paramètre le resultat de interest contenue dans earned
            #total = total_account.total_amount(token)
            total=iterate_credit_account(token)
            #print(total)
        else:
            try:
                amount = get_amount()# ici on tente de récupèrer le montant que l'on a rentrer
            except ValueError as ve: # si il n'arrive pas à convertir en float
                return render_template('client_file.html', client=account_client, error=ve)# ici on retourne la page html client_file.html au niveau de laquelle on injecte dans les variables client et error accessibles depuis la page html, on leur pattribut comme valeur pour client la variable client définit plus haut qui contient le client en cours, et dans error le message d'erreur définit dans exception
            if request.form['action'] == 'credit':# ici on verifie quel boutton a été cliquer (c a d que l'on vérifie si la velur de la clé action est bien credit)
                account.credit(amount) #dans ce cas on ajoute amount à l'account
                #print(account)
                #total= total_account.total_amount(token)
                total = iterate_credit_account(token)
            else:
                account.debit(amount)# sinon on débite amount d'account
                #total= total_account.total_amount(token)
                #print(client)
                total = iterate_credit_account(token)
                #current_sum = total
        #db.commit()# ici on commit la base de données et on enregistre les modifs de l'account
    #print(request.method)
    #print("Total : {}".format(total))
    return render_template('client_file_client.html', client=client , accounts=account_client, token=token, name=total)

def add_account(token, type):                 # Au clic de "Debit account" ou "Saving account" dans la page client_file.html, on injecte les valeurs de client_id et de type dans l'url, qui est ensuite récupéré comme paramètres client_id et type dans la fonction add_account
    log.info('Controler add_account starts')  # On met à jour le log avec une entrée de type info
    client = get_client_using_Token(token)
    if type == 1:                             # type est une variable qui va permettre a Flask de discriminer quel type de compte l'utilisateur a souhaité créer. Ici type=1 fait référence à un "Debit account"
        account = DebitAccount(client)     # Si l'utilisateur a souhaité créer un "Debit account", on crée une instance de DebitAccount, liée au client en cours à travers le paramètre client_id et stockée dans la variable account
    else:
        account = SavingAccount(client, 0.03)  # Sinon, l'utilisateur a souhaité créer un "Saving account", on crée donc une instance de SavingAccount, liée au client à travers client_id et stockée dans account
    db.add(account)                   # On ajoute le nouveau compte dans la base de donnée
    db.commit()                               # et on valide la modification de la base de donnée (commit)
    return redirect(url_for('client_file_client', token=token))# Enfin on redirige l'utilisateur vers sa page profil client_file.html


def add_account_admin(token, type):                 # Au clic de "Debit account" ou "Saving account" dans la page client_file.html, on injecte les valeurs de client_id et de type dans l'url, qui est ensuite récupéré comme paramètres client_id et type dans la fonction add_account
    log.info('Controler add_account starts')  # On met à jour le log avec une entrée de type info
    client = get_client_using_Token(token)
    if type == 1:                             # type est une variable qui va permettre a Flask de discriminer quel type de compte l'utilisateur a souhaité créer. Ici type=1 fait référence à un "Debit account"
        account = DebitAccount(client)     # Si l'utilisateur a souhaité créer un "Debit account", on crée une instance de DebitAccount, liée au client en cours à travers le paramètre client_id et stockée dans la variable account
    else:
        account = SavingAccount(client, 0.03)  # Sinon, l'utilisateur a souhaité créer un "Saving account", on crée donc une instance de SavingAccount, liée au client à travers client_id et stockée dans account
    db.add(account)                   # On ajoute le nouveau compte dans la base de donnée
    db.commit()                               # et on valide la modification de la base de donnée (commit)
    return redirect(url_for('client_file', token=token))# Enfin on redirige l'utilisateur vers sa page profil client_file.html


def del_account(token):
    log.info('Controle del_account starts')
    client_id= get_client_using_Token(token)
    if request.method == 'POST':
        enter_number=  request.form['number']
        req= db.query(BankAccount).filter_by(number=enter_number)
        account=db.execute(req).fetchone()
        #print("this account admin", account)

        if account is None:
            return render_template('redirectory_to_delete_account.html', number=enter_number)

        if client_id != account[2]:
            return render_template('redirectory_to_delete_account.html', number=enter_number)

        if client_id == account[2]:

            db.query(SavingAccount).filter_by(number=request.form['number']).delete()
            #print(req)
            db.commit()
            return redirect(url_for('client_file', token=token))# dans le url_for (qui est une fonction) le 'client file' ici est un end point d'une url définiit dans le main et qui va appeler le reste de l'url au moment de l'éxécution de la fonction, et qui va injecter la donneé contenu de "client_id" à l'emplcement correspondant dans l'url du main
    else:
        return render_template('delete_account.html', token=token)


def del_account_client(token):
    log.info('Controle del_account_client starts')
    client_id= get_client_using_Token(token)
    if request.method == 'POST':
        enter_number=  request.form['number']
        req= db.query(BankAccount).filter_by(number=enter_number)
        account=db.execute(req).fetchone()
        print("this account client", account)

        if account is None:
            return render_template('redirectory_to_delete_account_client.html', number=enter_number)

        if client_id != account[2] or account is None:
            return render_template('redirectory_to_delete_account_client.html', number=enter_number)

        if client_id == account[2]:

            db.query(SavingAccount).filter_by(number=request.form['number']).delete()
            #print(req)
            db.commit()
            return redirect(url_for('client_file', token=token))# dans le url_for (qui est une fonction) le 'client file' ici est un end point d'une url définiit dans le main et qui va appeler le reste de l'url au moment de l'éxécution de la fonction, et qui va injecter la donneé contenu de "client_id" à l'emplcement correspondant dans l'url du main
    else:
        return render_template('delete_account_client.html',token=token)



def display_account(token):                   # Permet d'afficher le profil du compte sélectionné
    log.info('Controler display_account starts') # On met à jour le log avec une entrée de type info
    #raise NotImplementedError()                  # La fonction est prévue mais pas encore implémentée. Le raise permet de traiter proprement le cas d'erreur en informant l'utilisateur que la fonctionnalité n'est pas encore opérationnelle


