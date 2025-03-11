from odoo import http
from odoo.http import request
from datetime import datetime, timedelta


class AutomobileFinanceCustom(http.Controller):

    @http.route('/get_finance_records_by_date', type='json', auth='user')
    def get_finance_records_by_date(self, **rec):
        rec = request.httprequest.get_json()
        start_date = rec.get('start_date')
        end_date = rec.get('end_date')

        if not start_date or not end_date:
            return {'success': False, 'message': 'Missing start_date or end_date'}

        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            return {'success': False, 'message': 'Invalid date format. Use YYYY-MM-DD'}

        income_records = request.env['automobile.finance.income'].sudo().search([
            ('date', '>=', start_date),
            ('date', '<=', end_date)
        ])
        income_data = [
            {'id': rec.id, 'date': rec.date, 'name': rec.customer_name_id.name, 'total_amount': rec.total_amount} for
            rec in income_records
        ]
        expense_records = request.env['automobile.finance.expense'].sudo().search([
            ('date', '>=', start_date),
            ('date', '<=', end_date)
        ])
        expense_data = [
            {'id': rec.id, 'date': rec.date, 'total_amount': rec.total_amount} for rec in expense_records
        ]

        return {
            'success': True,
            'income_records': income_data,
            'expense_records': expense_data
        }

    @http.route('/income_overview_last_3_months', type='json', auth='user')
    def income_overview_last_3_months(self):
        today = datetime.today()
        three_months_ago = today - timedelta(days=90)
        income_records = request.env['automobile.finance.income'].sudo().search([
            ('date', '>=', three_months_ago.strftime('%Y-%m-%d')),
            ('date', '<=', today.strftime('%Y-%m-%d'))
        ])
        income_summary = {}
        for rec in income_records:
            month = rec.date.strftime('%Y-%m')
            if month not in income_summary:
                income_summary[month] = 0
            income_summary[month] += rec.total_amount

        response_data = [{'month': month, 'total_income': total} for month, total in sorted(income_summary.items())]

        return {
            'success': True,
            'message': 'Income overview for the last 3 months',
            'data': response_data
        }

    @http.route('/get_income_by_category', type='json', auth='user', methods=['POST'])
    def get_income_by_category(self):
        income_records = request.env['automobile.finance.income.line'].sudo().search([])
        category_income = {}

        for record in income_records:
            category = record.category_id  # Selection field
            amount = record.amount

            if category in category_income:
                category_income[category] += amount
            else:
                category_income[category] = amount


        result = [{'category': cat, 'total_income': income} for cat, income in category_income.items()]

        return {'success': True, 'data': result}

    @http.route('/get_expense_by_category', type='json', auth='user', methods=['POST'])
    def get_expense_by_category(self):
        expense_records = request.env['automobile.finance.expense.line'].sudo().search([])
        category_expense = {}
        for record in expense_records:
            category = record.category_id
            amount = record.amount

            if category in category_expense:
                category_expense[category] += amount
            else:
                category_expense[category] = amount


        result = [{'category': cat, 'total_expense': expense} for cat, expense in category_expense.items()]

        return {'success': True, 'data': result}
