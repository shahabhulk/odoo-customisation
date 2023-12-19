from odoo import api, fields, models

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    employee_id = fields.Many2one('hr.employee', string="Employee")



    # @api.model
    # def create(self, vals):
    #     # Check if the user is in the 'group_restrict_po'
    #     if self.env.user.has_group('task_purchase_security.group_restrict_po'):
    #         raise PermissionError("You do not have permission to create purchase orders.")
    #
    #     return super(PurchaseOrder, self).create(vals)
    #
    #
    # def write(self, vals):
    #     # Check if the user is in the 'group_restrict_po'
    #     if self.env.user.has_group('task_purchase_security.group_restrict_po'):
    #         raise PermissionError("You do not have permission to edit purchase orders.")
    #
    #     return super(PurchaseOrder, self).write(vals)
