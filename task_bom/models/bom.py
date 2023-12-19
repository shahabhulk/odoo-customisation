from odoo import models, api, SUPERUSER_ID,fields,_
from collections import defaultdict
from odoo.tools import float_compare


class MrpProductionInherit(models.Model):
    _inherit = 'mrp.production'

    source = fields.Char(string='Source',
                         help='Sale Order from which this Manufacturing '
                              'Order created')
    qty_to_produce = fields.Float(string='Quantity to Produce',
                                  help='The number of products to be produced')

    def update_quantity(self):
        """ Method for changing the quantities of components according to
         product quantity """
        for rec in self.move_raw_ids:
            self.write({
                'move_raw_ids': [
                    (1, rec.id, {
                        'product_uom_qty': rec.product_uom_qty *
                                           self.qty_to_produce,
                        # 'quantity_done':rec.product_uom_qty *
                        #                    self.qty_to_produce
                    }),
                ]
            })
        # self.product_qty=self.qty_to_produce
        # self.button_mark_done()


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        """ Create manufacturing order of components in selected BOM """
        for rec in self.order_line:
            check_route = [routes.name for routes in
                           rec.product_template_id.route_ids]
            if rec.bom_id and 'Manufacture' not in check_route:
                move_raw = []
                bom_line = self.env['mrp.bom.line'].search(
                    [('bom_id', '=', rec.bom_id.id)])
                for val in bom_line.mapped('product_id'):
                    product_uom_qty = bom_line.filtered(
                        lambda x: x.product_id.id == val.id).product_qty
                    move_raw.append(
                        (0, 0, {
                            'company_id': self.env.user.company_id.id,
                            'product_id': val.id,
                            'product_uom_qty': product_uom_qty *
                                               rec.product_uom_qty,
                            'name': val.name,
                        }))
                self.env['mrp.production'].sudo().create({
                    'product_id': rec.product_id.id,
                    'product_uom_qty': rec.product_uom_qty,
                    'bom_id': rec.bom_id.id,
                    'user_id': self.env.uid,
                    'product_uom_id': rec.product_id.uom_id.id,
                    'company_id': self.env.user.company_id.id,
                    'state': 'confirmed',
                    'product_qty': rec.product_uom_qty,
                    'source': self.name,
                    'move_raw_ids': move_raw
                })
        return super(SaleOrderInherit, self).action_confirm()


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    bom_id = fields.Many2one('mrp.bom', string='Bill of Material')
    product_template_id = fields.Many2one(related="product_id.product_tmpl_id",
                                          string="Template Id of Selected"
                                                 " Product")

class MrpProductionInherit(models.Model):
    _inherit = 'stock.rule'

    @api.model
    def _run_manufacture(self, procurements):
        sale = []
        productions_values_by_company = defaultdict(list)
        for procurement, rule in procurements:
            if float_compare(procurement.product_qty, 0,
                             precision_rounding=procurement.product_uom.rounding) <= 0:
                # If procurement contains negative quantity, don't create a MO that would be for a negative value.
                continue
            current_sale_order = self.env['sale.order'].search(
                [('name', '=', procurement.origin)])
            if current_sale_order not in sale:
                sale.append(current_sale_order)
        bom_values = self._find_bom_order_line(sale)
        bom_exist = {key: value for key, value in bom_values.items() if value}
        if bom_exist:
            i = 0
            only_bom_record = list(bom_exist.keys())
            for procurement, rule in procurements:
                productions_values_by_company[procurement.company_id.id].append(rule._prepare_mo_vals(*procurement, bom_exist[only_bom_record[i]]))
                i = i + 1
        for company_id, productions_values in productions_values_by_company.items():
            # create the MO as SUPERUSER because the current user may not have the rights to do it (mto product launched by a sale for example)
            productions = self.env['mrp.production'].with_user(
                SUPERUSER_ID).sudo().with_company(company_id).create(
                productions_values)
            productions.filtered(
                self._should_auto_confirm_procurement_mo).action_confirm()
            for production in productions:
                origin_production = production.move_dest_ids and \
                                    production.move_dest_ids[
                                        0].raw_material_production_id or False
                orderpoint = production.orderpoint_id
                if orderpoint and orderpoint.create_uid.id == SUPERUSER_ID and orderpoint.trigger == 'manual':
                    production.message_post(
                        body=_(
                            'This production order has been created from Replenishment Report.'),
                        message_type='comment',
                        subtype_xmlid='mail.mt_note')
                elif orderpoint:
                    production.message_post_with_view(
                        'mail.message_origin_link',
                        values={'self': production, 'origin': orderpoint},
                        subtype_id=self.env.ref('mail.mt_note').id)
                elif origin_production:
                    production.message_post_with_view(
                        'mail.message_origin_link',
                        values={'self': production,
                                'origin': origin_production},
                        subtype_id=self.env.ref('mail.mt_note').id)
        return True

    def _find_bom_order_line(self, sale):
        bom_list = {}
        j = 1
        for rec in sale[0].order_line:
            if rec.bom_id:
                bom_list.update({j: rec.bom_id })
            elif rec.product_template_id.route_ids:
                bom = self.env['mrp.bom'].search([("product_tmpl_id","=",rec.product_template_id.id)], limit=1)
                bom_list.update({j:bom })
            j = j + 1
        return bom_list