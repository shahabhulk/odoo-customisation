from odoo import api, fields, models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _action_cancel(self):

        for rec in self:
            res = super(SaleOrder, rec)._action_cancel()
            for picking in rec.picking_ids:
                return_picking = picking.create({
                    'origin': picking.name,
                    'sale_id': rec.id,
                    'partner_id': rec.partner_id.id,
                    'picking_type_id': 6,
                    'location_id': picking.location_dest_id.id,
                    'location_dest_id': picking.location_id.id,
                })
                for move in picking.move_ids:
                    return_move = move.copy({
                        'picking_id': return_picking.id,
                        'location_id': picking.location_dest_id.id,
                        'location_dest_id': picking.location_id.id,
                    })
                    for move_line in move.move_line_ids:
                        return_move_line = move_line.copy({
                            'move_id': return_move.id,
                            'lot_id': move_line.lot_id.id,
                            'qty_done': move_line.qty_done,
                            'location_id': picking.location_dest_id.id,
                            'location_dest_id': picking.location_id.id,
                            'picking_id': return_picking.id,
                        })

                return_picking.action_confirm()
                return_picking.action_assign()
                return_picking.button_validate()

            return res
