# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api, _
from openerp.exceptions import Warning
import time
import logging
_logger = logging.getLogger(__name__)


class product_template(models.Model):
    _inherit = 'product.template'

    # product_id = fields.Integer(
    #     related='product_variant_ids.product_id'
    #     # 'product.pricelist',
    #     # compute='_get_product_id',
    #     # store=True
    #     )
    # pricelist_ids = fields.Many2many(
    pricelist_ids = fields.One2many(
        'product.pricelist',
        compute='get_pricelist_ids',
        inverse='dummy_inverse',
        string='Pricelists',
        )
    pricelist_qty = fields.Float(
        string="Cantidad",
        default=1.0,
    )

    @api.one
    def dummy_inverse(self):
        """
        Dummy Inverse function so that we can edit vouchers and save changes
        """
        return True

    @api.one
    # TODO use multi
    def get_pricelist_ids(self):
        pricelists = self.pricelist_ids.search([
            ('type', '=', 'sale'),
            ])
        date = self._context.get('date') or time.strftime('%Y-%m-%d')
        date = date[0:10]
        for pricelist in pricelists:
            version = False
            for v in pricelist.version_id:
                if ((v.date_start is False) or (v.date_start <= date)) and ((v.date_end is False) or (v.date_end >= date)):
                    version = v
                    break
            if version:
                self.pricelist_ids |= pricelist

# class product_product(models.Model):
#     _inherit = 'product.product'

#     # product_id = fields.Many2one(
#     product_id = fields.Integer(
#         # 'product.pricelist',
#         related='id',
#         # compute='_get_product_id',
#         # store=True
#         )
