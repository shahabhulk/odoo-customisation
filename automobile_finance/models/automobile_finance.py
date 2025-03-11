from odoo import models, fields, api


class AutomobileFinanceIncome(models.Model):
    _name = "automobile.finance.income"
    _description = "Automobile Finance - Income"
    _order = "date desc"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'customer_name_id'

    customer_name_id = fields.Many2one(
        "res.partner",
        string="Customer",
        domain=[("is_company", "=", False)]
    )
    date = fields.Date(string="Date", required=True, default=fields.Date.context_today)
    sequence_income = fields.Char(string="Finance Income", readonly=True)
    total_amount = fields.Float(
        string="Total Amount", compute="_compute_total_amount", store=True
    )
    income_line_ids = fields.One2many(
        "automobile.finance.income.line", "income_id", string="Income Lines"
    )
    company_id = fields.Many2one(
        "res.company", string="Company", required=True, default=lambda self: self.env.company
    )

    @api.model
    def create(self, vals):
        vals['sequence_income'] = self.env['ir.sequence'].next_by_code('finance.income') or '/'
        return super(AutomobileFinanceIncome, self).create(vals)


    @api.depends("income_line_ids.amount")
    def _compute_total_amount(self):
        for record in self:
            record.total_amount = 0
            for line in record.income_line_ids:
                record.total_amount += line.amount


class AutomobileFinanceIncomeLine(models.Model):
    _name = "automobile.finance.income.line"

    sequence = fields.Integer(default=10)
    income_id = fields.Many2one("automobile.finance.income", string="Income Record", required=True, ondelete="cascade")
    category_id = fields.Selection(
        [
            ("service", "Service"),
            ("spare_parts", "Spare Parts"),
            ("insurance", "Insurance"),
            ("others", "Others"),
        ],
        string="Category",
        required=True,
    )
    amount = fields.Float(string="Amount", required=True)
    description = fields.Text(string="Description")


class AutomobileFinanceExpense(models.Model):
    _name = "automobile.finance.expense"
    _description = "Automobile Finance Expense"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "date desc"
    _rec_name = 'date'

    sequence_expense = fields.Char(string="Finance Expense", readonly=True)
    date = fields.Date(string="Date", required=True, default=fields.Date.context_today)
    total_amount = fields.Float(string="Total Amount", compute="_compute_total_amount", store=True)
    company_id = fields.Many2one(
        "res.company", string="Company", required=True, default=lambda self: self.env.company
    )
    expense_line_ids = fields.One2many(
        "automobile.finance.expense.line", "expense_id", string="Expense Lines"
    )

    @api.model
    def create(self, vals):
        vals['sequence_expense'] = self.env['ir.sequence'].next_by_code('finance.expense') or '/'
        return super(AutomobileFinanceExpense, self).create(vals)

    @api.depends("expense_line_ids.amount")
    def _compute_total_amount(self):
        for record in self:
            record.total_amount = sum(record.expense_line_ids.mapped("amount"))


class AutomobileFinanceExpenseLine(models.Model):
    _name = "automobile.finance.expense.line"
    _description = "Expense Line"

    sequence = fields.Integer(default=10)
    expense_id = fields.Many2one(
        "automobile.finance.expense", string="Expense Reference", required=True, ondelete="cascade"
    )
    amount = fields.Float(string="Amount", required=True)
    category_id = fields.Selection(
        [
            ("salary", "Salary"),
            ("rent", "Rent"),
            ("maintenance", "Maintenance"),
            ("utilities", "Utilities"),
            ("others", "Others"),
        ],
        string="Category",
        required=True,
    )
    description = fields.Text(string="Description")
