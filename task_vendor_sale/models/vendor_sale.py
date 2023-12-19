from odoo import api, fields, models
from datetime import date


class VendorBill(models.Model):
    _name = "vendor.bill"

    sale_order_id = fields.Many2one("sale.order", string="Sale Order")
    account_move_id = fields.Many2one("account.move", string="Vendor Bill")


class SaleOrder(models.Model):
    _inherit = "sale.order"

    vendor_order_id = fields.Many2one("account.move", string="Vendor Order")
    vendor_bill_count = fields.Integer(string="Vendor Bill Count")
    is_vendor_bill_created = fields.Boolean(string="Vendor Bill Created")

    def create_vendor_bill(self):
        vendor_orders = {}
        vendors = set()  # Use a set to keep track of unique vendors

        for line in self.order_line:
            vendor = line.vendors_id
            vendors.add(vendor.id)

            if vendor.id in vendor_orders:
                vendor_orders[vendor.id].append(line)
            else:
                vendor_orders[vendor.id] = [line]

        for v in vendors:
            vendor_order_line = []
            for line in vendor_orders[v]:
                vendor_order_vals = {
                    'product_id': line.product_id.id,
                    'quantity': line.product_uom_qty,
                    'price_unit': line.price_unit,
                    'price_subtotal': line.price_subtotal,
                    'name': line.product_id.name
                }
                vendor_order_line.append((0, 0, vendor_order_vals))

            vendor_vals = {
                'partner_id': v,
                'move_type': 'in_invoice',  # Set the move type to 'in_invoice' for a Vendor Bill
                'invoice_date': date.today(),
                'invoice_line_ids': vendor_order_line
            }

            vendor_order = self.env['account.move'].create(vendor_vals)
            self.vendor_order_id = vendor_order.id

            # Create a record in the VendorBill model to link the sale order and vendor bill
            self.env['vendor.bill'].create({
                'sale_order_id': self.id,
                'account_move_id': vendor_order.id,
            })

            vendor_order.action_post()
            self.vendor_bill_count += 1

        self.is_vendor_bill_created = True

    def action_vendor_bill(self):
        action = self.env.ref('account.action_move_in_invoice_type')
        vendor_bill_ids = self.env['vendor.bill'].search([('sale_order_id', 'in', self.ids)]).mapped('account_move_id')
        result = action.read()[0]
        result['domain'] = [('id', 'in', vendor_bill_ids.ids)]
        result['res_id'] = False  # Set it to False to prevent opening a specific record immediately
        return result


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    vendors_id = fields.Many2one("res.partner", string="Vendor")
