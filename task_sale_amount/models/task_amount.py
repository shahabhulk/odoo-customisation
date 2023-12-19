from odoo import api, models, fields


class SaleOrder(models.Model):
    _inherit = "sale.order"

    sale_amount = fields.Integer(string="Sale Amount")
    ticker = fields.Boolean(string="500 above", compute="_compute_ticker")

    @api.onchange("sale_amount")
    def change_sale_amount(self):
        for line in self.order_line:
            if (line.price_subtotal >= self.sale_amount):
                line.checker = True
            else:
                line.checker = False

    @api.depends("amount_total")
    def _compute_ticker(self):
        for order in self:
            if (order.amount_total >= 500):
                order.ticker = True
            else:
                order.ticker = False


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    checker = fields.Boolean(string="Checker")

# class SaleOrder(models.Model):
#     _inherit = "sale.order"
#
#     sale_amount = fields.Integer(string="sale amount")
#


# class SaleOrderLine(models.Model):
#     _inherit = "sale.order.line"
#
#     checker = fields.Boolean(string="Checker", compute="_compute_checker")
#
#     @api.depends('order_id.sale_amount', 'price_subtotal')
#     def _compute_checker(self):
#         for line in self:
#             if line.order_id.sale_amount and line.price_subtotal >= line.order_id.sale_amount:
#                 line.checker = True
#             else:
#                 line.checker = False
