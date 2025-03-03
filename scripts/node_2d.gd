extends Node2D


var monnaie : int = 100
@onready var label = $Label
func _ready():
	update_monnaie()
func update_monnaie():
	label.text = "Monnaie : " + str(monnaie) + "pièces"
func ajouter_monnaie(montant : int):
	monnaie += montant
	update_monnaie()
	#Fonction pour ajouter ou retirer de la monnaie
func retirer_monnaie(montant : int):
	if monnaie >= montant:
		monnaie -= montant
		update_monnaie()
	else:
		print("Pas assez de monnaie ! ")
