# 🟡 Détection & Perception de Balle Jaune (OpenCV)

Ce projet réalise la détection et le suivi automatique de balles jaunes sur **images statiques**, **fichiers vidéo** et **flux webcam en direct** à l'aide de **Python** et **OpenCV**.

---

## 🎯 Objectifs & Démarche Technique

L'objectif principal est d'extraire et de géolocaliser une balle de couleur jaune dans un environnement complexe tout en maintenant une exécution fluide en temps réel.

### Pipeline de Traitement d'Image :
1. **Conversion Colorimétrique (HSV) :** Passage du domaine BGR au domaine HSV. Contrairement au domaine RGB qui dépend fortement des variations d'éclairage et d'ombres, l'espace HSV permet d'isoler la teinte (*Hue*) indépendamment de la luminosité ($V$).
2. **Filtrage Morphologique :** Application d'opérations d'érosion et de dilatation (noyau elliptique) pour éliminer le bruit et homogénéiser la zone ciblée.
3. **Masquage Couleur :** Application d'un masque de seuillage (`cv2.inRange`) sur la plage de teinte jaune ($H \in [12, 60]$).
4. **Détection de Forme (Hough Circles) :** Passage en niveau de gris, lissage Gaussien et application de la transformée de Hough circulaire (`cv2.HoughCircles`) pour valider la géométrie de l'objet.
5. **Filtrage Temporel & Stabilité (Vidéo/Live) :** Vérification de la continuité spatiale sur plusieurs frames consécutives pour éviter les faux positifs.

---

## ⚡ Optimisations de Performance

Lors du traitement vidéo, l'exécution frame par frame à haute résolution ralentit le flux. Pour maintenir une cadence fluide :
- **Sous-échantillonnage spatial (Downscaling) :** Redimensionnement de l'image (facteur $\times 4$ en vidéo, $\times 2$ en flux live) avant le calcul, puis projection des coordonnées sur la résolution d'origine.
- **Synchronisation FPS :** Calcul dynamique du temps de traitement par image pour respecter le framerate d'origine de la vidéo (`Video_Balle.mp4`).

---

## 📁 Structure du Projet

```text
.
├── Perception_Image.py               # Script de détection sur image statique (clic manuel)
├── Perception_Video.py               # Script de détection sur fichier vidéo avec synchro FPS
├── Perception_Live.py                # Script de détection en temps réel via webcam
├── Video_Balle.mp4                   # Vidéo de test
├── Balle_Base_Grand.jpg              # Image de test (grand format)
├── Balle_Base_Petite.jpg             # Image de test (petit format)
├── Balle_Main.jpg                    # Image de test (balle tenue en main)
├── Balle_Multiple.jpg                # Image de test (plusieurs balles)
├── Balle_Ombre.jpg                   # Image de test (avec zones d'ombre)
├── Balle_Simple.jpg                  # Image de test (environnement simple)
└── Benjamin Saigné Rapport Perception.pdf  # Rapport de projet complet
