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
        FROM pompe_à_chaleur
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
    sql = '''SELECT Id_modèle, nom_modèle, marque FROM Modèle;'''
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
    sql2 = "SELECT Id_modèle, nom_modèle, marque FROM Modèle;"
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



# -------------------------------------------
# GESTION DES CLIENTS
# -------------------------------------------
@app.route('/client/show')
def show_client():
    mycursor = get_db().cursor()
    sql = "SELECT * FROM Client ORDER BY nom_client;"
    mycursor.execute(sql)
    clients = mycursor.fetchall()
    return render_template('client/show_client.html', clients=clients)

@app.route('/client/add', methods=['GET'])
def add_client():
    return render_template('client/add_client.html')

@app.route('/client/add', methods=['POST'])
def valid_add_client():
    nom = request.form.get('nom_client')
    prenom = request.form.get('prenom_client')
    adresse = request.form.get('adresse')
    telephone = request.form.get('telephone')

    mycursor = get_db().cursor()
    sql = "INSERT INTO Client (nom_client, prenom_client, adresse, telephone) VALUES (%s, %s, %s, %s);"
    mycursor.execute(sql, (nom, prenom, adresse, telephone))
    get_db().commit()
    return redirect('/client/show')

@app.route('/client/delete')
def delete_client():
    id_client = request.args.get('id')
    mycursor = get_db().cursor()
    sql = "DELETE FROM Client WHERE Id_Client=%s;"
    mycursor.execute(sql, (id_client))
    get_db().commit()
    return redirect('/client/show')

@app.route('/client/edit', methods=['GET'])
def edit_client():
    id_client = request.args.get('id')
    mycursor = get_db().cursor()
    sql = "SELECT * FROM Client WHERE Id_Client=%s;"
    mycursor.execute(sql, (id_client))
    client = mycursor.fetchone()
    return render_template('client/edit_client.html', client=client)

@app.route('/client/edit', methods=['POST'])
def valid_edit_client():
    id_client = request.form.get('id_client')
    nom = request.form.get('nom_client')
    prenom = request.form.get('prenom_client')
    adresse = request.form.get('adresse')
    telephone = request.form.get('telephone')

    mycursor = get_db().cursor()
    sql = '''UPDATE Client SET nom_client=%s, prenom_client=%s, adresse=%s, telephone=%s WHERE Id_Client=%s;'''
    mycursor.execute(sql, (nom, prenom, adresse, telephone, id_client))
    get_db().commit()
    return redirect('/client/show')



# -------------------------------------------
# ETAT : STATISTIQUES
# -------------------------------------------
@app.route('/etat/show')
def show_etat():
    mycursor = get_db().cursor()
    sql = '''
        SELECT 
            modele.nom_modele,
            modele.marque,
            COUNT(pompe_a_chaleur.id_pompe_a_chaleur) AS nombre_pac,
            AVG(pompe_a_chaleur.prix_pac) AS prix_moyen,
            AVG(pompe_a_chaleur.puissance) AS puissance_moyenne
        FROM pompe_a_chaleur
        JOIN modele ON pompe_a_chaleur.id_modele = modele.id_modele
        GROUP BY modele.nom_modele, modele.marque;
    '''
    mycursor.execute(sql)
    stats = mycursor.fetchall()
    return render_template('etat/show_etat.html', stats=stats)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
