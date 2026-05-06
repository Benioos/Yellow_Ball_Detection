#################################################
#  Perception d'une balle jaune dans une vidéo  #
#################################################

#Réalisé par : Saigné Benjamin
#Date : 2025

#Remarque: - Détection automatique (aucune action requise)
#          - Cette algorithme ne fonctionne que sur les balles de couleur jaune

##################################################

#Importation des librairies :
import cv2
import numpy as np
import time

#Chemin d'accès Vidéo :  
video_path = 'balle.mp4'

#Fonction de détection :
def detect_ball(frame):

    if not hasattr(detect_ball, "prev_center"):
        detect_ball.prev_center = None  


    Hauteur, Largeur, canaux = frame.shape

    Echelle = 4
    NoubelleLargeur = int(Largeur / Echelle)
    NouvelleHauteur = int(Hauteur / Echelle)
    ImagePerception = cv2.resize(frame, (NoubelleLargeur, NouvelleHauteur))


    ImagePerception = cv2.cvtColor(ImagePerception, cv2.COLOR_BGR2HSV)
    ImagePerception[:, :, 2] = 255
    ImagePerception = cv2.cvtColor(ImagePerception, cv2.COLOR_HSV2BGR)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (14, 14))
    ImagePerception = cv2.erode(ImagePerception, kernel, iterations=1)
    ImagePerception = cv2.dilate(ImagePerception, kernel, iterations=1)

    ImagePerception = cv2.cvtColor(ImagePerception, cv2.COLOR_BGR2HSV)

    lower_H = np.array([12, 0, 255])
    upper_H = np.array([50, 255, 255])
    mask = cv2.inRange(ImagePerception, lower_H, upper_H)
    ImagePerception = cv2.bitwise_and(ImagePerception, ImagePerception, mask=mask)

    ImagePerception = cv2.erode(ImagePerception, kernel, iterations=1)
    ImagePerception = cv2.dilate(ImagePerception, kernel, iterations=1)

    ImagePerception = cv2.cvtColor(ImagePerception, cv2.COLOR_HSV2BGR)
    ImagePerception = cv2.cvtColor(ImagePerception, cv2.COLOR_BGR2GRAY)

    ImagePerception = cv2.GaussianBlur(ImagePerception, (3, 3), 2)
    ret, ImagePerception = cv2.threshold(ImagePerception, 127, 255, cv2.THRESH_TOZERO)

    circles = cv2.HoughCircles(
        image=ImagePerception,
        method=cv2.HOUGH_GRADIENT,
        dp=1.2,
        minDist=200,
        param1=100,
        param2=20,
        minRadius=10,
        maxRadius=700
    )

    if circles is not None:

        circles = np.uint16(np.around(circles))
        x, y, r = circles[0][0]

        scale_x = Largeur / NoubelleLargeur
        scale_y = Hauteur / NouvelleHauteur

        x = int(x * scale_x)
        y = int(y * scale_y)
        r = int(r * ((scale_x + scale_y) / 2))

        CercleDessin = False
        if detect_ball.prev_center is None:
            CercleDessin = True
        else:
            x_prev, y_prev = detect_ball.prev_center
            distance = np.sqrt((x - x_prev)**2 + (y - y_prev)**2)
            DistanceMinDetection = 50
            if distance <= DistanceMinDetection:
                CercleDessin = True

        if CercleDessin:
            cv2.circle(frame, (x, y), r, (0, 255, 0), 2)
            cv2.circle(frame, (x, y), 2, (0, 0, 255), 3)
            detect_ball.prev_center = (x, y)
            print(f"Centre Cercle : x={x}, y={y}. Rayon : r={r}")
    else:
        print("Aucune balle détectée")

    return frame


if __name__ == "__main__":

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Erreur : Impossible d'ouvrir la vidéo.")
        exit() #Arrêt du programme 

    #Fonctionnalité FPS : 
    NbreFPSVideoOriginal = cap.get(cv2.CAP_PROP_FPS)
    if NbreFPSVideoOriginal <= 0:
        NbreFPSVideoOriginal = 30 #Défaut

    DureeFrame = 1.0 / NbreFPSVideoOriginal
    print(NbreFPSVideoOriginal)
    #Détection en boucle :
    while True:
        TempsDebFrame = time.time()

        ret, frame = cap.read()
        if not ret:
            break

        resultat = detect_ball(frame) #Détection de la balle
        
        # Synchronisation avec la cadence d’origine
        TempsEcoulerDepuisDernierAffichage = time.time() - TempsDebFrame
        Synchro = DureeFrame - TempsEcoulerDepuisDernierAffichage
        if Synchro > 0:
            time.sleep(Synchro)

        TempsTraitement = time.time() - TempsDebFrame
        FPSActuelle = 1.0 / max(TempsTraitement, 1e-6) #Évite la division par zéro
        cv2.putText(resultat, f"FPS : {int(FPSActuelle)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2) #Affichage des FPS
        cv2.imshow('PerceptionImage', resultat)

        if cv2.waitKey(1) & 0xFF == ord('q'): #Quitter détection
            break

    cap.release()
    cv2.destroyAllWindows()
