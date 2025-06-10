from odoo import models, fields, api
from odoo.exceptions import ValidationError

class FleetUser(models.Model):
    _inherit = 'res.users'  # Inheriting res.users to manage locataires

    # Locataire-specific fields
    cin_number = fields.Char(string="Numéro CIN", required=True, help="Numéro de la Carte d'Identité Nationale")
    cin_date = fields.Date(string="Date de Délivrance CIN", help="Date à laquelle la CIN a été délivrée")
    identity_card_picture = fields.Binary(string="Carte d'identité", help="Image de la Carte d'Identité")
    phone_number = fields.Char(string="Numéro de Téléphone", required=True)
    date_of_birth = fields.Date(string="Date de Naissance", help="Date de naissance du locataire")
    address = fields.Char(string="Adresse", help="Adresse du locataire")
    place_of_birth = fields.Char(string="Lieu de Naissance", help="Lieu de naissance du locataire")
    num_tva = fields.Char(string="Numéro TVA", help="Numéro d'identification fiscale du locataire")
    registre_commerce = fields.Char(string="Registre de Commerce", help="Numéro du registre de commerce")
    birth_place = fields.Char(string="Lieu de Naissance", help="Lieu exact de naissance")
    is_locataire = fields.Boolean(string="Is Locataire",  help="Mark this user as a locataire.")



