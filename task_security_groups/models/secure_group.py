from odoo import api, fields, models

class SecureGroup(models.Model):
    _name = "secure.group"
    _description = "Security Groups"

    name = fields.Char(string="Name")
    sequence = fields.Char(string="Sequence", readonly=True, default=" ")

    def secure_create(self):
        user = self.env['res.users'].search([('name', '=', self.name)], limit=1)
        if user:
            self.name = user.name

    # @api.constrains("name")
    # def _sequence_generate(self):
    #     for rec in self:
    #         if rec.name and rec.sequence == " ":
    #             seq = self.env['ir.sequence'].next_by_code('secure.group.sequence')
    #             rec.sequence = seq
