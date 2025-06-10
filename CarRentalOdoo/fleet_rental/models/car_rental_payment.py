from odoo import models, fields, api
from odoo.exceptions import UserError

class CarRentalPayment(models.Model):
    _inherit = 'account.payment'
    _description = 'Car Rental Payment'
    
    contract_id = fields.Many2one('car.rental.contract', string='Contrat', help="Contrat", required=True, ondelete='cascade')
    customer_id = fields.Many2one('res.partner', string="Conducteur", help="Conducteur", related='contract_id.customer_id', readonly=True)
    vehicle_id = fields.Many2one('fleet.vehicle', string="Véhicule", help="Véhicule", related='contract_id.vehicle_id', readonly=True)
    rent_start_date = fields.Datetime(string="Date de début", help="Date de début", related='contract_id.rent_start_date', required=True)
    rent_end_date = fields.Datetime(string="Date de fin", help="Date de fin", related='contract_id.rent_end_date', required=True)
    acompte = fields.Float(string="Acompte", help="Acompte", related='contract_id.acompte', readonly=True)
    montant_restant = fields.Float(string="Montant restant à payer", help="Montant restant à payer", compute="_compute_montant_restant", store=True)
    total_amount = fields.Float(string="Montant à payer", help="Montant à payer", compute="_compute_total_costp", store=True)
    move_id = fields.Many2one('account.move', string="Invoice")
    no_tax = fields.Float(string="Montant sans tax", help="Montant sans tax", related='contract_id.total_cost', readonly=True)
    no_timbre = fields.Float(string="Montant sans tax", help="Montant sans tax", compute="_compute_total_costpt", readonly=True)

    extra_cost = fields.Float( string="Extra cost", help="extra cost", related='contract_id.extra_cost', readonly=True)

    
    tax_rate = fields.Float(string="Tax Rate", default=0.19)
    tax_timbre = fields.Float(string="Tax Timbre", default=1.0)
    
   
    bank_name = fields.Char(string="Banque")
    cheque_number = fields.Char(string="Numero de chèque")

    @api.depends('total_amount', 'acompte','extra_cost')
    def _compute_montant_restant(self):
        for record in self:
            if record.extra_cost:
                record.montant_restant = record.extra_cost + record.tax_timbre + record.extra_cost * record.tax_rate
            else:
                record.montant_restant = record.total_amount - record.acompte

    @api.depends('contract_id.total_cost')
    def _compute_total_costp(self):
        for record in self:
            if record.contract_id:
                base_cost = record.contract_id.total_cost
                tax_amount = base_cost * record.tax_rate
                record.total_amount = base_cost + tax_amount + record.tax_timbre

    @api.depends('contract_id.total_cost')
    def _compute_total_costpt(self):
        for record in self:
            if record.contract_id:
                base_cost = record.contract_id.total_cost
                tax_amount = base_cost * record.tax_rate
                record.total_amount = base_cost + tax_amount 

    @api.model
    def create(self, vals):
        res = super(CarRentalPayment, self).create(vals)
        res.action_confirm_payment()
        return res

    def action_confirm_payment(self):
        self.ensure_one()
        if not self.journal_id:
            raise UserError("Veuillez définir un mode de paiement sur votre paiement.")
        #if self.amount != self.montant_restant:
            #raise UserError("Le montant payé doit être égal au montant restant à payer.")
        
        self.contract_id.write({'is_paid': True, 'state': 'running', 'extra_cost':0})
        #self.contract_id.write({'is_paid': True, 'state': 'running', 'extra_cost':0})


        return {'type': 'ir.actions.act_window_close'}

    def create_invoice(self):
        self.ensure_one()
        if not self.move_id:
            account = self.env['account.move'].search([('code', '=', '400000')], limit=1)
            if not account:
                raise UserError("Account with code '400000' not found.")
            
            move_vals = {
                'quick_edit_total_amount': self.no_timbre,
                'payment_id': self.id,
                'car_rental_contract_id': self.contract_id,
                'invoice_line_ids': [
                    (0, 0, {
                        'quantity': 1,
                        'account_id': account.id,
                    }),
                ],
            }
            move = self.env['account.move'].create(move_vals)
            self.write({'move_id': move.id})
            move.action_post()

    
    def print_invoice(self):
        # Ensure the current payment is posted
        if self.state != 'posted':
            raise UserError("Seuls les paiements validés peuvent générer une facture.")

        # Render the PDF using the report template
        return self.env.ref('fleet_rental.payment_invoice_report_action').report_action(self)

class AccountMoveExtended(models.Model):
    _inherit = 'account.move'
    car_rental_contract_id = fields.Many2one('car.rental.contract', string='Rental Contract')



