#################################################
#  Perception d'une balle jaune dans un Live    #
#################################################

#Réalisé par : Saigné Benjamin
#Date : 2025

#Remarque: - Détection automatique (aucune action requise)
#          - Cette algorithme ne fonctionne que sur les balles de couleur jaune

##################################################

#Importation des librairies :
import cv2
import numpy as np

def detect_ball(frame,positions):


    hauteur, largeur, _ = frame.shape

    Echelle = 2
    NouvelleLargeur = int(largeur / Echelle)
    NouvelleHauteur = int(hauteur / Echelle)

    Echelle_x = largeur / NouvelleLargeur
    Echelle_y = hauteur / NouvelleHauteur

    ImagePerception = cv2.resize(frame, (NouvelleLargeur, NouvelleHauteur))
    ImagePerception = cv2.cvtColor(ImagePerception, cv2.COLOR_BGR2HSV)
    ImagePerception[:, :, 2] = 255
    ImagePerception = cv2.cvtColor(ImagePerception, cv2.COLOR_HSV2BGR)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (14, 14))
    ImagePerception = cv2.erode(ImagePerception, kernel, iterations=1)
    ImagePerception = cv2.dilate(ImagePerception, kernel, iterations=1)

    ImagePerception = cv2.cvtColor(ImagePerception, cv2.COLOR_BGR2HSV)
    lower_H = np.array([15, 0, 255])
    upper_H = np.array([60, 255, 255])
    mask = cv2.inRange(ImagePerception, lower_H, upper_H)
    ImagePerception = cv2.bitwise_and(ImagePerception, ImagePerception, mask=mask)
    ImagePerception = cv2.erode(ImagePerception, kernel, iterations=1)
    ImagePerception = cv2.dilate(ImagePerception, kernel, iterations=1)

    ImagePerception = cv2.cvtColor(ImagePerception, cv2.COLOR_HSV2BGR)
    ImagePerception = cv2.cvtColor(ImagePerception, cv2.COLOR_BGR2GRAY)
    ImagePerception = cv2.GaussianBlur(ImagePerception, (3, 3), 2)

    _, ImagePerception = cv2.threshold(ImagePerception, 127, 255, cv2.THRESH_TOZERO)
    cv2.imshow('Detection2 Balle', ImagePerception)

    circles = cv2.HoughCircles(
        image=ImagePerception,
        method=cv2.HOUGH_GRADIENT,
        dp=1.2,
        minDist=200,
        param1=100,
        param2=20,
        minRadius=15,
        maxRadius=100
    )

    DistanceMinEntreDeuxDetection = 50
    NombreDetectionReussiAvantAffichage = 3  

    if circles is not None:
        circles = np.uint16(np.around(circles))
        x, y, r = circles[0][0]

        x = int(x * Echelle_x)
        y = int(y * Echelle_y)
        r = int(r * ((Echelle_x + Echelle_y) / 2))

        positions.append((x, y))
        if len(positions) > 3:
            positions.pop(0)

        if len(positions) == 3:
            x0, y0 = positions[0]
            x1, y1 = positions[1]
            x2, y2 = positions[2]

            dist1 = np.sqrt((x1 - x0)**2 + (y1 - y0)**2)
            dist2 = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        else :
            dist1=200
            dist2=200

        if dist1 < 50 and dist2 < 50:
            cv2.circle(frame, (x, y), r, (0, 255, 0), 2)
            cv2.circle(frame, (x, y), 2, (0, 0, 255), 3)
            print(f"Balle détectée en : x={x}, y={y}, r={r}")
        else:
            print(f"Balle instable")
    else:
        print("Aucune balle détectée")

    return frame,positions


if __name__ == "__main__":

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Erreur : Impossible d'accéder à la webcam.")
        exit() #Quitter le programme

    #Initialisation détection précédente:
    positions = []

    while True:

        ret, frame = cap.read()
        if not ret:
            print("Erreur de lecture de la webcam.")
            break

        resultat,positions = detect_ball(frame,positions)
        cv2.imshow('PerceptionBalle', resultat)

        if cv2.waitKey(1) & 0xFF == ord('q'): #Arrêt détection
            break

    cap.release()
    cv2.destroyAllWindows()