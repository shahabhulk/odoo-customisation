from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    purchase_product_id = fields.Many2one('purchase.order')

    def action_confirm(self):
        for rec in self:
            res = super(SaleOrder, self).action_confirm()
            sale_products = []
            for line in rec.order_line:
                sale_line_vals = {
                    'product_id': line.product_id.id,
                    'product_qty': line.product_uom_qty,
                    'price_unit': line.price_unit,
                    'price_subtotal': line.price_subtotal
                }
                sale_products.append((0, 0, sale_line_vals))
            purchase_vals = {
                'partner_id':rec.partner_id.id,
                'order_line': sale_products
            }
            purchase_products = self.env['purchase.order'].create(purchase_vals)
            rec.purchase_product_id = purchase_products
            purchase_products.button_confirm()
            return res
    def action_purchase_order(self):
        pass
