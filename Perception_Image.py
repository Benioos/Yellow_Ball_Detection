#################################################
#  Perception d'une balle jaune dans une image  #
#################################################

#Réalisé par : Saigné Benjamin
#Date : 2025

#Remarque: - Clic gauche pour lancer la détection
#          - Cette algorithme ne fonctionne que sur les balles de couleur jaune

##################################################

#Importation des librairies :
import cv2
import numpy as np

#Chemin d'accès Image : 
path = 'balle_small.jpg'


#Fonction de détection :
def Detection(event, x, y, flags, params):

    if event == cv2.EVENT_LBUTTONDOWN:

        ImagePerception=image.copy()

        ImagePerception = cv2.cvtColor(ImagePerception, cv2.COLOR_BGR2HSV)       
        ImagePerception[:, :, 2] = 255   
        #cv2.imshow('ImageTraiter0', ImagePerception) #Débeuggage                       
        ImagePerception = cv2.cvtColor(ImagePerception, cv2.COLOR_HSV2BGR)     
             
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (28, 28))
        ImagePerception = cv2.erode(ImagePerception, kernel, iterations=2)
        ImagePerception = cv2.dilate(ImagePerception, kernel, iterations=2)
        #cv2.imshow('ImageTraiter1', ImagePerception) #Débeuggage

        ImagePerception = cv2.cvtColor(ImagePerception, cv2.COLOR_BGR2HSV)
        H_Low = np.array([15, 0, 255])       
        H_High = np.array([38, 255, 255])    
        masque = cv2.inRange(ImagePerception, H_Low, H_High)
        ImagePerception= cv2.bitwise_and(ImagePerception, ImagePerception, mask=masque)
        #cv2.imshow('ImageTraiter6', ImagePerception) #Débeuggage

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (20, 20))
        ImagePerception = cv2.erode(ImagePerception, kernel, iterations=4)
        ImagePerception = cv2.dilate(ImagePerception, kernel, iterations=4)
        #cv2.imshow('ImageTraiter4', ImagePerception) #Débeuggage

        ImagePerception = cv2.cvtColor(ImagePerception, cv2.COLOR_HSV2BGR)
        ImagePerception = cv2.cvtColor(ImagePerception, cv2.COLOR_BGR2GRAY)
        #cv2.imshow('ImageTraiter5', ImagePerception) #Débeuggage

        ImagePerception = cv2.GaussianBlur(ImagePerception, (3, 3), 2)
        _,ImagePerception = cv2.threshold(ImagePerception,127,255,cv2.THRESH_TOZERO)
        #cv2.imshow('ImageTraiter3', ImagePerception) #Débeuggage
        
        circles = cv2.HoughCircles(image=ImagePerception,method=cv2.HOUGH_GRADIENT,dp=1.2,minDist=200,param1=100,param2=20,minRadius=10,maxRadius=600)

        #Représentation des cercles détectés:
        ImageFin = image.copy()

        if circles is not None:
            circles = np.uint16(np.around(circles))
            for (x, y, r) in circles[0, :]:
                cv2.circle(ImageFin, (x, y), r, (0, 255, 0), 3)  
                cv2.circle(ImageFin, (x, y), 2, (0, 0, 255), 3)  
                print(f"Centre cercle : x={x}, y={y}. Et rayon : r={r}")
        else:
            print("Aucune balle détectée")            
        cv2.imshow('ResultatFinal', ImageFin) #Apperçu du résultat final


if __name__=="__main__":

    image = cv2.imread(path, cv2.IMREAD_COLOR)

    cv2.imshow('ImageDebut', image)

    cv2.setMouseCallback('ImageDebut', Detection)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()
