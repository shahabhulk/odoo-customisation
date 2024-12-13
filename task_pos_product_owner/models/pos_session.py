from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_owner = fields.Many2one('res.partner', string='Product Owner')


class ProductProduct(models.Model):
    _inherit = 'product.product'

    product_owner = fields.Many2one(
        'res.partner',
        string='Product Owner',
        related='product_tmpl_id.product_owner',
       # Storing the field for easier search and retrieval, adjust according to your needs.

    )


class PosSession(models.Model):
    _inherit = 'pos.session'

    def _loader_params_product_product(self):
        result = super()._loader_params_product_product()
        # Make sure to include 'product_owner' in the list of fields to fetch.
        result['search_params']['fields'].append('product_owner')
        return result
