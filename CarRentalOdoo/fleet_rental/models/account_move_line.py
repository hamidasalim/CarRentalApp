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
from odoo import api, models


class AccountMoveLine(models.Model):
    """Hériter de account.move.line"""
    _inherit = 'account.move.line'

    @api.onchange('price_unit')
    def _onchange_price_unit(self):
        """
            Mettre à jour le champ 'first_payment' du modèle associé
            'car.rental.contract' lorsque le champ 'price_unit' change.
        """
        fleet_model = self.move_id.fleet_rent_id
        if fleet_model:
            fleet_model.first_payment = self.price_unit

