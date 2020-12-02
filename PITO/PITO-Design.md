# TP Architecture Distribué

## Architecture

![Features](static/schema_archi.png)

## Stack technique

### Front-end : JavaScript + HTML + CSS

### Back-end : Python

Bibliothèque : flask, request, sqlalchemy

Storage : Base de donné sqlLite

## End point

127.0.0.1:8080/vols/ : listes de tous les vols

127.0.0.1:8080/vols/<boolean:vol_reservation> : liste des vols réservés

127.0.0.1:8080/vols/<name:user_name> : liste des vols réservés à mon nom

127.0.0.1:8080/vols/<id:name> : Post sur le billet avec l'id correspondant on change alors la valeur de la réservation à true et le nom de l'utilisateur 

## Modèle de donnée

Billet :

- Int : ID
- Datetime : Date d'entrée dans l'api
- Boolean : Reservation
- String : Code de départ 
- String : Code de destination
- Int : Prix
- String : User name
