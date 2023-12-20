from odoo import api, fields, models
from datetime import date


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def button_confirm(self):
        res = super(PurchaseOrder, self).button_confirm()
        for rec in self:
            current_purchase = self.env['stock.picking'].search([
                ('purchase_id', '=', rec.id)
            ])
            if current_purchase:
                for line in current_purchase.move_ids_without_package.move_line_ids:
                    line.move_id.quantity_done = line.move_id.product_uom_qty
                    current_purchase.button_validate()
            rec.action_create_invoice()
            new_vendor_order = self.env['account.move'].search([
                ('partner_id', '=', rec.partner_id.id),
                ('move_type', '=', 'in_invoice'),
                ('state', '=', 'draft')
            ])

            if new_vendor_order:
                new_vendor_order.invoice_date = fields.Date.today()
                new_vendor_order.action_post()

        return res


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    purchase_id = fields.Many2one('purchase.order', string='purchase_id')
