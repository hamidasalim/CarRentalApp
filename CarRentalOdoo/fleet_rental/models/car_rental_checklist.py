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
from odoo import api, fields, models


class CarRentalChecklist(models.Model):
    """Modèle pour ajouter la checklist de location"""
    _name = 'car.rental.checklist'

    name = fields.Many2one('car.tools', string="Nom",
                           help='Sélectionnez les outils de voiture')
    checklist_active = fields.Boolean(string="Disponible",
                                      default=True,
                                      help='Activer lorsque l\'outil est disponible lors de la vérification')
    checklist_number = fields.Many2one('car.rental.contract',
                                       string="Numéro de checklist",
                                       help='Numéro de la checklist')
    price = fields.Float(string="Prix",
                         help='Prix de l\'outil de voiture')
    company_id = fields.Many2one('res.company', string='Entreprise',
                                 default=lambda self: self.env.company,
                                 help="Entreprise propriétaire de cet enregistrement")

    @api.onchange('name')
    def onchange_name(self):
        """
           Mettre à jour le prix en fonction du nom sélectionné.
        """
        self.price = self.name.price
