from odoo import api, models, fields, _
from datetime import timedelta
import logging

_logger = logging.getLogger(__name__)

class CarRentalContractCron(models.Model):
    _inherit = 'car.rental.contract'

    @api.model
    def _cron_rent_contract_reminder(self):
        """
        Cron job to send email reminders for ending rent contracts
        """
        contract_reminder_days = int(self.env['ir.config_parameter'].sudo().get_param('fleet_rental.contract_reminder_days', default=1))
        end_date_threshold = fields.Date.today() + timedelta(days=contract_reminder_days)
        
        contracts_to_remind = self.search([
            ('state', '=', 'running'),
            ('rent_end_date', '>=', fields.Date.today()),
            ('rent_end_date', '<=', end_date_threshold)
        ])

        for contract in contracts_to_remind:
            _logger.info(f"Sending reminder for contract {contract.name} to {contract.customer_id.name}")
            contract.send_mail_reminder()
        return True

    def send_mail_reminder(self):
        """
        Send email reminder for the rent contract
        """
        template = self.env.ref('fleet_rental.email_template_rent_contract_reminder_end')
        for contract in self:
            _logger.info(f"Sending email to {contract.customer_id.email} for vehicle {contract.vehicle_id.name}")
            _logger.info(f"Contract Details: ID {contract.id}, Customer {contract.customer_id.name}, Vehicle {contract.vehicle_id.name}, End Date {contract.rent_end_date}")
            template.send_mail(contract.id, force_send=True, email_values={'email_to': contract.customer_id.email})