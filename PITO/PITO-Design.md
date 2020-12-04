# TP Architecture Distribué

## Architecture

![Features](static/schema_archi.png)
https://github.com/sintcha/tp-architecture/blob/IAD-PITO/static/schema_archi.png

## Stack technique

### Front-end : JavaScript + HTML + CSS

### Back-end : Python

Bibliothèque : flask, request, sqlalchemy

Storage : Base de donné sqlLite

## End point

127.0.0.1:5000/Ticket/<int:Ticket_id> : Post sur le billet avec l'id correspondant on change alors la valeur de la réservation à true et le nom de l'utilisateur

127.0.0.1:5000/Tickets: liste de tous les billets

127.0.0.1:5000/Ticket_id/<int:billet_id>: Afficher le billet avec l'id spécifié

127.0.0.1:5000/Ticket_departure/<string:code_depart>: liste des billets avec le le lieu de départ spécifié

127.0.0.1:5000/Ticket_destination/<string:code_destination>: liste des billets avec le lieu d'arrivée spécifié

127.0.0.1:5000/Ticket_entree_api/<string:date_entree_api>: liste des billets ajoutés dans l'api à la date correspondante

127.0.0.1:5000/Ticket_departure_date/<string:date_departure>: liste des billets pour un départ à la date spécifiée

127.0.0.1:5000/Ticket_arrival_date/<string:date_arrival>:liste des billets pour une arrivée à la date spécifiée

127.0.0.1:5000/Ticket_price/<string:price>: liste des billets selon le prix spécifié

## Modèle de donnée

Billet :

- Int : ID
- Datetime : Date d'entrée dans l'api
- Datetime : Date de départ du vol
- Datetime : Date d'arrivée du vol
- Boolean : Reservation
- String : Code de départ 
- String : Code de destination
- Int : Prix
- String : User name
