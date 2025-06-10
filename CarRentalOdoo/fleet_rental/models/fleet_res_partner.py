from odoo import models, fields, api
from odoo.exceptions import ValidationError
import hashlib
from werkzeug.security import generate_password_hash



class ResPartner(models.Model):
    _inherit = 'res.partner'

    identity_card_picture = fields.Binary(string='Carte d\'identité')
    drivers_license_picture = fields.Binary(string='Permis de conduire')
    is_locataire = fields.Boolean(string='is_Locataire')
    is_assurance = fields.Boolean(string='is_Assurance')
    is_conducteur = fields.Boolean(string='is_Conducteur' )

    
    driver_license_number = fields.Char(string='Numéro de permis de conduire')
    x_trade_register = fields.Char(string='Registre de commerce')
    x_date_of_birth = fields.Date(string='Date de naissance')
    x_place_of_birth = fields.Char(string='Lieu de naissance')
    cin_number = fields.Char(string='Numéro CIN')
    x_cin_issue_date = fields.Date(string='CIN Délivrée le')
    x_license_issue_date = fields.Date(string='Permis délivré le')
    x_license_category = fields.Char(string='Permis catégorie')
    profile_pic = fields.Binary(string='Photo de profil')
    password = fields.Char(string='mot de passe')


    @api.model
    def create(self, vals):
        # Fields to validate for uniqueness
        unique_fields = ['email', 'mobile', 'cin_number', 'driver_license_number', 'x_trade_register']
        for field_name in unique_fields:
            if field_name in vals and vals[field_name]:
                existing_partner = self.search([(field_name, '=', vals[field_name])], limit=1)
                if existing_partner:
                    raise ValidationError(f"The {field_name.replace('_', ' ')} '{vals[field_name]}' is already in use.")

        # Hash the password before saving it
        if 'password' in vals:
            vals['password'] = generate_password_hash(vals['password'])

        return super(ResPartner, self).create(vals)

    def write(self, vals):
        # Fields to validate for uniqueness
        unique_fields = ['email', 'mobile', 'cin_number', 'driver_license_number', 'x_trade_register']

        for field_name in unique_fields:
            if field_name in vals and vals[field_name]:
                existing_partner = self.search([
                    (field_name, '=', vals[field_name]),
                    ('id', '!=', self.id)  # Exclude the current record
                ], limit=1)
                if existing_partner:
                    raise ValidationError(f"The {field_name.replace('_', ' ')} '{vals[field_name]}' is already in use.")

        # Hash the password before saving it
        if 'password' in vals:
            vals['password'] = generate_password_hash(vals['password'])

        return super(ResPartner, self).write(vals)

