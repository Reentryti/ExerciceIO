# Exercice IODB

[![Django](https://img.shields.io/badge/Django-5.1-brightgreen)](https://www.djangoproject.com/)
[![Vue.js](https://img.shields.io/badge/Vue.js-3.3-green)](https://vuejs.org/)
[![AWS](https://img.shields.io/badge/AWS-EC2%2FS3-orange)](https://aws.amazon.com)

## 📌 Description
Application web [descript°] avec :
- **Backend** : Django REST Framework
- **Frontend** : Vue.js + Vite
- **Base de données** : MySQL
- **Stockage** : AWS S3
- **Sécurité** : Oauth2, Détection de plagiat
- **Visualisation de statistiques** : Chart.js

## 🌐 Accès au projet
### URLs de démonstration
| Service       | Lien                          | Identifiants (si besoin) |
|---------------|-------------------------------|--------------------------|
| Frontend      | http://[IP_EC2]:5173          | -                        |
| Backend       | http://[IP_EC2]:8000/         | -                        |
| Admin Django  | http://[IP_EC2]:8000/admin    |                          |

## 🛠️ Installation locale
### Prérequis
- Docker 23+
- Docker-Compose 2.20+

### Lancer le projet
```bash
git clone https://github.com/Reentryti/ExerciceIO
cd ExerciceIO
docker-compose up -d --build
