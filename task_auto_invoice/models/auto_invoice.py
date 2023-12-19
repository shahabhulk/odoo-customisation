from odoo import api,fields,models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        for order in self:
            res = super(SaleOrder, order).action_confirm()
            delivery_order=self.env['stock.picking'].search([
                ('sale_id','=',order.id),
            ])
            for line in delivery_order.move_ids_without_package:
                line.quantity_done=line.product_uom_qty
            delivery_order.button_validate()
            invoice = order._create_invoices()
            invoice.action_post()  # Automatically validate the invoic
            return res

