from sqlalchemy import create_engine, Column, Integer, String, Float, \
    ForeignKey  # ici on importe tout ce qu'il faut créer et gérer une table, create_engine: permet de gérer la db (syntax: base_de _données.), le reste fait référence aux composants de la db
from sqlalchemy.ext.declarative import \
    declarative_base  # declarative_base permet de fusionner la table, la map et l'objet map crées,  en base de données, c'est propre à sqlachelmy
from sqlalchemy.orm import sessionmaker, relationship, \
    scoped_session  # tous les outils nécéssaire à la création du connecteur qui va faire le lien entre la base données et python ou un autre langage
import hashlib


engine = create_engine('sqlite:///bankin.db',
                       echo=False)  # on crée le moteur de la base de données responsale de traiter les requêtes associé au fichier qui héberger la base de données, passé en paramètre, la paramètre echo permet de dire au serveur sql si il doit répondre par un message à la requête, ici false donc ne renvois rien
Base = declarative_base(
    bind=engine)  # permet de structurer la base de données (création de la table, relation ect...), le paramètre bind est un connectable(interface d'objet qui supporte l'execution du code sql) optionnel, ici connecté au moteur de la db (engine)
session = scoped_session(sessionmaker(bind=engine))  # ici on crée le connecteur qui sera relié au engine


class Client(Base):
    __tablename__ = 'clients'
    client_id = Column(Integer, primary_key=True)
    firstname = Column(String(30), nullable=False)
    lastname = Column(String(30), nullable=False)
    email = Column(String(75), nullable=True)
    accounts = relationship("BankAccount", back_populates="client")
    token = Column(String(30), nullable=False)
    password = Column(String(30), nullable=True)
    current_sum = Column(Integer, nullable=False)

    def __init__(self, firstname, lastname, email, token,
                 password):  # le constructeur permet d'insérer de la données à la table ci dessus
        self.firstname = firstname.capitalize()
        self.lastname = lastname.upper()
        self.email = email.lower()
        self.accounts = []
        self.token = token  # ici on injecte la valeur token donnée en paramètre du constructeur dans la variable self.token
        self.password = hashlib.sha256(bytes(password, "utf-8")).hexdigest()
        self.current_sum = 0

    def __str__(self):  # ici permet de lire sur une ligne deux paramètres de la table, ici firstname et lastname
        # string = '{} {} {} {} {} {} {}'.format(self.client_id, self.firstname, self.lastname, self.email, self.token, self.password, self.current_sum)

        # for account in self.accounts:
        #    string += str(account.get_account_balance()) + "\n"

        # return str(self.accounts)
        return '{} {} {} {} {} {} {}'.format(self.client_id, self.firstname, self.lastname, self.email, self.token,
                                             self.password, self.current_sum)


class BankAccount(Base):
    __tablename__ = 'bank_accounts'
    number = Column(Integer, primary_key=True)
    _balance = Column(Float)
    client_id = Column(ForeignKey('clients.client_id'))
    client = relationship("Client",
                          back_populates="accounts")  # correspondance de la liaison dans la table Client, ici la table cible(relation qu'oblige sqlalchemy), noter que l'on peut faire une réfence à la table cible donc le back est gerer automatiquement avec la paramètre backref, qui n'oblige pas de faire une raltion correspondante dans la table cible
    type = Column(String(20))
    __mapper_args__ = {
        # permet de dire au engine comment manipuler les tables entre elles en fonction du type d'héritage
        'polymorphic_on': type,
        # paramètre qui va dire au engine quel sera le discriminateur, c'est à dire dans la cas présent, type va déterminer le type d'oblet(saving_account ou debit_account)
        'polymorphic_identity': 'bank_account'  # va déterminer comment représenter l'objet courant à l'affichage
    }

    def __init__(self, client_id):
        self.client_id = client_id
        self._balance = 0  # ici variable de classe privée

    def credit(self, amount):  # pour créditer l'account
        client = session.query(Client).filter_by(client_id=self.client_id).first()
        print("credit client {}".format(client))
        if amount >= 0:
            self._balance += amount  # ici si l'amount passée en parmètre est supérieur ou nul à 0, on incremente _balance avec amount( self._balance est égale à balance plus amount)
            client.current_sum += amount
            session.add(client)
            session.commit()

        else:
            raise Exception("You can't add a negative value to the account balance")

    def get_account_balance(self):
        return self._balance  # ici (ne pas oublier self fait référence à lui même) on récupère _balance modifier dans credit

    @property  # pas utile
    def get_type_name(self):  # récupère le nom du type d'account
        return 'General account'

    def __str__(self):  # affichage de l'account
        return 'General account ({} {})'.format(self.number, self._balance)


class DebitAccount(BankAccount):
    __mapper_args__ = {
        # sert à configurer l'héritage ici 'polymorphic_identity' est l'étiquette que l'on va donner à la configuration
        'polymorphic_identity': 'debit_accounts'
        # voir au dessus la signification, à noter qu'il n'y a pas de manière explicite le polymorphic_on, car il est hérité de la classe BankAccount et écrase la valeur du polymorphic_identity
    }

    def debit(self, amount):
        # client = session.query(Client).filter_by(client_id=self.client_id).first()
        # print("debit client {}".format(client))
        if amount >= 0:
            self._balance -= amount  # ici on décrémente la copie de _balance qui se trouve dans la fille (_balance est égale à _balanace - amount)
            # client.current_sum -= amount
        else:
            raise Exception("You can't soustract a negative value to the account balance")

    @property  # voir au dessus
    def get_type_name(self):  # ici on renvois le type d'account
        return 'Debit account'

    def __repr__(self):  # voir au dessus
        return 'Debit account {} {} {}'.format(self.client_id, self.number, self._balance)


class SavingAccount(BankAccount):
    __mapper_args__ = {
        'polymorphic_identity': 'saving_accounts'  # voir signifacation au dessus
    }
    rate = Column(Float)  # rajoute une colonne spécifique à la classe SavingAccount

    def __init__(self, client_id, rate):
        super().__init__(
            client_id)  # appelle le constructeur de la mère dans lequel il passe client_id(paramètre se trouvant dans la constructeur de la classe mère) en paramètre du super().__init__() ce qui est oliger en python
        self.rate = rate

    def interest(self):  # calcule des intêrets
        return self._balance * self.rate

    @property  # voir au dessus
    def get_type_name(self):  # ici on renvois le type d'account
        return 'Saving account'

    def __str__(self):  # voir au dessus
        return 'Saving account{} {} {}'.format(self.client_id, self.number, self._balance)


class TotalAccounts(BankAccount):
    __mapper_args__ = {
        'polymorphic_identity': 'total_accounts'  # voir signifacation au dessus
    }

    def __init__(self, client_id, token):
        super().__init__(client_id)
        self.total = self.total_amount(token)

    def total_amount(self, token):
        current_account = 0
        client = session.query(Client).filter_by(token=token).first()
        for account in client.accounts:
            current_account += account.get_account_balance()
            return current_account

    def get_type_name(self):  # ici on renvois le type d'account
        return 'Total account'

    def __str__(self):  # voir au dessus
        return 'Total account {} {} {}'.format(self.client_id, self.number, self.total)


if __name__ == '__main__':
    Base.metadata.create_all(
        engine)  # metadata est un objet contenu dans declarative_base() qui est elle même appeler dans la varibla Base qu permet de collecter toutes les tables (toutes les infos à travers les classes de table) qui seront créer à l'appel du create_all(méthode de metadata) dans lequel on aura liée le moteur de la base de données(ici engine) passé en paramètre
    # à ce stade donc crée tout (base de données, moteur, structure) et le lance
