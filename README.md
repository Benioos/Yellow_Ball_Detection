# 🟡 Détection & Perception de Balle Jaune (OpenCV)

Ce projet réalise la détection et le suivi automatique de balles jaunes sur **images statiques**, **fichiers vidéo** et **flux webcam en direct** à l'aide de **Python** et **OpenCV**.

---

## 🎯 Objectifs & Démarche Technique

L'objectif principal est d'extraire et de géolocaliser une balle de couleur jaune dans un environnement complexe tout en maintenant une exécution fluide en temps réel.

### Pipeline de Traitement d'Image :
1. **Conversion Colorimétrique (HSV) :** Passage du domaine BGR au domaine HSV. Contrairement au domaine RGB qui dépend fortement des variations d'éclairage et d'ombres, l'espace HSV permet d'isoler la teinte (Hue) indépendamment de la luminosité ($V$).
2. **Filtrage Morphologique :** Application d'opérations d'érosion et de dilatation (noyau elliptique) pour éliminer le bruit et homogénéiser la zone ciblée.
3. **Masquage Couleur :** Application d'un masque de seuillage (`cv2.inRange`) sur la plage de teinte jaune ($H \in [12, 60]$).
4. **Détection de Forme (Hough Circles) :** Passage en niveau de gris, lissage Gaussien et application de la transformée de Hough circulaire (`cv2.HoughCircles`) pour valider la géométrie géométrique de l'objet.
5. **Filtrage Temporel & Stabilité (Vidéo/Live) :** Vérification de la continuité spatiale sur plusieurs frames consécutives pour éviter les faux positifs.

---

## ⚡ Optimisations de Performance

Lors du traitement vidéo, l'exécution frame par frame à haute résolution ralentit le flux. Pour maintenir une cadence fluide :
- **Sous-échantillonnage spatiale (Downscaling) :** Redimensionnement de l'image (facteur $\times 4$ en vidéo, $\times 2$ en flux live) avant le calcul, puis projection des coordonnées sur la résolution d'origine.
- **Synchronisation FPS :** Calcul dynamique du temps de traitement par image pour respecter le framerate d'origine de la vidéo.

---

## 📁 Structure du Projet

```text
.
├── image_detection.py      # Détection sur image statique au clic
├── video_detection.py      # Détection sur fichier vidéo avec synchro FPS
├── live_detection.py       # Détection en temps réel via la webcam
├── balle_small.jpg         # Image de test
└── balle.mp4               # Vidéo de test
