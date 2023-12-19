from odoo import api, models, fields

class SaleOrder(models.Model):
    _inherit = "sale.order"

    amount=fields.Integer(string="amount")
    ticker = fields.Boolean(string="500 above")

    def update_ticker(self):
        sale_orders = self.env['sale.order'].search([])
        for each in sale_orders:
            if(each.amount_total>=500):
                each.ticker=True
            else:
                each.ticker=False

    @api.model
    def filter_above_500(self, domain, context=None):
        domain += [('amount_total', '>=', 500)]
        return domain



# class SaleOrderLine(models.Model):
#     _inherit = "sale.order.line"
#
#     checker = fields.Boolean(string="Checker")
