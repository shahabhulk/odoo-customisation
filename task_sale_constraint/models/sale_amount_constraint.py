from odoo import api, fields, models

# class SaleOrder(models.Model):
#     _inherit = "sale.order"
#
#     amount=fields.Integer(string="Amount")
#
#     @api.constrains("amount")
#     def amount_constrain(self):
#         for each in self:
#             if(each.amount>=100):
#                 pass
#             else:
#                 raise models.ValidationError("Should be greater than or equal to 100")

from odoo import api, models, fields


class SaleOrder(models.Model):
    _inherit = "sale.order"

    amount = fields.Integer(string="Amount")

    @api.model
    # logic implemented only while creating the record
    def create(self, vals):
        value = vals['amount']
        if value < 100:
            raise models.ValidationError("Amount should be greater than 100")
        return super(SaleOrder, self).create(vals)

    def write(self, vals):
        value = vals['amount']
        if value < 100:
            raise models.ValidationError("Amount should be greater than 100")
        return super(SaleOrder, self).write(vals)

