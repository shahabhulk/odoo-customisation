from odoo import api, fields, models

class SameBarcode(models.Model):
    _inherit = "product.template"

    @api.depends('barcode')
    def barcode_num(self):
        for record in self:
            duplicate_records = self.env['product.template'].search([
                ('barcode', '=', record.barcode),
                ('id', '!=', record.id)
            ])
            if duplicate_records:
                # Bypass constraints and access rights during the write operation
                self.write({'barcode': record.barcode})
                # Optionally log a message or perform additional actions

                # No need to remove the validation error as it won't be triggered due to sudo
