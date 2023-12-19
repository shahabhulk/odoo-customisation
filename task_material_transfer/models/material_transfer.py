from odoo import api, fields, models


class MaterialTransfer(models.Model):
    _name = "material.transfer"
    _description = "Material Transfer"

    material_from_id = fields.Many2one('stock.location', string="From")
    material_to_id = fields.Many2one('stock.location', string="To")
    picking_id = fields.Many2one('stock.picking', string='Picking')
    product_ids = fields.One2many('transfer.line', 'transfer_id', string="Products")
    transfer_count = fields.Integer(compute="_compute_transfer_order", string="count Transfer order")

    def action_transfer_value(self):
        transfer_order_lines = []
        for line in self.product_ids:
            transfer_line_vals = {
                'name': line.product_id.name,  # Example: Set the name field
                'product_id': line.product_id.id,
                'product_uom_qty': line.quantity,
                'location_id': self.material_from_id.id,  # Set the source location
                'location_dest_id': self.material_to_id.id,
                'picking_type_id': 5,  # Replace with the appropriate picking_type_id
                'quantity_done': line.quantity
            }
            transfer_order_lines.append((0, 0, transfer_line_vals))

        transfer_vals = {
            'location_id': self.material_from_id.id,
            'location_dest_id': self.material_to_id.id,
            'picking_type_id': 5,  # Replace with the appropriate picking_type_id
            'move_ids_without_package': transfer_order_lines,
        }
        transfer_order = self.env['stock.picking'].create(transfer_vals)
        transfer_order.action_confirm()
        transfer_order.button_validate()
        self.picking_id = transfer_order
    def transfer_order(self):
        action = self.env.ref('stock.action_picking_tree_all')
        result = action.read()[0]
        result['domain'] = [('id', '=', self.picking_id.id)]
        result['res_id'] = self.picking_id.id

        return result

    @api.depends('picking_id')
    def _compute_transfer_order(self):
        for rec in self:
            rec.transfer_count = len(rec.picking_id)


class TransferLine(models.Model):
    _name = 'transfer.line'
    _description = 'Transfer Line'

    product_id = fields.Many2one('product.product', string="Product")
    quantity = fields.Float(string="Quantity")
    transfer_id = fields.Many2one('material.transfer', string="Transfer")
    on_hand_quantity = fields.Float(string="On Hand Quantity", compute="_compute_on_hand_quantity")

    @api.depends('product_id', 'transfer_id.material_from_id')
    def _compute_on_hand_quantity(self):
        for rec in self:
            if rec.product_id and rec.transfer_id.material_from_id:
                product = rec.product_id
                location_id = rec.transfer_id.material_from_id
                stock_qty_obj = self.env['stock.quant']
                stock_qty = stock_qty_obj.search(
                    [('product_id', '=', product.id), ('location_id', '=', location_id.id)])  # Limit to 1 record
                # a = stock_qty.quantity-rec.quantity
                rec.on_hand_quantity=stock_qty.quantity

            else:
                rec.on_hand_quantity = 0.0

    # @api.depends('product_id', 'quantity', 'transfer_id.material_from_id')
    # def _compute_available_quantity(self):
    #     for rec in self:
    #         if rec.product_id and rec.transfer_id.material_from_id:
    #             # Compute the available quantity based on the selected product and quantity
    #             product = rec.product_id
    #             quantity_needed = rec.quantity
    #             available_quantity = 0.0
    #
    #             # Search for stock.quant records in the source location
    #             quants = self.env['stock.quant'].search([
    #                 ('location_id', '=', rec.transfer_id.material_from_id.id),
    #                 ('product_id', '=', product.id),
    #             ])
    #
    #             # Calculate the available quantity from the quants
    #             for quant in quants:
    #                 available_quantity += quant.quantity
    #
    #             # Deduct the quantity needed from the available quantity
    #             available_quantity -= quantity_needed
    #
    #             rec.available_quantity = available_quantity
    #         else:
    #             rec.available_quantity = 0.0
    #
    # @api.constrains('product_id', 'quantity')
    # def _compute_available_quantity(self):
    #     for rec in self:
    #         x=self.env['stock.quant'].search(['location_id','=','material_from_id'])
    #         for item in x:
    #            if (rec.product_id.id==item.product_id.id):
    #                rec.available_quantity=item.quantity-rec.quantity
    #

