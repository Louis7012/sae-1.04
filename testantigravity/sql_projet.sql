DROP TABLE IF EXISTS parraine;
DROP TABLE IF EXISTS commande;
DROP TABLE IF EXISTS ligne_de_commande;
DROP TABLE IF EXISTS filleul;
DROP TABLE IF EXISTS intervention;
DROP TABLE IDROP TABLE IF EXISTS parraine;
DROP TABLE IF EXISTS commande;
DROP TABLE IF EXISTS ligne_de_commande;
DROP TABLE IF EXISTS filleul;
DROP TABLE IF EXISTS intervention;
DROP TABLE IF EXISTS client;
DROP TABLE IF EXISTS personnel;
DROP TABLE IF EXISTS poste;
DROP TABLE IF EXISTS pompe_a_chaleur;
DROP TABLE IF EXISTS modele;
DROP TABLE IF EXISTS motif;


CREATE TABLE client(
   id_client INT AUTO_INCREMENT,
   adresse VARCHAR(50),
   nom_client VARCHAR(50),
   prenom_client VARCHAR(50),
   telephone VARCHAR(10),
   PRIMARY KEY(id_client)
);

CREATE TABLE filleul(
   id_filleul INT AUTO_INCREMENT,
   nom_filleul VARCHAR(50),
   PRIMARY KEY(id_filleul)
);

CREATE TABLE modele(
   id_modele INT AUTO_INCREMENT,
   nom_modele VARCHAR(50),
   marque VARCHAR(50),
   PRIMARY KEY(id_modele)
);

CREATE TABLE poste(
   id_poste INT AUTO_INCREMENT,
   libelle_poste VARCHAR(50),
   PRIMARY KEY(id_poste)
);

CREATE TABLE motif(
   id_motif INT AUTO_INCREMENT,
   libelle_motif VARCHAR(50),
   PRIMARY KEY(id_motif)
);

CREATE TABLE pompe_a_chaleur(
   id_pompe_a_chaleur INT AUTO_INCREMENT,
   puissance DECIMAL(15,2),
   eff_energie DECIMAL(15,2),
   classe_energie VARCHAR(10),
   temp_fonctionnement_cel INT,
   volume_chauffe DECIMAL(15,2),
   eff_saison DECIMAL(15,2),
   dimensions VARCHAR(50),
   prix_pac DECIMAL(15,2),
   id_modele INT NOT NULL,
   PRIMARY KEY(id_pompe_a_chaleur),
   FOREIGN KEY(id_modele) REFERENCES modele(id_modele)
);

CREATE TABLE personnel(
   id_personnel INT AUTO_INCREMENT,
   nom_personnel VARCHAR(50),
   id_poste INT NOT NULL,
   PRIMARY KEY(id_personnel),
   FOREIGN KEY(id_poste) REFERENCES poste(id_poste)
);

CREATE TABLE ligne_de_commande(
   id_ligne_de_commande INT AUTO_INCREMENT,
   date_livraison DATE,
   quantite INT,
   id_pompe_a_chaleur INT NOT NULL,
   PRIMARY KEY(id_ligne_de_commande),
   FOREIGN KEY(id_pompe_a_chaleur) REFERENCES pompe_a_chaleur(id_pompe_a_chaleur)
);

CREATE TABLE intervention(
   id_intervention INT AUTO_INCREMENT,
   date_inter DATE,
   id_pompe_a_chaleur INT NOT NULL,
   id_personnel INT NOT NULL,
   id_motif INT NOT NULL,
   id_client INT NOT NULL,
   PRIMARY KEY(id_intervention),
   UNIQUE(id_client),
   FOREIGN KEY(id_pompe_a_chaleur) REFERENCES pompe_a_chaleur(id_pompe_a_chaleur),
   FOREIGN KEY(id_personnel) REFERENCES personnel(id_personnel),
   FOREIGN KEY(id_motif) REFERENCES motif(id_motif),
   FOREIGN KEY(id_client) REFERENCES client(id_client)
);

CREATE TABLE commande(
   num_commande INT AUTO_INCREMENT,
   prix_cmd DECIMAL(15,2),
   date_cmd DATE,
   id_ligne_de_commande INT NOT NULL,
   id_client INT NOT NULL,
   PRIMARY KEY(num_commande),
   FOREIGN KEY(id_ligne_de_commande) REFERENCES ligne_de_commande(id_ligne_de_commande),
   FOREIGN KEY(id_client) REFERENCES client(id_client)
);

CREATE TABLE parraine(
   id_client INT,
   id_filleul INT,
   PRIMARY KEY(id_client, id_filleul),
   FOREIGN KEY(id_client) REFERENCES client(id_client),
   FOREIGN KEY(id_filleul) REFERENCES filleul(id_filleul)
);

INSERT INTO client (adresse, nom_client, prenom_client, telephone) VALUES
('12 rue des Lilas', 'Dupont', 'Marie', '0612345678'),
('5 avenue Victor Hugo', 'Martin', 'Lucas', '0623456789'),
('8 chemin des Fleurs', 'Bernard', 'Sophie', '0634567890'),
('22 place de la République', 'Lefevre', 'Julien', '0645678901');

INSERT INTO filleul (nom_filleul) VALUES
('Durand'),
('Petit'),
('Deschamps'),
('Moreau');

INSERT INTO modele (nom_modele, marque) VALUES
('EcoHeat 3000', 'Daikin'),
('ThermoPlus X', 'Mitsubishi'),
('AirConfort S', 'Panasonic'),
('ClimaPro 500', 'Hitachi');

INSERT INTO poste (libelle_poste, id_poste) VALUES
('Technicien', '1'),
('Commercial', '2'),
('Installateur', '3');

INSERT INTO motif (id_motif, libelle_motif) VALUES
(1, 'Maintenance'),
(2, 'Réparation'),
(3, 'Contrôle annuel');

INSERT INTO pompe_a_chaleur (puissance, eff_energie, classe_energie, temp_fonctionnement_cel, volume_chauffe, eff_saison, dimensions, prix_pac, id_modele) VALUES
(12.5, 3.8, 'A++', -5, 250.00, 4.1, '100x80x50', 4500.00, 1),
(15.0, 4.2, 'A+++', -10, 300.00, 4.6, '110x85x55', 5200.00, 2),
(10.0, 3.5, 'A+', -3, 200.00, 3.9, '95x75x45', 3900.00, 3),
(18.0, 4.5, 'A+++', -15, 400.00, 4.8, '120x90x60', 6500.00, 4);

INSERT INTO personnel (id_personnel, nom_personnel, id_poste) VALUES
(1, 'Durand', 1),
(2, 'Lemoine', 2),
(3, 'Chevalier', 3);

INSERT INTO ligne_de_commande (date_livraison, quantite, id_pompe_a_chaleur) VALUES
('2025-01-12', 2, 1),
('2025-02-05', 1, 2),
('2025-03-18', 3, 3),
('2025-04-22', 1, 4);

INSERT INTO commande (prix_cmd, date_cmd, id_ligne_de_commande, id_client) VALUES
(9000.00, '2025-01-10', 1, 1),
(5200.00, '2025-02-01', 2, 2),
(11700.00, '2025-03-15', 3, 3),
(6500.00, '2025-04-20', 4, 4);

INSERT INTO intervention (date_inter, id_pompe_a_chaleur, id_personnel, id_motif, id_client) VALUES
('2025-01-20', 1, 1, 1, 1),
('2025-02-15', 2, 2, 2, 2),
('2025-03-22', 3, 3, 3, 3),
('2025-04-25', 4, 1, 2, 4);

INSERT INTO parraine (id_client, id_filleul) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4);

SELECT client.id_client, nom_client, prenom_client, num_commande, date_cmd, prix_cmd
FROM client
JOIN commande ON client.id_client = commande.id_client;

SELECT id_ligne_de_commande, date_livraison, quantite, ligne_de_commande.id_pompe_a_chaleur, nom_modele, marque, prix_pac
FROM ligne_de_commande
JOIN pompe_a_chaleur ON ligne_de_commande.id_pompe_a_chaleur = pompe_a_chaleur.id_pompe_a_chaleur
JOIN modele ON pompe_a_chaleur.id_modele = modele.id_modele;

SELECT id_intervention, date_inter, nom_personnel AS technicien, libelle_motif AS motif, nom_client, prenom_client
FROM intervention
JOIN personnel ON intervention.id_personnel = personnel.id_personnel
JOIN motif ON intervention.id_motif = motif.id_motif
JOIN client  ON intervention.id_client = client.id_client;

SELECT client.nom_client AS parrain, client.prenom_client, filleul.nom_filleul AS filleul
FROM parraine
JOIN client ON parraine.id_client= client.id_client
JOIN filleul ON parraine.id_filleul = filleul.id_filleul;



F EXISTS client;
DROP TABLE IF EXISTS personnel;
DROP TABLE IF EXISTS poste;
DROP TABLE IF EXISTS pompe_a_chaleur;
DROP TABLE IF EXISTS modele;
DROP TABLE IF EXISTS motif;


CREATE TABLE client(
   id_client INT AUTO_INCREMENT,
   adresse VARCHAR(50),
   nom_client VARCHAR(50),
   prenom_client VARCHAR(50),
   telephone VARCHAR(10),
   PRIMARY KEY(id_client)
);

CREATE TABLE filleul(
   id_filleul INT AUTO_INCREMENT,
   nom_filleul VARCHAR(50),
   PRIMARY KEY(id_filleul)
);

CREATE TABLE modele(
   id_modele INT AUTO_INCREMENT,
   nom_modele VARCHAR(50),
   marque VARCHAR(50),
   PRIMARY KEY(id_modele)
);

CREATE TABLE poste(
   id_poste INT AUTO_INCREMENT,
   libelle_poste VARCHAR(50),
   PRIMARY KEY(id_poste)
);

CREATE TABLE motif(
   id_motif INT AUTO_INCREMENT,
   libelle_motif VARCHAR(50),
   PRIMARY KEY(id_motif)
);

CREATE TABLE pompe_a_chaleur(
   id_pompe_a_chaleur INT AUTO_INCREMENT,
   puissance DECIMAL(15,2),
   eff_energie DECIMAL(15,2),
   classe_energie VARCHAR(10),
   temp_fonctionnement_cel INT,
   volume_chauffe DECIMAL(15,2),
   eff_saison DECIMAL(15,2),
   dimensions VARCHAR(50),
   prix_pac DECIMAL(15,2),
   id_modele INT NOT NULL,
   PRIMARY KEY(id_pompe_a_chaleur),
   FOREIGN KEY(id_modele) REFERENCES modele(id_modele)
);

CREATE TABLE personnel(
   id_personnel INT AUTO_INCREMENT,
   nom_personnel VARCHAR(50),
   id_poste INT NOT NULL,
   PRIMARY KEY(id_personnel),
   FOREIGN KEY(id_poste) REFERENCES poste(id_poste)
);

CREATE TABLE ligne_de_commande(
   id_ligne_de_commande INT AUTO_INCREMENT,
   date_livraison DATE,
   quantite INT,
   id_pompe_a_chaleur INT NOT NULL,
   PRIMARY KEY(id_ligne_de_commande),
   FOREIGN KEY(id_pompe_a_chaleur) REFERENCES pompe_a_chaleur(id_pompe_a_chaleur)
);

CREATE TABLE intervention(
   id_intervention INT AUTO_INCREMENT,
   date_inter DATE,
   id_pompe_a_chaleur INT NOT NULL,
   id_personnel INT NOT NULL,
   id_motif INT NOT NULL,
   id_client INT NOT NULL,
   PRIMARY KEY(id_intervention),
   UNIQUE(id_client),
   FOREIGN KEY(id_pompe_a_chaleur) REFERENCES pompe_a_chaleur(id_pompe_a_chaleur),
   FOREIGN KEY(id_personnel) REFERENCES personnel(id_personnel),
   FOREIGN KEY(id_motif) REFERENCES motif(id_motif),
   FOREIGN KEY(id_client) REFERENCES client(id_client)
);

CREATE TABLE commande(
   num_commande INT AUTO_INCREMENT,
   prix_cmd DECIMAL(15,2),
   date_cmd DATE,
   id_ligne_de_commande INT NOT NULL,
   id_client INT NOT NULL,
   PRIMARY KEY(num_commande),
   FOREIGN KEY(id_ligne_de_commande) REFERENCES ligne_de_commande(id_ligne_de_commande),
   FOREIGN KEY(id_client) REFERENCES client(id_client)
);

CREATE TABLE parraine(
   id_client INT,
   id_filleul INT,
   PRIMARY KEY(id_client, id_filleul),
   FOREIGN KEY(id_client) REFERENCES client(id_client),
   FOREIGN KEY(id_filleul) REFERENCES filleul(id_filleul)
);

INSERT INTO client (adresse, nom_client, prenom_client, telephone) VALUES
('12 rue des Lilas', 'Dupont', 'Marie', '0612345678'),
('5 avenue Victor Hugo', 'Martin', 'Lucas', '0623456789'),
('8 chemin des Fleurs', 'Bernard', 'Sophie', '0634567890'),
('22 place de la République', 'Lefevre', 'Julien', '0645678901');

INSERT INTO filleul (nom_filleul) VALUES
('Durand'),
('Petit'),
('Deschamps'),
('Moreau');

INSERT INTO modele (nom_modele, marque) VALUES
('EcoHeat 3000', 'Daikin'),
('ThermoPlus X', 'Mitsubishi'),
('AirConfort S', 'Panasonic'),
('ClimaPro 500', 'Hitachi');

INSERT INTO poste (libelle_poste, id_poste) VALUES
('Technicien', '1'),
('Commercial', '2'),
('Installateur', '3');

INSERT INTO motif (id_motif, libelle_motif) VALUES
(1, 'Maintenance'),
(2, 'Réparation'),
(3, 'Contrôle annuel');

INSERT INTO pompe_a_chaleur (puissance, eff_energie, classe_energie, temp_fonctionnement_cel, volume_chauffe, eff_saison, dimensions, prix_pac, id_modele) VALUES
(12.5, 3.8, 'A++', -5, 250.00, 4.1, '100x80x50', 4500.00, 1),
(15.0, 4.2, 'A+++', -10, 300.00, 4.6, '110x85x55', 5200.00, 2),
(10.0, 3.5, 'A+', -3, 200.00, 3.9, '95x75x45', 3900.00, 3),
(18.0, 4.5, 'A+++', -15, 400.00, 4.8, '120x90x60', 6500.00, 4);

INSERT INTO personnel (id_personnel, nom_personnel, id_poste) VALUES
(1, 'Durand', 1),
(2, 'Lemoine', 2),
(3, 'Chevalier', 3);

INSERT INTO ligne_de_commande (date_livraison, quantite, id_pompe_a_chaleur) VALUES
('2025-01-12', 2, 1),
('2025-02-05', 1, 2),
('2025-03-18', 3, 3),
('2025-04-22', 1, 4);

INSERT INTO commande (prix_cmd, date_cmd, id_ligne_de_commande, id_client) VALUES
(9000.00, '2025-01-10', 1, 1),
(5200.00, '2025-02-01', 2, 2),
(11700.00, '2025-03-15', 3, 3),
(6500.00, '2025-04-20', 4, 4);

INSERT INTO intervention (date_inter, id_pompe_a_chaleur, id_personnel, id_motif, id_client) VALUES
('2025-01-20', 1, 1, 1, 1),
('2025-02-15', 2, 2, 2, 2),
('2025-03-22', 3, 3, 3, 3),
('2025-04-25', 4, 1, 2, 4);

INSERT INTO parraine (id_client, id_filleul) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4);

SELECT client.id_client, nom_client, prenom_client, num_commande, date_cmd, prix_cmd
FROM client
JOIN commande ON client.id_client = commande.id_client;

SELECT id_ligne_de_commande, date_livraison, quantite, ligne_de_commande.id_pompe_a_chaleur, nom_modele, marque, prix_pac
FROM ligne_de_commande
JOIN pompe_a_chaleur ON ligne_de_commande.id_pompe_a_chaleur = pompe_a_chaleur.id_pompe_a_chaleur
JOIN modele ON pompe_a_chaleur.id_modele = modele.id_modele;

SELECT id_intervention, date_inter, nom_personnel AS technicien, libelle_motif AS motif, nom_client, prenom_client
FROM intervention
JOIN personnel ON intervention.id_personnel = personnel.id_personnel
JOIN motif ON intervention.id_motif = motif.id_motif
JOIN client  ON intervention.id_client = client.id_client;

SELECT client.nom_client AS parrain, client.prenom_client, filleul.nom_filleul AS filleul
FROM parraine
JOIN client ON parraine.id_client= client.id_client
JOIN filleul ON parraine.id_filleul = filleul.id_filleul;



