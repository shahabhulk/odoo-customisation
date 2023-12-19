from odoo import api, fields, models

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    overtime_pay = fields.Float(string="Overtime Pay", compute='_compute_overtime_pay')
    extra = fields.Integer(string="Extra charge")

    @api.depends('employee_id')
    def _compute_overtime_pay(self):
        for payslip in self:
            total_sum = 0.0
            hourly_wage = 0
            user_attend = self.env['hr.attendance'].search([
                ('employee_id', '=', payslip.employee_id.id),
                ('worked_hours', '>=', 9),
            ])
            total_sum = sum(attendance.worked_hours for attendance in user_attend)
            contract = payslip.contract_id
            if contract:
                hourly_wage = contract.hourly_wage
            # extra = (total_sum % 8) * (hourly_wage)
            extra=(total_sum-(len(user_attend)*8))*(hourly_wage)
            payslip.extra = extra
            payslip.overtime_pay = total_sum-(len(user_attend)*8)

    def compute_sheet(self):
        for payslip in self:
            hourly_wage = 0.0
            # Call the original compute_sheet method
            res=super(HrPayslip, payslip).compute_sheet()

            # Update the "extra" field value in the result dictionary
            user_attend = self.env['hr.attendance'].search([
                ('employee_id', '=', payslip.employee_id.id),
                ('worked_hours', '>=', 8),
            ])
            contract = payslip.contract_id
            if contract:
                hourly_wage = contract.hourly_wage
            user_attend_len = len(user_attend)
            for line in payslip.line_ids:
                if line.code == 'OVER':
                    line.amount = payslip.extra
                    line.extra_hours=(payslip.extra)/hourly_wage
                elif line.code == 'BASIC':
                    line.amount = user_attend_len * 8 * hourly_wage
                elif line.code == 'NET':
                    line.amount = payslip.extra + (user_attend_len * hourly_wage * 8)
            return res

class HrPayslipLine(models.Model):
    _inherit = 'hr.payslip.line'

    extra_hours = fields.Float(string='Extra Hours')

    # def _compute_extra_hours(self):
    #     # user_attend = self.env['hr.attendance'].search([
    #     #     ('worked_hours', '>=', 9)
    #     # ])
    #     for line in self:
    #         if line.code == 'OVER':
    #             line.extra_hours = 0