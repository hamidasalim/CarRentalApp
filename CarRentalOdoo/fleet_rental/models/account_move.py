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
from odoo import fields, models


class AccountMove(models.Model):
    """Hériter de account.move pour ajouter un champ supplémentaire"""
    _inherit = 'account.move'

    fleet_rent_id = fields.Many2one('car.rental.contract',
                                    string='Location',
                                    help='Facture liée à quel enregistrement de location')

    is_first_invoice = fields.Boolean(string='Est-ce la première facture de location', default=False,
                                      help='Est-ce la première facture de location')

    def button_cancel(self):
        """
            Surcharger la méthode de base button_cancel pour gérer la logique
            supplémentaire pour le modèle 'car.rental.contract' basé sur 'fleet_rent_id'.
        """
        res = super().button_cancel()
        fleet_model = self.env['car.rental.contract'].search(
            [('id', '=', self.fleet_rent_id.id)])
        if fleet_model.state == 'running':
            fleet_model.state = 'running'
            fleet_model.first_invoice_created = False
        else:
            fleet_model.state = 'checking'
        return res
