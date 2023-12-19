from odoo import api, fields, models, exceptions
from dateutil.relativedelta import relativedelta


class LoanManage(models.Model):
    _name = 'loan.manage'
    _description = 'loan'

    employee = fields.Many2one('hr.employee', string="Employee")
    date = fields.Date(string='Date', readonly=True, states={'draft': [('readonly', False)]})
    amount = fields.Float(string='Amount', readonly=True, states={'draft': [('readonly', False)]})
    installments = fields.Float(string='Number of installments', readonly=True, states={'draft': [('readonly', False)]})
    loan_ids = fields.One2many('loan.line', 'loan_line_id')
    is_approved = fields.Boolean(string='is approved')
    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('done', 'Done')
    ], string='Status', required=True, readonly=True, copy=False,
        tracking=True, default='draft')

    def action_loan(self):
        if self.state == 'draft':
            # Check if installment lines already exist
            # self.loan_ids.unlink()
            if not self.loan_ids:
                # Check if the installment value is greater than 0
                if self.installments <= 0:
                    raise models.ValidationError("Installments must be greater than 0.")

                # Calculate the installment amount
                installment_amount = self.amount / self.installments
                installment_list = []

                installments_int = int(self.installments)

                current_date = self.date + relativedelta(months=1)

                for i in range(installments_int):
                    installment_date = current_date + relativedelta(months=i)
                    installment_list.append((0, 0, {
                        'date_line': installment_date,
                        'amount_line': installment_amount
                    }))

                self.loan_ids = installment_list

            self.is_approved = True
            self.write({
                'state': "done"
            })
        return

    def action_reset(self):
        self.write({
            'state': "draft"
        })


class LoanLine(models.Model):
    _name = 'loan.line'

    date_line = fields.Date(string='Date', states={'draft': [('readonly', False)]})
    amount_line = fields.Float(string='Amount', states={'draft': [('readonly', False)]})
    loan_line_id = fields.Many2one('loan.manage')


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    def compute_sheet(self):
        for payslip in self:
            res = super(HrPayslip, payslip).compute_sheet()
            total_ded = 0.0
            search_loan = self.env['loan.manage'].search([
                ('employee', '=', payslip.employee_id.id),
                ('state', '=', 'done'),
            ])
            for loan in search_loan.loan_ids:
                if payslip.date_from <= loan.date_line <= payslip.date_to:
                    total_ded += loan.amount_line

            for line in payslip.line_ids:
                if line.code == 'DED':
                    line.amount = total_ded
            return res



