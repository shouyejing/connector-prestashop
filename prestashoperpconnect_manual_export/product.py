# -*- coding: utf-8 -*-
##############################################################################
#
#  licence AGPL version 3 or later
#  see licence in __openerp__.py or http://www.gnu.org/licenses/agpl-3.0.txt
#  Copyright (C) 2015 Akretion (http://www.akretion.com).
#
##############################################################################
from openerp import models, api
from openerp.addons.connector.session import ConnectorSession
import openerp.addons.prestashoperpconnect.consumer as prestashoperpconnect


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.multi
    def write(self, vals):
        """
        Don't trigger automatic export.
        """
        return super(
            ProductTemplate,
            self.with_context(connector_no_export=True)).write(vals)


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.multi
    def write(self, vals):
        """
        Don't trigger automatic export.
        """
        return super(
            ProductProduct,
            self.with_context(connector_no_export=True)).write(vals)


class PrestashopProductTemplate(models.Model):
    _inherit = 'prestashop.product.template'

    @api.model
    def create(self, vals):
        """
        Don't trigger automatic export.
        """
        return super(
            PrestashopProductTemplate,
            self.with_context(connector_no_export=True)).create(vals)

    @api.multi
    def write(self, vals):
        """
        Don't trigger automatic export.
        """
        return super(
            PrestashopProductTemplate,
            self.with_context(connector_no_export=True)).write(vals)

    @api.multi
    def export_product(self):
        session = ConnectorSession(self.env.cr, self.env.uid,
                                   context=self.env.context)
        for product in self:
            prestashoperpconnect.delay_export(
                session, 'prestashop.product.template', product.id, {})
        return True

