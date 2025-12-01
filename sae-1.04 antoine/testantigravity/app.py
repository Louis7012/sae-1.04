#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Flask, request, render_template, redirect, flash

app = Flask(__name__)
app.secret_key = 'une cle(token) : grain de sel(any random string)'

                                    ## à ajouter
from flask import session, g
import pymysql.cursors

def get_db():
    if 'db' not in g:
        g.db =  pymysql.connect(
            host="serveurmysql",                 # à modifier
            user="lmarting",                     # à modifier
            password="secret",                # à modifier
            database="BDD_lmarting",        # à modifier
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    return g.db

@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

app = Flask(__name__)

# -------------------------------------------
# PAGE D'ACCUEIL
# -------------------------------------------
@app.route('/')
def show_layout():
    return render_template('layout.html')


# -------------------------------------------
# AFFICHAGE DES POMPES À CHALEUR
# -------------------------------------------
@app.route('/pac/show')
def show_pac():
    mycursor = get_db().cursor()
    sql = '''
        SELECT 
            id_pompe_a_chaleur AS id,
            puissance,
            eff_energie,
            classe_energie,
            temp_fonctionnement_cel,
            volume_chauffe,
            eff_saison,
            dimensions,
            prix_pac,
            modele.nom_modele AS modele,
            modele.marque AS marque
        FROM pompe_a_chaleur
        JOIN modele ON pompe_a_chaleur.id_modele = modele.id_modele
        ORDER BY id_pompe_a_chaleur;
    '''
    mycursor.execute(sql)
    liste_pac = mycursor.fetchall()
    return render_template('pac/show_pac.html', pompes=liste_pac)


# -------------------------------------------
# AJOUT D'UNE POMPE À CHALEUR (GET)
# -------------------------------------------
@app.route('/pac/add', methods=['GET'])
def add_pac():
    mycursor = get_db().cursor()
    sql = '''SELECT id_modele, nom_modele, marque FROM modele;'''
    mycursor.execute(sql)
    modeles = mycursor.fetchall()

    return render_template('pac/add_pac.html', modeles=modeles)


# -------------------------------------------
# AJOUT D'UNE POMPE À CHALEUR (POST)
# -------------------------------------------
@app.route('/pac/add', methods=['POST'])
def valid_add_pac():

    puissance = request.form.get('puissance')
    eff_energie = request.form.get('eff_energie')
    classe_energie = request.form.get('classe_energie')
    temp = request.form.get('temp_fonctionnement_cel')
    volume = request.form.get('volume_chauffe')
    eff_saison = request.form.get('eff_saison')
    dimensions = request.form.get('dimensions')
    prix = request.form.get('prix_pac')
    modele = request.form.get('id_modele')

    mycursor = get_db().cursor()
    tuple_param = (puissance, eff_energie, classe_energie, temp, volume, eff_saison, dimensions, prix, modele)

    sql = '''
    INSERT INTO pompe_a_chaleur
    (puissance, eff_energie, classe_energie, temp_fonctionnement_cel, volume_chauffe, eff_saison, dimensions, prix_pac, id_modele)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);
    '''

    mycursor.execute(sql, tuple_param)
    get_db().commit()

    return redirect('/pac/show')


# -------------------------------------------
# SUPPRESSION
# -------------------------------------------
@app.route('/pac/delete')
def delete_pac():

    id = request.args.get('id')

    mycursor = get_db().cursor()
    tuple_param = (id)

    sql = "DELETE FROM pompe_a_chaleur WHERE id_pompe_a_chaleur=%s;"
    mycursor.execute(sql, tuple_param)
    get_db().commit()

    return redirect('/pac/show')


# -------------------------------------------
# MODIFIER UNE POMPE À CHALEUR (GET)
# -------------------------------------------
@app.route('/pac/edit', methods=['GET'])
def edit_pac():

    id = request.args.get('id')

    mycursor = get_db().cursor()

    # Charger la PAC à modifier
    sql = '''
        SELECT * FROM pompe_a_chaleur
        WHERE id_pompe_a_chaleur=%s;
    '''
    mycursor.execute(sql, (id))
    pac = mycursor.fetchone()

    # Charger les modèles
    sql2 = "SELECT Id_modele, nom_modele, marque FROM modele;"
    mycursor.execute(sql2)
    modeles = mycursor.fetchall()

    return render_template('pac/edit_pac.html', pac=pac, modeles=modeles)


# -------------------------------------------
# MODIFIER UNE POMPE À CHALEUR (POST)
# -------------------------------------------
@app.route('/pac/edit', methods=['POST'])
def valid_edit_pac():

    id = request.form.get('id')
    puissance = request.form.get('puissance')
    eff_energie = request.form.get('eff_energie')
    classe_energie = request.form.get('classe_energie')
    temp = request.form.get('temp_fonctionnement_cel')
    volume = request.form.get('volume_chauffe')
    eff_saison = request.form.get('eff_saison')
    dimensions = request.form.get('dimensions')
    prix = request.form.get('prix_pac')
    modele = request.form.get('id_modele')

    tuple_param = (puissance, eff_energie, classe_energie, temp, volume, eff_saison, dimensions, prix, modele, id)

    sql = '''
        UPDATE pompe_a_chaleur
        SET puissance=%s, eff_energie=%s, classe_energie=%s,
            temp_fonctionnement_cel=%s, volume_chauffe=%s, eff_saison=%s,
            dimensions=%s, prix_pac=%s, id_modele=%s
        WHERE id_pompe_a_chaleur=%s;
    '''

    mycursor = get_db().cursor()
    mycursor.execute(sql, tuple_param)

    get_db().commit()

    return redirect('/pac/show')




# GESTION DES COMMANDES

@app.route('/commande/show')
def show_commande():
    mycursor = get_db().cursor()
    sql = "SELECT * FROM commande;"
    mycursor.execute(sql)
    commande = mycursor.fetchall()
    return render_template('commande/show_commande.html', commande=commande)

@app.route('/commande/add', methods=['GET'])
def add_commande():
    db = get_db()
    mycursor = db.cursor()
    sql='''SELECT ligne_de_commande.id_ligne_de_commande from ligne_de_commande;'''
    mycursor.execute(sql)
    ligne_de_commande = mycursor.fetchall()
    print(ligne_de_commande)
    sql = ''' SELECT id_client, prenom_client, nom_client from client; '''
    mycursor.execute(sql)
    clients = mycursor.fetchall()
    return render_template('commande/add_commande.html', liste_ligne_de_commande=ligne_de_commande, clients=clients)

@app.route('/commande/add', methods=['POST'])
def valid_add_commande():
    prix_cmd = request.form.get('prix_cmd')
    date_cmd = request.form.get('date_cmd')
    id_ligne_de_commande = request.form.get('id_ligne_de_commande')
    id_client = request.form.get('id_client')

    mycursor = get_db().cursor()
    sql = '''INSERT INTO commande (prix_cmd, date_cmd, id_ligne_de_commande, id_client) VALUES (%s, %s, %s, %s);'''
    mycursor.execute(sql, (prix_cmd, date_cmd, id_ligne_de_commande, id_client))
    get_db().commit()
    return redirect('/commande/show')

@app.route('/commande/delete')
def delete_commande():
    num_commande = request.args.get('id')
    print(num_commande)
    mycursor = get_db().cursor()
    sql = "DELETE FROM commande WHERE num_commande=%s;"
    mycursor.execute(sql, (num_commande,))
    get_db().commit()
    return redirect('/commande/show')

@app.route('/commande/edit', methods=['GET'])
def edit_commande():
    num_commande = request.args.get('id')
    mycursor = get_db().cursor()
    sql = "SELECT * FROM commande WHERE num_commande=%s;"
    mycursor.execute(sql, (num_commande,))
    commande = mycursor.fetchone()
    sql = '''SELECT ligne_de_commande.id_ligne_de_commande from ligne_de_commande;'''
    mycursor.execute(sql)
    ligne_de_commande = mycursor.fetchall()
    sql = ''' SELECT id_client, prenom_client, nom_client from client; '''
    mycursor.execute(sql)
    clients = mycursor.fetchall()


    return render_template('commande/edit_commande.html', commande=commande, ligne_de_commande=ligne_de_commande, clients=clients)

@app.route('/commande/edit', methods=['POST'])
def valid_edit_commande():
    prix_cmd = request.form.get('prix_cmd')
    date_cmd = request.form.get('date_cmd')
    id_ligne_de_commande = request.form.get('id_ligne_de_commande')
    id_client = request.form.get('id_client')
    num_commande = request.form.get('num_commande')

    mycursor = get_db().cursor()
    sql = '''UPDATE commande SET prix_cmd=%s, date_cmd=%s, id_ligne_de_commande=%s, id_client=%s WHERE num_commande=%s;'''
    mycursor.execute(sql, (prix_cmd, date_cmd, id_ligne_de_commande, id_client, num_commande))
    get_db().commit()
    return redirect('/commande/show')



# -------------------------------------------
# ETAT : STATISTIQUES
# -------------------------------------------


@app.route('/etat/show')
def show_etat():
    mycursor = get_db().cursor()

    # 1 — moyenne !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    mycursor.execute('''
        SELECT AVG(prix_cmd) AS moyenne_prix FROM commande;
    ''')
    moyenne = mycursor.fetchone()

    # 2 — total !!!!!!!!!!!!!!!!!!!!!!
    mycursor.execute('''
        SELECT SUM(prix_cmd) AS total_prix FROM commande;
    ''')
    total = mycursor.fetchone()

    # 3 — stats par client !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    mycursor.execute('''
        SELECT id_client, COUNT(*) AS total_commandes, SUM(prix_cmd) AS total_prix_client
        FROM commande
        GROUP BY id_client;
    ''')
    stats_clients = mycursor.fetchall()

    # 4 — top 5 des commandes !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    mycursor.execute('''
        SELECT num_commande, prix_cmd, date_cmd
        FROM commande
        ORDER BY prix_cmd DESC
        LIMIT 5;
    ''')
    top5 = mycursor.fetchall()

    return render_template(
        'etat/show_etat.html',
        moyenne=moyenne,
        total=total,
        stats_clients=stats_clients,
        top5=top5
    )



if __name__ == '__main__':
    app.run(debug=True, port=5000)
