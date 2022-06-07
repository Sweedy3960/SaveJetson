# SaveJetson

librairie Opencv 1.5.0  avec python 3.9 (Maj à faire -> python 3.10 = ajout de la structure Switch --> modification des elsif)





**// Sauvegarde de tout le travail fait //**
Approche du projet Eurobot 2021-22 
But final: Transmettre au robot aliées les positions de tout les robots et échantillons 
Intermédiaire: transmettre la position des robots 



**Gènéralité**
PCB: les différentes cartes

images: résultats

Save All : Fichier de sauvegarde principal

    myFi: fichier text, par exemple les calibrations,script pour vcmd ventilateur
    
    myPy: tout les codes : 
    
        Calib: différente version programme de calibrations 
        
        exampleTest: Aide mémoire avec structure et Démo VOIR https://pep8.org/
        
        Filtres: Code avec filtres d'images(Utilisé pour détéction de ligne)
        
        Fun: Cod eportes ouvertes (dessin à distance) utilisation d'ip cam 
        
        OLD: V1 à Vlast plusieurs aproches
        
        ServerTCP: différentre version d'un protocol "maison" TCPIP
        
        UndistStitch: Code pour corriger disctortion et sttching(assemblage par point de corélation)
        
        utils: rogramme de detection depuis une image, Capture de video pour 1 et 2 caméra, GETPIP,help(mettre le nom de la librairie ou cmd pour l'aide)
        
        ScriptFiles: script d'instalation de la librairie opencv et de ces dépendances(modifier version dans le script), script d'instalation de VSCode  

 -- Les sources sont dans le source.txt

**//todo://**
Test RenewV2 + débug
Modification sauvegarde des plans


=======
**Resultat:**
- Bat 20000mAh -> 1h =~10% -> 9h d'autonomie 
