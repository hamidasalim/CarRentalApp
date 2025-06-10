from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import timedelta

class CarRentalContract(models.Model):
    _name = 'car.rental.contract'
    _description = 'Car Rental Contract'

    name = fields.Char(string="Nom", required=True, copy=False, readonly=True, default='New')
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('reserved', 'Réservé'),
        ('running', 'En Cours'),
        ('done', 'Terminé'),
        ('cancel', 'Annulé')
    ], string='Etat', default='draft')
    company_id = fields.Many2one('res.company', string='Client', required=True,
                                 default=lambda self: self.env.company,
                                 help="Entreprise propriétaire de cet enregistrement")
    customer_id = fields.Many2one('res.partner', string='Conducteur', required=True, help="Conducteur principal")
    second_driver = fields.Many2one('res.partner', string="2ème Conducteur", help="Deuxième conducteur")
    vehicle_id = fields.Many2one('fleet.vehicle', string='Véhicule', required=True)
    last_odometer = fields.Float(string="Dernier compteur kilométrique", help="Dernier compteur kilométrique", related='vehicle_id.dernier_releve_kilometrique', readonly=True)
    new_odometer = fields.Float(string="Nouveau compteur kilométrique", help="Nouveau compteur kilométrique")
    old_odometer = fields.Float(string="Ancien compteur kilométrique", readonly=True)

    fuel_level = fields.Selection([('1/4', '1/4'), ('1/2', '1/2'), ('3/4', '3/4'), ('Plein', 'Plein')], string="Niveau Carburant", help="Niveau de carburant")
    rent_start_date = fields.Datetime(string="Date de début", required=True)
    rent_end_date = fields.Datetime(string="Date d'expiration", required=True)
    tarif = fields.Float(string='Tarif', related='vehicle_id.tarif', readonly=True)
    rent_type = fields.Selection([('Jour', 'Jour'), ('Heure', 'Heure')], string="Type de location")
    total_days = fields.Integer(string="Total Jours", compute='_compute_total_days')
    total_cost = fields.Float(string="Total Location", compute='_compute_total_cost')
    contract_date = fields.Date(string="Date de Contrat", default=fields.Date.context_today)
    old_rent_end_date = fields.Datetime(string="Ancienne date d'expiration")
    is_paid = fields.Boolean(string="Est payé", default=False)
    new_rent_end_date = fields.Datetime(string="Nouvelle date d'expiration")

    force_create_vidange = fields.Boolean(string="Forcer création (vidange)")
    force_create_assurance = fields.Boolean(string="Forcer création (assurance)")
    force_create_leasing = fields.Boolean(string="Forcer création (leasing)")
    force_create_visite = fields.Boolean(string="Forcer création (visite)")
    force_create_vignette = fields.Boolean(string="Forcer création (vignette)")

    kilometrage_vidange = fields.Float(string='Kilométrage vidange', related='vehicle_id.kilometrage_vidange', readonly=True)
    montant_vidange = fields.Float(string='Montant vidange', related='vehicle_id.montant_vidange', readonly=True)
    nbr_kilometres_alerte = fields.Float(string='NBR kilomètres alerte', related='vehicle_id.nbr_kilometres_alerte', readonly=True)

    date_echeance_assurance = fields.Date(string='Date échéance assurance', related='vehicle_id.date_echeance_assurance', readonly=True)
    montant_assurance = fields.Float(string='Montant assurance', related='vehicle_id.montant_assurance', readonly=True)
    nbr_jour_alerte_assurance = fields.Float(string='NBR jour alerte assurance', related='vehicle_id.nbr_jour_alerte_assurance', readonly=True)

    date_echeance_leasing = fields.Date(string='Date échéance leasing', related='vehicle_id.date_echeance_leasing', readonly=True)
    montant_leasing = fields.Float(string='Montant leasing', related='vehicle_id.montant_leasing', readonly=True)
    nbr_jours_alerte_leasing = fields.Float(string='NBR jours alerte leasing', related='vehicle_id.nbr_jours_alerte_leasing', readonly=True)

    date_echeance_visite = fields.Date(string='Date échéance visite', related='vehicle_id.date_echeance_visite', readonly=True)
    montant_visite = fields.Float(string='Montant visite', related='vehicle_id.montant_visite', readonly=True)
    nbr_jour_alerte_visite = fields.Float(string='NBR jour alerte visite', related='vehicle_id.nbr_jour_alerte_visite', readonly=True)

    date_echeance_vignette = fields.Date(string='Date échéance vignette', related='vehicle_id.date_echeance_vignette', readonly=True)
    montant_vignette = fields.Float(string='Montant vignette', related='vehicle_id.montant_vignette', readonly=True)
    nbr_jour_alerte_vignette = fields.Float(string='NBR jour alerte vignette', related='vehicle_id.nbr_jour_alerte_vignette', readonly=True)
    tarif_carburant = fields.Float(string="Tarif Carburant", compute="_compute_tarif_carburant")
    acompte = fields.Float(string="Acompte")

    payment_ids = fields.One2many('account.payment', 'contract_id', string="Payments")

    extended_days = fields.Integer(string="Extended Days", compute='_compute_extended_days')
    extra_cost = fields.Float(string="Extra Cost", compute='_compute_extra_cost')

    second_vehicle_id = fields.Many2one('fleet.vehicle', string='Second Véhicule', readonly=False, help="Véhicule secondaire associé au contrat.")

    
    
    @api.onchange('rent_start_date', 'rent_end_date')
    def _onchange_vehicle_id_domain(self):
        if self.rent_start_date and self.rent_end_date and self.rent_start_date < self.rent_end_date:
            # Fetch vehicle IDs already reserved or running in the given date range
            rented_vehicle_ids = self.env['car.rental.contract'].sudo().search([
                ('state', 'in', ['reserved', 'running']),  # Replace with your relevant states
                ('rent_start_date', '<=', self.rent_end_date),
                ('rent_end_date', '>=', self.rent_start_date),
            ]).mapped('vehicle_id.id')

            # Apply domain to filter out rented vehicles
            return {
                'domain': {
                    'vehicle_id': [('id', 'not in', rented_vehicle_ids)]
                }
            }
        else:
            # Clear domain if dates are invalid or not set
            return {
                'domain': {
                    'vehicle_id': []
                }
            }
            
    def action_change_vehicle(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Changer de Véhicule',
            'res_model': 'car.rental.change.vehicle.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_contract_id': self.id},
        }
    
    def print_contract(self):
        """Print the contract report for the current contract."""
        self.ensure_one()  # Ensure only one record is processed
        if not self.name:
            raise UserError("Le contrat n'a pas de numéro. Veuillez d'abord sauvegarder le contrat.")
        
        return self.env.ref('fleet_rental.contrat_report_pdf_action').report_action(self)

    @api.depends('rent_end_date', 'old_rent_end_date')
    def _compute_extended_days(self):
        for record in self:
            if record.old_rent_end_date and record.rent_end_date:
                record.extended_days = (record.rent_end_date - record.old_rent_end_date).days
            else:
                record.extended_days = 0

    @api.depends('extended_days', 'tarif')
    def _compute_extra_cost(self):
        for record in self:
            record.extra_cost = record.extended_days * record.tarif if record.extended_days > 0 else 0


    @api.onchange('vehicle_id', 'rent_start_date', 'rent_end_date')
    def _onchange_vehicle_or_dates(self):
        if self.vehicle_id and self.rent_start_date and self.rent_end_date:
            overlapping_contracts = self.env['car.rental.contract'].search([
                ('vehicle_id', '=', self.vehicle_id.id),
                ('state', '!=', 'draft'),
                ('rent_start_date', '<=', self.rent_end_date),
                ('rent_end_date', '>=', self.rent_start_date)
            ])
            if overlapping_contracts:
                self.vehicle_id = False
                return {
                    'warning': {
                        'title': "Véhicule indisponible",
                        'message': "Le véhicule sélectionné est déjà réservé pour les dates choisies. Veuillez choisir un autre véhicule ou modifier les dates."
                    }
                }


    @api.onchange('vehicle_id')
    def _onchange_vehicle_id(self):
        if self.vehicle_id:
            self.kilometrage_vidange = self.vehicle_id.kilometrage_vidange
            self.montant_vidange = self.vehicle_id.montant_vidange
            self.nbr_kilometres_alerte = self.vehicle_id.nbr_kilometres_alerte

            self.date_echeance_assurance = self.vehicle_id.date_echeance_assurance
            self.montant_assurance = self.vehicle_id.montant_assurance
            self.nbr_jour_alerte_assurance = self.vehicle_id.nbr_jour_alerte_assurance

            self.date_echeance_leasing = self.vehicle_id.date_echeance_leasing
            self.montant_leasing = self.vehicle_id.montant_leasing
            self.nbr_jours_alerte_leasing = self.vehicle_id.nbr_jours_alerte_leasing

            self.date_echeance_visite = self.vehicle_id.date_echeance_visite
            self.montant_visite = self.vehicle_id.montant_visite
            self.nbr_jour_alerte_visite = self.vehicle_id.nbr_jour_alerte_visite

            self.date_echeance_vignette = self.vehicle_id.date_echeance_vignette
            self.montant_vignette = self.vehicle_id.montant_vignette
            self.nbr_jour_alerte_vignette = self.vehicle_id.nbr_jour_alerte_vignette

    @api.model
    def create(self, vals):
        # Get the conducteur_id from the values
        conducteur_id = vals.get('customer_id')

        # Check if conducteur_id exists
        if conducteur_id:
            conducteur = self.env['res.partner'].sudo().browse(conducteur_id)

            # Check if category_id is approved
            if not conducteur.category_id:
                raise UserError("Please complete user profile or update user profile to include the required fields.")
 
        # Auto-generate name if it is the default value ("New")
        if vals.get('name', 'New') == 'New':
            # Find the last record by ID
            last_record = self.search([], order='id desc', limit=1)
            if last_record:
                # Extract the number from the last record's name (e.g., Rent001 → 1)
                last_number = int(last_record.name[4:]) if last_record.name.startswith('Rent') else 0
                next_number = last_number + 1
            else:
                # Start from 1 if no records exist
                next_number = 1

            # Format the new name (e.g., Rent001)
            vals['name'] = f'Rent{str(next_number).zfill(3)}'

               # Validate rental dates
        rent_start_date = vals.get('rent_start_date')
        rent_end_date = vals.get('rent_end_date')
        if rent_start_date and rent_end_date:
            rent_start_date = fields.Datetime.from_string(rent_start_date)
            rent_end_date = fields.Datetime.from_string(rent_end_date)

            # Ensure start_date is earlier than end_date
            if rent_start_date >= rent_end_date:
                raise UserError("La date de début doit être antérieure à la date d'expiration.")
            
        vehicle_id = vals.get('vehicle_id')
        if rent_start_date and rent_end_date and vehicle_id:
            overlapping_contracts = self.env['car.rental.contract'].search([
                ('vehicle_id', '=', vehicle_id),
                ('state', 'not in', ['draft', 'cancel']),  # Exclude draft and cancelled states
                ('rent_start_date', '<=', rent_end_date),
                ('rent_end_date', '>=', rent_start_date)
            ])
            if overlapping_contracts:
                raise UserError(
                    "Le véhicule sélectionné est déjà réservé pour les dates choisies :\n"
                    f"Du {overlapping_contracts[0].rent_start_date} au {overlapping_contracts[0].rent_end_date}"
                )

        # Proceed with creating the record
        return super(CarRentalContract, self).create(vals)

    def write(self, vals):
        if 'rent_start_date' in vals or 'rent_end_date' in vals or 'vehicle_id' in vals:
            rent_start_date = vals.get('rent_start_date', self.rent_start_date)
            rent_end_date = vals.get('rent_end_date', self.rent_end_date)
            vehicle_id = vals.get('vehicle_id', self.vehicle_id.id)
            overlapping_contracts = self.env['car.rental.contract'].search([
                ('vehicle_id', '=', vehicle_id),
                ('state', '!=', 'draft'),
                ('state', '!=', 'cancel'),
                ('rent_start_date', '<=', rent_end_date),
                ('rent_end_date', '>=', rent_start_date),
                ('id', '!=', self.id)
            ])
            if overlapping_contracts:
                raise UserError("Le véhicule sélectionné est déjà réservé pour les dates choisies.")
        return super(CarRentalContract, self).write(vals)

    @api.depends('rent_start_date', 'rent_end_date')
    def _compute_total_days(self):
        for record in self:
            if record.rent_start_date and record.rent_end_date:
                record.total_days = (record.rent_end_date - record.rent_start_date).days
            else:
                record.total_days = 0

    @api.depends('total_days', 'tarif', 'acompte', 'tarif_carburant')
    def _compute_total_cost(self):
        for record in self:
            record.total_cost = (record.total_days * record.tarif)  + record.tarif_carburant

    @api.depends('fuel_level')
    def _compute_tarif_carburant(self):
        for record in self:
            if record.fuel_level == '1/4':
                record.tarif_carburant = 15
            elif record.fuel_level == '1/2':
                record.tarif_carburant = 30
            elif record.fuel_level == '3/4':
                record.tarif_carburant = 45
            elif record.fuel_level == 'Plein':
                record.tarif_carburant = 60
            else:
                record.tarif_carburant = 0



    def action_confirm(self):
        self._check_vehicle_alerts()
        self.state = 'reserved'
        self.vehicle_id.rental_check_availability= False


    def action_done(self):
        for record in self:
            if not record.new_odometer:
                raise UserError("Veuillez insérer le nouveau kilométrage de la voiture avant de terminer le contrat.")
            record.old_odometer = record.last_odometer  # Store the old odometer reading
            record.vehicle_id.dernier_releve_kilometrique = record.new_odometer  # Update the vehicle's 
            record.vehicle_id.rental_check_availability = True
            if not self.is_paid:
                raise UserError("Le contrat doit être payé avant de pouvoir être terminé.")
            self.state = 'done'


    def action_cancel(self):
        self.state = 'cancel'
        self.vehicle_id.write({'rental_check_availability' : True})

    def action_extend_rent(self):
        """Open the modal to set a new rent end date."""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Extend Rent',
            'res_model': 'car.rental.extend.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_contract_id': self.id},
        }

    def open_payment_modal(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Payer le contrat',
            'res_model': 'account.payment',
            'view_mode': 'form',
            'view_id': self.env.ref('fleet_rental.view_payment_form_inherit').id,
            'target': 'new',
            'context': {
                'default_contract_id': self.id,
                'default_total_cost': self.extra_cost if self.extended_days > 0 else self.total_cost,
                'default_customer_id': self.customer_id.id,
                'default_vehicle_id': self.vehicle_id.id,
                'default_rent_start_date': self.rent_start_date,
                'default_rent_end_date': self.rent_end_date,
                'default_acompte': self.acompte,
            },
        }

    def action_confirm_payment(self):
        contract_id = self.env.context.get('default_contract_id')
        if not contract_id:
            raise UserError("Erreur: l'ID du contrat n'est pas trouvé.")
        
        contract = self.env['car.rental.contract'].browse(contract_id)
        
        if self.deposit != self.total_cost:
            raise UserError("Le montant payé doit être égal au montant à payer.")
        
        contract.write({'is_paid': True , 'state' :'reserved' , 'extra_cost': 0})
        return {'type': 'ir.actions.act_window_close'}

    def _check_vehicle_alerts(self):
        vehicle = self.vehicle_id
        rent_start_date = self.rent_start_date.date()
        rent_end_date = self.rent_end_date.date()
        if vehicle:
            if vehicle.kilometrage_vidange <= vehicle.nbr_kilometres_alerte + vehicle.dernier_releve_kilometrique and not self.force_create_vidange:
                raise UserError("L'alerte vidange est active. Veuillez résoudre cette alerte avant de confirmer le contrat.")
             # Assurance Alert
            if vehicle.date_echeance_assurance:
                assurance_alert_date = vehicle.date_echeance_assurance - timedelta(days=vehicle.nbr_jour_alerte_assurance)
                if rent_start_date <= vehicle.date_echeance_assurance and rent_end_date >= assurance_alert_date and not self.force_create_assurance:
                    raise UserError(
                        "Le véhicule est en période d'alerte assurance.\n"
                        f"Date d'alerte assurance : {assurance_alert_date}.\n"
                        "Veuillez résoudre cette alerte avant de confirmer le contrat."
                    )

            # Leasing Alert
            if vehicle.date_echeance_leasing:
                leasing_alert_date = vehicle.date_echeance_leasing - timedelta(days=vehicle.nbr_jours_alerte_leasing)
                if rent_start_date <= vehicle.date_echeance_leasing and rent_end_date >= leasing_alert_date and not self.force_create_leasing:
                    raise UserError(
                        "Le véhicule est en période d'alerte leasing.\n"
                        f"Date d'alerte leasing : {leasing_alert_date}.\n"
                        "Veuillez résoudre cette alerte avant de confirmer le contrat."
                    )

            # Visite Alert
            if vehicle.date_echeance_visite:
                visite_alert_date = vehicle.date_echeance_visite - timedelta(days=vehicle.nbr_jour_alerte_visite)
                if rent_start_date <= vehicle.date_echeance_visite and rent_end_date >= visite_alert_date and not self.force_create_visite:
                    raise UserError(
                        "Le véhicule est en période d'alerte visite technique.\n"
                        f"Date d'alerte visite : {visite_alert_date}.\n"
                        "Veuillez résoudre cette alerte avant de confirmer le contrat."
                    )

            # Vignette Alert
            if vehicle.date_echeance_vignette:
                vignette_alert_date = vehicle.date_echeance_vignette - timedelta(days=vehicle.nbr_jour_alerte_vignette)
                if rent_start_date <= vehicle.date_echeance_vignette and rent_end_date >= vignette_alert_date and not self.force_create_vignette:
                    raise UserError(
                        "Le véhicule est en période d'alerte vignette.\n"
                        f"Date d'alerte vignette : {vignette_alert_date}.\n"
                        "Veuillez résoudre cette alerte avant de confirmer le contrat."
                    )

        # Reset the checkboxes
        self.force_create_vidange = False
        self.force_create_assurance = False
        self.force_create_leasing = False
        self.force_create_visite = False
        self.force_create_vignette = False

    class CarRentalExtendWizard(models.TransientModel):
        _name = 'car.rental.extend.wizard'
        _description = 'Extend Rent Wizard'

        contract_id = fields.Many2one('car.rental.contract', string="Contract", required=True)
        new_rent_end_date = fields.Datetime(string="New End Date", required=True)

        def confirm_extension(self):
            """Update the contract with the new rent end date."""
            self.ensure_one()
            if self.new_rent_end_date <= self.contract_id.rent_end_date:
                raise UserError("The new end date must be later than the current end date.")
            
            # Save the old end date before updating
            self.contract_id.old_rent_end_date = self.contract_id.rent_end_date
            self.contract_id.rent_end_date = self.new_rent_end_date


class CarRentalChangeVehicleWizard(models.TransientModel):
    _name = 'car.rental.change.vehicle.wizard'
    _description = 'Changer de Véhicule'

    contract_id = fields.Many2one('car.rental.contract', string="Contrat", required=True)
    new_vehicle_id = fields.Many2one('fleet.vehicle', string="Nouveau Véhicule", required=True)

    def confirm_change_vehicle(self):
        """Store the new vehicle in second_vehicle_id."""
        self.ensure_one()
        contract = self.contract_id

        # Check if the new vehicle is available
        overlapping_contracts = self.env['car.rental.contract'].search([
            ('vehicle_id', '=', self.new_vehicle_id.id),
            ('state', '!=', 'draft'),
            ('rent_start_date', '<=', contract.rent_end_date),
            ('rent_end_date', '>=', contract.rent_start_date)
        ])
        if overlapping_contracts:
            raise UserError("Le nouveau véhicule sélectionné est déjà réservé pour les dates choisies.")

        # Store the new vehicle in second_vehicle_id
        contract.second_vehicle_id = self.new_vehicle_id

