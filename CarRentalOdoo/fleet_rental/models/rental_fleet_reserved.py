# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2024-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Cybrosys Techno Solutions(<https://www.cybrosys.com>)
#
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
from odoo import models, fields


class FleetReservedTime(models.Model):
    _name = "rental.fleet.reserved"
    _description = "Temps réservé"

    customer_id = fields.Many2one('res.partner',
                                  string='Client',
                                  help='Sélectionnez le client')
    date_from = fields.Date(string='Date de début de réservation',
                            help='Sélectionnez la date de début de la location')
    date_to = fields.Date(string='Date de fin de réservation',
                          help='Sélectionnez la date de fin de la location')
    reserved_obj_id = fields.Many2one('fleet.vehicle',
                                      string='Objet réservé',
                                      help='Objet réservé')

