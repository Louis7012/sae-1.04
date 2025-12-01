#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Flask, request, render_template, redirect, flash
from flask import session, g
import pymysql.cursors

app = Flask(__name__)
app.secret_key = 'une cle(token) : grain de sel(any random string)'

def get_db():
    if 'db' not in g:
        g.db = pymysql.connect(
            host="serveurmysql",
            user="lmarting",
            password="secret",
            database="BDD_lmarting",
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    return g.db

@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()


@app.route('/')
def show_layout():
    return render_template('layout.html')


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


@app.route('/pac/add', methods=['GET'])
def add_pac():
    mycursor = get_db().cursor()
    sql = 'SELECT id_modele, nom_modele, marque FROM modele;'
    mycursor.execute(sql)
    modeles = mycursor.fetchall()
    return render_template('pac/add_pac.html', modeles=modeles)


# -------------------------------------------
# AJOUT D'UNE PAC (POST)
# -------------------------------------------
@app.route('/pac/add', methods=['POST'])
def valid_add_pac():
    # valeurs = peu importe si vide → MySQL accepte NULL
    values = (
        request.form.get('puissance') or None,
        request.form.get('eff_energie') or None,
        request.form.get('classe_energie') or None,
        request.form.get('temp_fonctionnement_cel') or None,
        request.form.get('volume_chauffe') or None,
        request.form.get('eff_saison') or None,
        request.form.get('dimensions') or None,
        request.form.get('prix_pac') or None,
        request.form.get('id_modele')
    )

    mycursor = get_db().cursor()
    sql = '''
    INSERT INTO pompe_a_chaleur
    (puissance, eff_energie, classe_energie, temp_fonctionnement_cel, 
     volume_chauffe, eff_saison, dimensions, prix_pac, id_modele)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);
    '''
    message="Pompe a chaleur ajouté : " + request.form.get('id_modele') +" puissance : " + request.form.get('puissance') + "température" + request.form.get('temp_fonctionnement_cel') + "volume" + request.form.get('volume_chauffe') + "efficacité saisonnière" + request.form.get('eff_saison') + "dimensions" + request.form.get('dimensions')+ "prix" + request.form.get('prix_pac')
    flash(message, 'success')
    mycursor.execute(sql, values)
    get_db().commit()

    return redirect('/pac/show')


@app.route('/pac/delete')
def delete_pac():
    id = int(request.args.get('id'))
    mycursor = get_db().cursor()
    requete1=f"DELETE FROM intervention WHERE id_pompe_a_chaleur={id};"
    mycursor.execute( requete1 )
    message="Pompe a chaleur supprimé : " + request.form.get('id_modele')
    flash(message, 'success')
    get_db().commit()
    return redirect('/pac/show')


@app.route('/pac/edit', methods=['GET'])
def edit_pac():
    id = request.args.get('id')
    mycursor = get_db().cursor()

    # PAC
    sql = 'SELECT * FROM pompe_a_chaleur WHERE id_pompe_a_chaleur=%s;'
    mycursor.execute(sql, (id,))
    pac = mycursor.fetchone()

    # modèles
    sql2 = "SELECT id_modele, nom_modele, marque FROM modele;"
    mycursor.execute(sql2)
    modeles = mycursor.fetchall()

    return render_template('pac/edit_pac.html', pac=pac, modeles=modeles)


@app.route('/pac/edit', methods=['POST'])
def valid_edit_pac():
    values = (
        request.form.get('puissance') or None,
        request.form.get('eff_energie') or None,
        request.form.get('classe_energie') or None,
        request.form.get('temp_fonctionnement_cel') or None,
        request.form.get('volume_chauffe') or None,
        request.form.get('eff_saison') or None,
        request.form.get('dimensions') or None,
        request.form.get('prix_pac') or None,
        request.form.get('id_modele'),
        request.form.get('id')
    )

    sql = '''
        UPDATE pompe_a_chaleur
        SET puissance=%s, eff_energie=%s, classe_energie=%s,
            temp_fonctionnement_cel=%s, volume_chauffe=%s, eff_saison=%s,
            dimensions=%s, prix_pac=%s, id_modele=%s
        WHERE id_pompe_a_chaleur=%s;
    '''

    message="Pompe a chaleur modifié : " + request.form.get('id_modele') +" puissance : " + request.form.get('puissance') + "température" + request.form.get('temp_fonctionnement_cel') + "volume" + request.form.get('volume_chauffe') + "efficacité saisonnière" + request.form.get('eff_saison') + "dimensions" + request.form.get('dimensions')+ "prix" + request.form.get('prix_pac')
    flash(message, 'success')
    mycursor = get_db().cursor()
    mycursor.execute(sql, values)
    get_db().commit()

    return redirect('/pac/show')

#--------------------------------------------
# ETATS / STATISTIQUES
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


# -------------------------------------------
# INTERVENTIONS
# -------------------------------------------
    
@app.route('/interventions')
def show_intervention():
    mycursor = get_db().cursor()
    sql='''
    SELECT id_intervention, date_inter, id_pompe_a_chaleur, id_personnel, id_motif, id_client
    FROM intervention
    ORDER BY date_inter DESC'''
    mycursor.execute(sql)
    all_interventions = mycursor.fetchall()
    return render_template('interventions/show_interventions.html', interventions=all_interventions)

@app.route('/interventions/add', methods=['GET'])
def add_intervention():
    mycursor = get_db().cursor()
    sql='''
    SELECT id_modele, nom_modele
    FROM modele'''
    mycursor.execute(sql)
    all_modeles= mycursor.fetchall()
    mycursor = get_db().cursor()
    sql='''
    SELECT id_personnel, nom_personnel
    FROM personnel'''
    mycursor.execute(sql)
    all_personnel = mycursor.fetchall()
    mycursor = get_db().cursor()
    sql='''
    SELECT id_motif, libelle_motif
    FROM motif'''
    mycursor.execute(sql)
    all_motifs = mycursor.fetchall()
    mycursor = get_db().cursor()
    sql='''
    SELECT id_client, nom_client, prenom_client
    FROM client'''
    mycursor.execute(sql)
    all_clients = mycursor.fetchall()
    return render_template('interventions/add_interventions.html', modeles=all_modeles,personnel=all_personnel,motifs=all_motifs,clients=all_clients)

@app.route('/interventions/add', methods=['POST'])
def valid_add_intervention():
    date = request.form.get('date')
    modele = request.form.get('modele')
    personnel = request.form.get('personnel')
    motif = request.form.get('motif')
    client = request.form.get('client')
    mycursor = get_db().cursor()
    sql='''
    INSERT INTO intervention(id_intervention, date_inter, id_pompe_a_chaleur, id_personnel, id_motif, id_client)
    VALUES (NULL, %s, %s, %s, %s, %s);'''
    tuple_param=(date, modele, personnel, motif, client)
    mycursor.execute(sql,tuple_param)
    get_db().commit()
    message = u'Intervention ajoutée. Date : '+date+ ' / Modèle : ' + modele + ' / Personnel : ' + personnel + ' / Motif : '+  motif + ' / Client : ' + client
    flash(message, 'alert-success')
    return redirect('/interventions')

@app.route('/inerventions/edit', methods=['GET'])
def edit_intervention():
    mycursor = get_db().cursor()
    id=request.args.get('id')
    if id != None and id.isnumeric():
        indice = int(id)
        sql='''
        SELECT *
        FROM intervention
        WHERE id_intervention=%s'''
        mycursor.execute(sql,indice)
        inter_cible=mycursor.fetchone()
    else:
        inter_cible=None
    sql = '''
        SELECT id_modele, nom_modele
        FROM modele'''
    mycursor.execute(sql)
    all_modeles = mycursor.fetchall()
    print(all_modeles)
    sql = '''
        SELECT id_personnel, nom_personnel
        FROM personnel'''
    mycursor.execute(sql)
    all_personnel = mycursor.fetchall()
    sql = '''
        SELECT id_motif, libelle_motif
        FROM motif'''
    mycursor.execute(sql)
    all_motifs = mycursor.fetchall()
    sql = '''
        SELECT id_client, nom_client, prenom_client
        FROM client'''
    mycursor.execute(sql)
    all_clients = mycursor.fetchall()
    return render_template('interventions/edit_interventions.html', intervention=inter_cible, modeles=all_modeles,personnel=all_personnel,motifs=all_motifs,clients=all_clients)

@app.route('/interventions/edit', methods=['POST'])
def valid_edit_intervention():
    mycursor = get_db().cursor()
    id = request.form.get('id')
    date = request.form.get('date')
    modele = request.form.get('modele')
    personnel = request.form.get('personnel')
    motif = request.form.get('motif')
    client = request.form.get('client')
    sql = '''
            UPDATE intervention
            SET date_inter = %s,
                id_pompe_a_chaleur = %s,
                id_personnel = %s,
                id_motif = %s,
                id_client = %s
            WHERE id_intervention = %s
          '''
    valeurs = (date, modele, personnel, motif, client, id)
    mycursor.execute(sql, valeurs)
    get_db().commit()
    message = u'Intervention modifiée. ID : '+ id+' / Date : ' + date + ' / Modèle : ' + modele + ' / Personnel : ' + personnel + ' / Motif : ' + motif + ' / Client : ' + client
    flash(message, 'alert-success')
    return redirect('/interventions')

@app.route('/interventions/delete')
def delete_intervention():
    mycursor = get_db().cursor()
    id=request.args.get('id')
    sql = '''
    DELETE FROM intervention
    WHERE id_intervention = %s;'''
    mycursor.execute(sql, id)
    get_db().commit()
    return redirect('/interventions')

# -------------------------------------------
# STATISTIQUES DES INTERVENTIONS
# -------------------------------------------

@app.route('/interventions/etats')
def show_etat_interventions():
    mycursor = get_db().cursor()
    sql = '''
        SELECT personnel.id_personnel, AVG(intervention.date_inter) AS moyen_date, personnel.nom_personnel
        FROM personnel
        JOIN intervention ON intervention.id_personnel = personnel.id_personnel
        GROUP BY personnel.id_personnel, personnel.nom_personnel
        ORDER BY moyen_date DESC;
    '''
    mycursor.execute(sql)
    stats = mycursor.fetchall()
    print(stats)
    return render_template('/interventions/etats_interventions.html', stats=stats)

# -------------------------------------------
# LANCEMENT SERVEUR
# -------------------------------------------
if __name__ == '__main__':
    app.run(debug=True, port=5000)
