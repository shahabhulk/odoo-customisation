# from odoo import api, fields, models
#
# class ResUsers(models.Model):
#     _inherit = 'res.users'
#
#     @api.model
#     def create(self, values):
#         user = super(ResUsers, self).create(values)
#
#         # Check if a corresponding record already exists for this user
#         existing_record = self.env['secure.group'].search([('name', '=', user.name)], limit=1)
#
#
#         # If no record exists, create a new one
#         if not existing_record:
#             self.env['secure.group'].create({
#                   # Set the reference to the user
#                 'name': user.name,  # You can set other fields as needed
#             })
#
#         return user
