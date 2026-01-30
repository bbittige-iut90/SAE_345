DROP TABLE IF EXISTS ligne_commande;
DROP TABLE IF EXISTS ligne_panier;
DROP TABLE IF EXISTS commande;
DROP TABLE IF EXISTS jeux_video;
DROP TABLE IF EXISTS utilisateur;
DROP TABLE IF EXISTS etat;
DROP TABLE IF EXISTS type_jeux_video;
DROP TABLE IF EXISTS console;


CREATE TABLE IF NOT EXISTS type_jeux_video (
    id_type_jeux_video INT AUTO_INCREMENT,
    libelle_type_jeux_video VARCHAR(255),
    PRIMARY KEY (id_type_jeux_video)
);

CREATE TABLE IF NOT EXISTS console (
    id_console INT AUTO_INCREMENT,
    libelle_console VARCHAR(255),
    capacité_stockage_Go INT,
    pays_origine VARCHAR(255),

    PRIMARY KEY (id_console)
);

CREATE TABLE IF NOT EXISTS jeux_video (
    id_jeux_video INT AUTO_INCREMENT,
    nom_jeux_video VARCHAR(255),
    description VARCHAR(255),
    prix_jeux_video INT,
    photo_jeux_video VARCHAR(255),
    stock INT,
    condition_jeux_video VARCHAR(255),
    pegi VARCHAR(2),
    editeur  VARCHAR(255),
    type_jeux_video_id INT,
    console_id INT,

    PRIMARY KEY (id_jeux_video),
    FOREIGN KEY (type_jeux_video_id) REFERENCES type_jeux_video(id_type_jeux_video),
    FOREIGN KEY (console_id) REFERENCES console(id_console)
);

CREATE TABLE IF NOT EXISTS utilisateur (
   id_utilisateur INT AUTO_INCREMENT,
   login VARCHAR(255) NOT NULL,
   email VARCHAR(255) NOT NULL,
   nom VARCHAR(255),
   password VARCHAR(255) NOT NULL,
   role VARCHAR(255),
   est_actif tinyint(1),

   PRIMARY KEY(id_utilisateur)
);

CREATE TABLE IF NOT EXISTS etat (
    id_etat INT AUTO_INCREMENT,
    libelle_etat VARCHAR(255),

    PRIMARY KEY (id_etat)
);

CREATE TABLE IF NOT EXISTS commande (
    id_commande INT AUTO_INCREMENT,
    date_commande DATE,
    utilisateur_id INT,
    etat_id INT,

    PRIMARY KEY (id_commande),
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id_utilisateur),
    FOREIGN KEY (etat_id) REFERENCES etat(id_etat)
);

CREATE TABLE IF NOT EXISTS ligne_commande (
    commande_id INT,
    jeux_video_id INT,
    prix, INT
    quantite INT,

    PRIMARY KEY (commande_id, jeux_video_id),
    FOREIGN KEY (commande_id) REFERENCES commande(id_commande),
    FOREIGN KEY (jeux_video_id) REFERENCES jeux_video(id_jeux_video)
);

CREATE TABLE IF NOT EXISTS ligne_panier (
    utilisateur_id INT,
    jeux_video_id INT,
    quantite INT,
    date_ajout DATE

    PRIMARY KEY (utilisateur_id, jeux_video_id),
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id_utilisateur),
    FOREIGN KEY (jeux_video_id) REFERENCES jeux_video(id_jeux_video)
);

INSERT INTO utilisateur(id_utilisateur,login,email,password,role,nom,est_actif) VALUES
(1,'admin','admin@admin.fr',
    'pbkdf2:sha256:1000000$eQDrpqICHZ9eaRTn$446552ca50b5b3c248db2dde6deac950711c03c5d4863fe2bd9cef31d5f11988',
    'ROLE_admin','admin','1'),
(2,'client','client@client.fr',
    'pbkdf2:sha256:1000000$jTcSUnFLWqDqGBJz$bf570532ed29dc8e3836245f37553be6bfea24d19dfb13145d33ab667c09b349',
    'ROLE_client','client','1'),
(3,'client2','client2@client2.fr',
    'pbkdf2:sha256:1000000$qDAkJlUehmaARP1S$39044e949f63765b785007523adcde3d2ad9c2283d71e3ce5ffe58cbf8d86080',
    'ROLE_client','client2','1');

INSERT INTO type_jeux_video (id_type_jeux_video,libelle_type_jeux_video) VALUES
(NULL, 'Action'), (NULL,'Plateforme'),(NULL,'Tir'),
(NULL,'Aventure'),(NULL,'Action-Aventure'),(NULL,'RPG'),
(NULL,'Relfexion'),(NULL,'Simulation'),(NULL,'Stratégie'),
(NULL,'Jeux de rythme'),(NULL,'Party game'),(NULL, 'Course');

INSERT INTO console (id_console, libelle_console, capacité_stockage_Go, pays_origine) VALUES
(NULL,'Playstation 5',825,'Japon'),
(NULL,'Xbox One',500,'États-Unis'),
(NULL,'Nintendo Switch',32,'Japon'),
(NULL,'Nintendo Wii U',16,'Japon'),
(NULL,'Nintendo 3DS',16,'Japon'),
(NULL,'Wii',8,'Etats-Unis'),
(NULL,'Playstation 3',12,'Japon'),
(NULL,'XBox 360',12,'Japon'),
(NULL,'Nintendo Gamecube',1,'Japon');

INSERT INTO jeux_video (id_jeux_video, nom_jeux_video, description, prix_jeux_video, photo_jeux_video, stock, condition_jeux_video, pegi, editeur, type_jeux_video_id, console_id)  VALUES
-- PS5
(NULL,'Elden Ring','Voyage au sein de l''Entre-terre',60,'elden_ring_ps5.jpg',6,'neuf','16','FromSoftware',6,1),
(NULL,'Mortal Kombat: Legacy Kollection','Compile plusieurs versions des quatre premiers jeux de combat d''arcade Mortal Kombat',48,'mortal_kombat_ps5.jpg',10,'neuf','18','Atari',1,1),
(NULL,'Sackboy: A Big Adventure','Sackboy de retour avec des mouvements en 3D isométrique',15,'sackboy_a_big_adventure.jpg',2,'occasion','3','Sumo Digital',2,1),
(NULL,'God of War Ragnarök','Ragnarök voit le joueur explorer chacun des neuf royaumes',70,'GoW_Ragnarok_ps5.jpg',8,'neuf','18','Sony',5,1),
(NULL,'Assassin''s Creed Valhalla','On suit Eivor Varinsdottir, une guerrière viking qui cherche à s''établir en Angleterre',70,'ac_valhalla_ps5.jpg',5,'neuf','18','Ubisoft',5,1),
-- XBOX ONE
(NULL,'Elden Ring','Voyage au sein de l''Entre-terre',60,'elden_ring_xboxone.jpg',3,'neuf','16','FromSoftware',6,2),
(NULL,'Minecraft','Monde ouvert pour exprimer sa créativité',25,'minecraft_xboxone.jpg',12,'neuf','3','Mojang',4,2),
(NULL,'Assassin''s Creed Valhalla','Eivor Varinsdottir, une guerrière viking, cherche à s''établir en Angleterre',25,'ac_valhalla_xboxone.jpg',2,'occasion','18','Ubisoft',5,2),
(NULL,'Grand Theft Auto V','Trois protagonistes dans l''état de San Andreas ',30,'gtav_xboxone.jpg',7,'neuf','18','Rockstar',1,2),
-- SWITCH
(NULL,'Super Mario Odyssey','Mario et Cappy tentent d''empêcher le marriage de Bowser et Peach',50,'mario_odyssey.jpg',5,'neuf','7','Nintendo',2,3),
(NULL,'Splatoon 2','Guerre de peinture en solo ou en ligne',50,'splatoon_2.jpg',8,'neuf','7','Nintendo',3,3),
(NULL,'Animal Crossing: New Horizons','Simulation de capitalisme sur une île',45,'acnh.jpg',13,'neuf','3','Nintendo',8,3),
(NULL,'The Legend of Zelda: Breath of the Wild','Une mystérieuse voix vous guide afin d''éliminer Ganon, «Le Fléau»',25,'zelda_botw.jpg',2,'occasion','12','occasion',5,3),
-- WII U
(NULL,'Splatoon','Guerre de peinture en solo ou en ligne',20,'splatoon.jpg',4,'neuf','7','Nintendo',3,4),
(NULL,'Call of Duty Black Ops 2','Vivez la fin de la guerre froide',10,'cod_bo2_wiiu.jpg',2,'occasion','18','Treyarch',3,4),
(NULL,'New Super Mario Bros U','Sauvez la princesse sur Wii U',40,'nsmbu.jpg',1,'occasion','3','Nintendo',2,4),
(NULL,'Super Smash Bros for Wii U','Jeux de combat à la sauce Nintendo',40,'smash_bros_wiiu.jpg',2,'occasion','12','Nintendo',1,4),
-- 3DS
(NULL,'Yo-Kai Watch 3','Vivez les aventures de Nathan aux États-Unis',200,'ykw3.jpg',1,'occasion','7','Level-5',6,5),
(NULL,'Yo-Kai Watch 2','Vivez la suite des aventures de Nathan à Grandval',40,'ykw2.jpg',2,'occasion','7','Level-5',6,5),
(NULL,'Pokemon Soleil','Explorez la région d''Alola et attrapez les tous',50,'pkmn_soleil.jpg',2,'occasion','7','Nintendo',6,5),
(NULL,'One Piece: Unlimited Cruise SP','Revivez le voyage des Mugiwaras sur GrandLine',100,'opucsp.jpg',1,'occasion','12','Bandai Namco',4,5),
-- WII
(NULL,'Wii Sports Resort','La suite du Party Game le plus vendu de Nintendo',35,'wii_sports_resort.jpg',3,'occasion','7','Nintendo',11,6),
(NULL,'PokéPark Wii : La Grande Aventure de Pikachu','Découvrez le monde de Pokemon à travers les yeux d''un pokemon',40,'pokepark_wii.jpg',2,'occasion','3','Nintendo',5,6),
(NULL,'Mario Kart Wii','Jeux de course dans l''univers de Mario',45,'mk_wii.jpg',1,'occasion','3','Nintendo',12,6),
(NULL,'Dragon Ball Budokai Tenkachi 3','Le jeux ultime de combat Dragon Ball',70,'dbbt3.jpg',1,'occasion','12','Bandai Namco',1,6),
(NULL,'The Lapins Crétins : La Grosse Aventure','Comédie d''aventure, jeu vidéo d''action et d''aventure et de plates-formes',35,'tlp_lga.jpg',0,'occasion','7','Ubisoft',4,6),
-- PS3
(NULL,'God of War III','Kratos lance un assaut sur l''Olympe jusqu''à ce qu''il soit abandonné par Gaïa.',10,'gow3.jpg',1,'occasion','','Sony',5,7),
(NULL,'South Park : Le Bâton de la vérité','Basé sur la série d''animation américaine South Park,',35,'south_park.jpg',2,'occasion','18','Ubisoft',6,7),
(NULL,'Spider-Man 3','adaptation vidéoludique du film du même nom',40,'spiderman3.jpg',1,'occasion','12','Activision',1,7),
-- XBOX 360
(NULL,'Call of Duty Black Ops 2','Vivez la fin de la guerre froide',15,'cod_bo2_xbox360.jpg',1,'occasion','18','Treyarch',3,8),
(NULL,'Assassin''s Creed IV Black Flag','utiliser l''Animus et d''examiner les souvenirs de Desmond Miles et ses ancêtres',35,'ac_black_flag.jpg',2,'occasion','18','Ubisoft',5,8),
(NULL,'Dead Rising 2','Beat Them All à Las Vegas contre des zombies',22,'dead_rising2.jpg',1,'occasion','18','Capcom',1,8),
(NULL,'Saints Row: The Third','Le GTA-Like le plus déjanté',0,'saint_row3.jpg',1,'occasion','18','THQ',1,8),
-- GAMECUBE
(NULL,'Paper Mario : La Porte Millénaire','Le RPG Mario du peuple',100,'paper_mario_ttyd.jpg',1,'occasion','3','Nintendo',6,9),
(NULL,'Pokémon Colosseum','Ambiance sombre et son scénario plus mature',150,'pkmn_colosseum.jpg',1,'occasion','3','The Pokemon Compagny',6,9),
(NULL,'The Legend of Zelda: Twilight Princess','Un monstre emporte Link dans un monde corrompu par le crépuscule',130,'twilight_princess.jpg',1,'occasion','12','Nintendo',5,9),
(NULL,'The Legend of Zelda: The Wind Waker','Naviguez sur les mers pour sauver la princesse',80,'wind_waker.jpg',1,'occasion','7','Nintendo',5,9),
(NULL,'Mario Kart: Double Dash!!','Le copilote est fourni!',90,'mk_double_dash.jpg',1,'occasion','3','Nintendo',12,9),
(NULL,'Super Mario Sunshine','Découvrez Delphino Plazza avec Jet',40,'mario_sunshine.jpg',1,'occasion','3','Nintendo',2,9),
(NULL,'Super Smash Bros Melee','Jeux de combat à la sauce Nintendo',100,'smash_bros_melee.jpg',1,'occasion','3','Nintendo',1,9);