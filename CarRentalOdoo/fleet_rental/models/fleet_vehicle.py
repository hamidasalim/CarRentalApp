from datetime import timedelta
from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class EmployeeFleet(models.Model):
    _inherit = 'fleet.vehicle'

    rental_check_availability = fields.Boolean(default=True, copy=False)
    car_pic = fields.Binary(string='Photo de voiture')


    # Additional Fields
    dernier_releve_kilometrique = fields.Float(string='Dernier relevé kilométrique')
    date_sortie = fields.Date(string='Date de sortie')
    enregistre_par = fields.Many2one('res.partner', string='Enregistré par')
    date_enregistrement = fields.Date(string='Date d\'enregistrement')
    agence_assurance = fields.Many2one('res.partner', string='Agence d\'assurance')
    modifie_par = fields.Many2one('res.partner', string='Modifié par')
    date_modification = fields.Date(string='Date de modification')
    garantie_jusqua = fields.Date(string='Garantie jusqu\'à')
    compte_revenus = fields.Many2one('account.account', string='Compte de revenus')
    compte_depenses = fields.Many2one('account.account', string='Compte de dépenses')
    premiere_date_contrat = fields.Date(string='Première date de contrat')
    tarif = fields.Float(string='Tarif')
    driver_mobile = fields.Char(string="Téléphone du conducteur", readonly=True)

    nbr_jour_alerte_assurance = fields.Float(string='Nombre de jour avant alerte', default=5.0)
    rental_reserved_time = fields.One2many('rental.fleet.reserved',
                                           'reserved_obj_id',
                                           string='Temps réservé',
                                           help='Temps de location réservé',
                                           readonly=1,
                                           ondelete='cascade')
    _sql_constraints = [('vin_sn_unique', 'unique (vin_sn)',
                         "Le numéro de châssis existe déjà !"),
                        ('license_plate_unique', 'unique (license_plate)',
                         "La plaque d'immatriculation existe déjà !")]

    # Gestion d'alerte
    kilometrage_vidange = fields.Float(string='Kilométrage vidange', readonly=True)
    montant_vidange = fields.Float(string='Montant vidange', readonly=True)
    nbr_kilometres_alerte = fields.Float(string='NBR kilomètres alerte')
    date_echeance_assurance = fields.Date(string='Date échéance assurance', readonly=True)
    montant_assurance = fields.Float(string='Montant assurance', readonly=True)
    nbr_jour_alerte_assurance = fields.Float(string='NBR jour alerte assurance')
    date_echeance_leasing = fields.Date(string='Date échéance leasing', readonly=True)
    montant_leasing = fields.Float(string='Montant leasing', readonly=True)
    nbr_jours_alerte_leasing = fields.Float(string='NBR jours alerte leasing')
    date_echeance_visite = fields.Date(string='Date échéance visite', readonly=True)
    montant_visite = fields.Float(string='Montant visite', readonly=True)
    nbr_jour_alerte_visite = fields.Float(string='NBR jour alerte visite')
    date_echeance_vignette = fields.Date(string='Date échéance vignette', readonly=True)
    montant_vignette = fields.Float(string='Montant vignette', readonly=True)
    nbr_jour_alerte_vignette = fields.Float(string='NBR jour alerte vignette')

    # Gestion des fluides
    type_carburant = fields.Char(string='Type de carburant')
    fuel_capacity = fields.Float(string='Capacité de carburant')
    oil_name = fields.Char(string='Nom de l\'huile')



    @api.onchange('driver_id')
    def _onchange_driver_id(self):
        if self.driver_id:
            self.driver_mobile = self.driver_id.mobile
        else:
            self.driver_mobile = False

    @api.model
    def check_assurance_dates(self):
        today = fields.Date.today()
        _logger.info(f"Running check_assurance_dates on {today}")
        vehicles = self.search([('date_echeance_assurance', '!=', False)])
        for vehicle in vehicles:
            if vehicle.date_echeance_assurance - timedelta(days=vehicle.nbr_jour_alerte_assurance) <= today <= vehicle.date_echeance_assurance:
                days_left = (vehicle.date_echeance_assurance - today).days
                if vehicle.driver_id:
                    _logger.info(f"Vehicle {vehicle.display_name} has {days_left} days left before assurance expiry.")
                    self.env['mail.message'].create({
                        'body': f"Le véhicule {vehicle.display_name} a {days_left} jours avant l'échéance de l'assurance.",
                        'subject': "Alerte d'échéance d'assurance",
                        'model': 'fleet.vehicle',
                        'res_id': vehicle.id,
                        'message_type': 'notification',
                        'subtype_id': self.env.ref('mail.mt_comment').id,
                        'partner_ids': [(6, 0, [vehicle.driver_id.partner_id.id])]
                    })
                else:
                    _logger.warning(f"Vehicle {vehicle.display_name} has no driver assigned, skipping notification.")

    @api.model
    def check_vidange_dates(self):
        today = fields.Date.today()
        _logger.info(f"Running check_vidange_dates on {today}")
        vehicles = self.search([('date_vidange', '!=', False)])
        for vehicle in vehicles:
            if vehicle.date_vidange - timedelta(days=vehicle.nbr_kilometres_alerte) <= today <= vehicle.date_vidange:
                days_left = (vehicle.date_vidange - today).days
                if vehicle.driver_id:
                    _logger.info(f"Vehicle {vehicle.display_name} has {days_left} days left before vidange expiry.")
                    self.env['mail.message'].create({
                        'body': f"Le véhicule {vehicle.display_name} a {days_left} jours avant l'échéance de la vidange.",
                        'subject': "Alerte d'échéance de vidange",
                        'model': 'fleet.vehicle',
                        'res_id': vehicle.id,
                        'message_type': 'notification',
                        'subtype_id': self.env.ref('mail.mt_comment').id,
                        'partner_ids': [(6, 0, [vehicle.driver_id.partner_id.id])]
                    })
                else:
                    _logger.warning(f"Vehicle {vehicle.display_name} has no driver assigned, skipping notification.")

    @api.model
    def check_leasing_dates(self):
        today = fields.Date.today()
        _logger.info(f"Running check_leasing_dates on {today}")
        vehicles = self.search([('date_echeance_leasing', '!=', False)])
        for vehicle in vehicles:
            if vehicle.date_echeance_leasing - timedelta(days=vehicle.nbr_jours_alerte_leasing) <= today <= vehicle.date_echeance_leasing:
                days_left = (vehicle.date_echeance_leasing - today).days
                if vehicle.driver_id:
                    _logger.info(f"Vehicle {vehicle.display_name} has {days_left} days left before leasing expiry.")
                    self.env['mail.message'].create({
                        'body': f"Le véhicule {vehicle.display_name} a {days_left} jours avant l'échéance du leasing.",
                        'subject': "Alerte d'échéance de leasing",
                        'model': 'fleet.vehicle',
                        'res_id': vehicle.id,
                        'message_type': 'notification',
                        'subtype_id': self.env.ref('mail.mt_comment').id,
                        'partner_ids': [(6, 0, [vehicle.driver_id.partner_id.id])]
                    })
                else:
                    _logger.warning(f"Vehicle {vehicle.display_name} has no driver assigned, skipping notification.")

    @api.model
    def check_visite_dates(self):
        today = fields.Date.today()
        _logger.info(f"Running check_visite_dates on {today}")
        vehicles = self.search([('date_echeance_visite', '!=', False)])
        for vehicle in vehicles:
            if vehicle.date_echeance_visite - timedelta(days=vehicle.nbr_jour_alerte_visite) <= today <= vehicle.date_echeance_visite:
                days_left = (vehicle.date_echeance_visite - today).days
                if vehicle.driver_id:
                    _logger.info(f"Vehicle {vehicle.display_name} has {days_left} days left before visite technique expiry.")
                    self.env['mail.message'].create({
                        'body': f"Le véhicule {vehicle.display_name} a {days_left} jours avant l'échéance de la visite technique.",
                        'subject': "Alerte d'échéance de visite technique",
                        'model': 'fleet.vehicle',
                        'res_id': vehicle.id,
                        'message_type': 'notification',
                        'subtype_id': self.env.ref('mail.mt_comment').id,
                        'partner_ids': [(6, 0, [vehicle.driver_id.partner_id.id])]
                    })
                else:
                    _logger.warning(f"Vehicle {vehicle.display_name} has no driver assigned, skipping notification.")

    @api.model
    def check_vignette_dates(self):
        today = fields.Date.today()
        _logger.info(f"Running check_vignette_dates on {today}")
        vehicles = self.search([('date_echeance_vignette', '!=', False)])
        for vehicle in vehicles:
            if vehicle.date_echeance_vignette - timedelta(days=vehicle.nbr_jour_alerte_vignette) <= today <= vehicle.date_echeance_vignette:
                days_left = (vehicle.date_echeance_vignette - today).days
                if vehicle.driver_id:
                    _logger.info(f"Vehicle {vehicle.display_name} has {days_left} days left before vignette expiry.")
                    self.env['mail.message'].create({
                        'body': f"Le véhicule {vehicle.display_name} a {days_left} jours avant l'échéance de la vignette.",
                        'subject': "Alerte d'échéance de vignette",
                        'model': 'fleet.vehicle',
                        'res_id': vehicle.id,
                        'message_type': 'notification',
                        'subtype_id': self.env.ref('mail.mt_comment').id,
                        'partner_ids': [(6, 0, [vehicle.driver_id.partner_id.id])]
                    })
                else:
                    _logger.warning(f"Vehicle {vehicle.display_name} has no driver assigned, skipping notification.")

class FleetVehicleLogServices(models.Model):
    _inherit = 'fleet.vehicle.log.services'

    @api.model
    def create(self, vals):
        res = super(FleetVehicleLogServices, self).create(vals)

        # Get the related vehicle
        vehicle = res.vehicle_id
        if not vehicle:
            return res

        # Get the creation date of the intervention
        creation_date = res.date or fields.Date.today()
        new_date = creation_date + timedelta(days=365)
        new_date_leasing = creation_date + timedelta(days=30)


        # Check the service type and update vehicle alerts accordingly
        service_type = res.service_type_id.name.lower()

        if service_type == 'vidange':
            # Update kilometrage vidange
            if vehicle.dernier_releve_kilometrique:
                vehicle.kilometrage_vidange = vehicle.dernier_releve_kilometrique + 10000
            vehicle.montant_vidange = res.amount
            vehicle.date_modification = creation_date
            vehicle.date_echeance_vidange = new_date  # Add a field for vidange if needed
            _logger.info(f"Updated 'vidange' alert for vehicle {vehicle.display_name}")

        elif service_type == 'assurance':
            # Update assurance expiration date
            vehicle.date_echeance_assurance = new_date
            vehicle.montant_assurance = res.amount
            _logger.info(f"Updated 'assurance' alert for vehicle {vehicle.display_name}")

        elif service_type == 'leasing':
            # Update leasing expiration date
            vehicle.date_echeance_leasing = new_date_leasing
            vehicle.montant_leasing = res.amount
            _logger.info(f"Updated 'leasing' alert for vehicle {vehicle.display_name}")

        elif service_type == 'visite':
            # Update visite expiration date
            vehicle.date_echeance_visite = new_date
            vehicle.montant_visite = res.amount
            _logger.info(f"Updated 'visite' alert for vehicle {vehicle.display_name}")

        elif service_type == 'vignette':
            # Update vignette expiration date
            vehicle.date_echeance_vignette = new_date
            vehicle.montant_vignette = res.amount
            _logger.info(f"Updated 'vignette' alert for vehicle {vehicle.display_name}")

        return res