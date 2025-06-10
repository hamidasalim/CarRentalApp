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


class FleetRentalLine(models.Model):
    _name = 'fleet.rental.line'

    name = fields.Char(string='Description', help='Nom')
    date_today = fields.Date(string='Date', help='Date d\'aujourd\'hui')
    account_info = fields.Char(string='Compte', help='Infos du compte')
    recurring_amount = fields.Float(string='Montant',
                                    help='Montant de la facture récurrente')
    rental_number = fields.Many2one('car.rental.contract',
                                    string='Numéro de location',
                                    help='Référence de la location')
    payment_info = fields.Char(compute='paid_info', string='État du paiement',
                               default='brouillon', help='Infos du paiement')
    invoice_number = fields.Integer(string='ID de la facture',
                                    help='ID de la facture')
    invoice_ref = fields.Many2one('account.move',
                                  string='Référence de la facture',
                                  help='Référence de la facture')
    date_due = fields.Date(string='Date d\'échéance',
                           help='Date d\'échéance',
                           related='invoice_ref.invoice_date_due')

    def paid_info(self):
        """
            Récupérer les informations de paiement pour l'enregistrement actuel.
            Vérifier l'état de la facture associée en fonction du numéro de
            facture fourni.
            Si l'enregistrement existe, définir le champ payment_info sur l'état
            de la facture.
            Sinon, définir le champ payment_info sur 'Enregistrement supprimé'.
        """
        for each in self:
            if self.env['account.move'].browse(each.invoice_number):
                each.payment_info = self.env['account.move'].browse(
                    each.invoice_number).state
            else:
                each.payment_info = 'Enregistrement supprimé'
