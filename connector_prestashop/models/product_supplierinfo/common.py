# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields

from ...unit.backend_adapter import (
    PrestaShopCRUDAdapter,
    PrestaShopWebServiceImage,
    GenericAdapter,
)
from ...backend import prestashop


class ResPartner(models.Model):
    _inherit = 'res.partner'

    prestashop_supplier_bind_ids = fields.One2many(
        comodel_name='prestashop.supplier',
        inverse_name='openerp_id',
        string="PrestaShop supplier bindings",
    )


class PrestashopSupplier(models.Model):
    _name = 'prestashop.supplier'
    _inherit = 'prestashop.binding'
    _inherits = {'res.partner': 'openerp_id'}

    openerp_id = fields.Many2one(
        comodel_name='res.partner',
        string='Partner',
        required=True,
        ondelete='cascade',
    )

    _sql_constraints = [
        ('prestashop_erp_uniq', 'unique(backend_id, openerp_id)',
         'A erp record with same ID on PrestaShop already exists.'),
    ]


class ProductSupplierinfo(models.Model):
    _inherit = 'product.supplierinfo'

    prestashop_bind_ids = fields.One2many(
        comodel_name='prestashop.product.supplierinfo',
        inverse_name='openerp_id',
        string="PrestaShop bindings",
    )


class PrestashopProductSupplierinfo(models.Model):
    _name = 'prestashop.product.supplierinfo'
    _inherit = 'prestashop.binding'
    _inherits = {'product.supplierinfo': 'openerp_id'}

    openerp_id = fields.Many2one(
        comodel_name='product.supplierinfo',
        string='Supplier info',
        required=True,
        ondelete='cascade',
    )

    _sql_constraints = [
        ('prestashop_erp_uniq', 'unique(backend_id, openerp_id)',
         'A erp record with same ID on PrestaShop already exists.'),
    ]


@prestashop
class SupplierImageAdapter(PrestaShopCRUDAdapter):
    _model_name = 'prestashop.supplier.image'
    _prestashop_image_model = 'suppliers'

    def read(self, supplier_id, options=None):
        client = PrestaShopWebServiceImage(self.prestashop.api_url,
                                           self.prestashop.webservice_key)
        res = client.get_image(
            self._prestashop_image_model,
            supplier_id,
            options=options
        )
        return res['content']


@prestashop
class SupplierAdapter(GenericAdapter):
    _model_name = 'prestashop.supplier'
    _prestashop_model = 'suppliers'


@prestashop
class SupplierInfoAdapter(GenericAdapter):
    _model_name = 'prestashop.product.supplierinfo'
    _prestashop_model = 'product_suppliers'
