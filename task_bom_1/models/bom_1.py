from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    manufacture_bill_count = fields.Integer(string="Manufacture Count", compute='_compute_manufacture_count')

    @api.depends('order_line')
    def _compute_manufacture_count(self):
        for order in self:
            manufacture_count = sum(1 for line in order.order_line if line.bom_id)
            order.manufacture_bill_count = manufacture_count

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for order in self:
            for line in order.order_line:
                if line.bom_id:
                    # Create a list to store the move lines
                    move_raw = []

                    # Iterate over the BOM lines to create move lines
                    for bom_line in line.bom_id.bom_line_ids:
                        move_raw.append((0, 0, {
                            'name': bom_line.product_id.name,
                            'product_id': bom_line.product_id.id,
                            'product_uom_qty': 2 * line.product_uom_qty,
                            'product_uom': bom_line.product_uom_id.id,
                        }))

                    # Create the manufacturing order with move lines
                    manufacturing_order = self.env['mrp.production'].create({
                        'product_id': line.product_id.id,
                        'product_uom_qty': line.product_uom_qty,
                        'bom_id': line.bom_id.id,
                        'product_uom_id': line.product_id.uom_id.id,
                        'company_id': order.company_id.id,
                        'product_qty': line.product_uom_qty,
                        'state': 'to_close',
                        'origin': order.name,
                        'move_raw_ids': move_raw,
                    })
                    manufacturing_order._create_update_move_finished()


        return res


    def action_manufacture_order(self):
        action = self.env.ref('mrp.mrp_production_action').read()[0]
        manufacturing_order_ids = self.env['mrp.production'].search([('origin', '=', self.name)])
        result = action.copy()
        result['domain'] = [('id', 'in', manufacturing_order_ids.ids)]
        result['res_id'] = False
        return result






class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    bom_id = fields.Many2one('mrp.bom', string='Bill of Material')
    product_template_id = fields.Many2one(related="product_id.product_tmpl_id",
                                          string="Template Id of Selected Product")
    finished_products = fields.Integer(string="Finished Products",readonly=True)


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    def button_mark_done(self):
        res = super(MrpProduction, self).button_mark_done()
        for production in self:
            sale_order_line = self.env['sale.order.line'].search([
                ('bom_id', '=', production.bom_id.id),
                ('order_id.state', '=', 'sale'),
                ('order_id.state', '!=', 'cancel'),
            ])
            sale_order_line.write({'finished_products': production.product_uom_qty})

        return res