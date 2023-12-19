from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()

        # Find the related delivery order for this sale order
        current_sale_order = self.env['stock.picking'].search([
            ('sale_id', '=', self.id),
        ], limit=1)
        if current_sale_order:
            for line in current_sale_order.move_ids_without_package.move_line_ids:
                line.move_id.quantity_done = line.move_id.product_uom_qty

            current_sale_order.action_assign()
            current_sale_order.button_validate()


        return res
