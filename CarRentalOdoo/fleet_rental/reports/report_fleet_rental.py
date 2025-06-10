from odoo import models, fields

class FleetRentalReport(models.Model):
    _name = "report.fleet.rental"
    _description = "Fleet Rental Analysis"
    _auto = False

    # Define at least one field to keep the model valid
    dummy_field = fields.Char(string="Dummy Field")
