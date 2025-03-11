from odoo import http
from odoo.http import request


class AutomobileFinance(http.Controller):


    @http.route('/create_income_finance', type='json', auth='user')
    def create_finance_income(self, **rec):
        if request.httprequest.content_type == 'application/json':
            customer_id = rec.get('name')
            if customer_id:
                vals = {
                    'customer_name_id': customer_id
                }
                new_rec = request.env['automobile.finance.income'].sudo().create(vals)
                return {
                    'success': True,
                    'message': 'Income record created successfully',
                    'data': {'id': new_rec.id}
                }
            else:
                return {'success': False, 'message': 'Missing customer ID'}

    @http.route('/get_income_finance', type='json', auth='user')
    def get_finance_income(self, **rec):
        income_finance_rec = request.env['automobile.finance.income'].search([])
        income_finance = []
        for rec in income_finance_rec:
            vals = {
                'id': rec.id,
                'name': rec.customer_name_id.name
            }
            income_finance.append(vals)
        data = {'status': 200, 'response': income_finance, 'message': 'Success'}
        return data

    @http.route('/create_expense_finance', type='json', auth='user')
    def create_finance_expense(self, **rec):
        if request.httprequest.content_type == 'application/json':
            company_id = rec.get('company_id')
            if not company_id:
                return {'success': False, 'message': 'Missing company ID'}


            expense_record = request.env['automobile.finance.expense'].sudo().create({
                'company_id': company_id
            })

            # Create Expense Lines
            expense_lines = rec.get('expense_lines', [])
            for line in expense_lines:
                request.env['automobile.finance.expense.line'].sudo().create({
                    'expense_id': expense_record.id,
                    'category_id': line.get('category_id'),
                    'amount': line.get('amount'),
                    'description': line.get('description'),
                })

            return {
                'success': True,
                'message': 'Expense record created successfully',
                'data': {'id': expense_record.id}
            }
        else:
            return {'success': False, 'message': 'Invalid content type. Use application/json'}

    @http.route('/get_expense_finance', type='json', auth='user')
    def get_finance_expense(self, **rec):
        expense_finance_rec = request.env['automobile.finance.expense'].search([])
        expense_finance = []
        for rec in expense_finance_rec:
            vals = {
                'id': rec.id,
                'date': rec.date,
                'total_amount': rec.total_amount
            }
            expense_finance.append(vals)
        data = {'status': 200, 'response': expense_finance, 'message': 'Success'}
        return data

    @http.route('/update_income_finance', type='json', auth='user', methods=['POST'])
    def update_finance_income(self,**rec):
        rec = request.httprequest.get_json()


        income_id = rec.get('income_id')
        if not income_id:
            return {'success': False, 'message': 'Missing income ID'}

        income_record = request.env['automobile.finance.income'].sudo().browse(income_id)
        if not income_record.exists():
            return {'success': False, 'message': 'Income record not found'}


        income_record.sudo().write({
            'customer_name_id': rec.get('customer_name_id', income_record.customer_name_id.id),
            'date': rec.get('date', income_record.date),
        })


        if 'income_lines' in rec:
            income_record.income_line_ids.unlink()
            for line in rec['income_lines']:
                request.env['automobile.finance.income.line'].sudo().create({
                    'income_id': income_id,
                    'category_id': line.get('category_id'),
                    'amount': line.get('amount'),
                    'description': line.get('description', ''),
                })

        return {'success': True, 'message': 'Income record updated successfully'}

    @http.route('/update_expense_finance', type='json', auth='user')
    def update_finance_expense(self, **rec):
        rec = request.httprequest.get_json()
        expense_id = rec.get('expense_id')
        company_id = rec.get('company_id')
        expense_lines = rec.get('expense_lines', [])

        if not expense_id:
            return {'success': False, 'message': 'Missing expense ID'}

        expense_rec = request.env['automobile.finance.expense'].sudo().browse(expense_id)
        if not expense_rec.exists():
            return {'success': False, 'message': 'Expense record not found'}

        if company_id:
            expense_rec.write({'company_id': company_id})

        if expense_lines:
            expense_rec.expense_line_ids.unlink()  # Remove existing lines
            for line in expense_lines:
                request.env['automobile.finance.expense.line'].sudo().create({
                    'expense_id': expense_rec.id,
                    'category_id': line.get('category_id'),
                    'amount': line.get('amount'),
                    'description': line.get('description'),
                })

        return {'success': True, 'message': 'Expense record updated successfully'}

    @http.route('/delete_income_finance', type='json', auth='user')
    def delete_finance_income(self, **rec):
        rec = request.httprequest.get_json()
        income_id = rec.get('income_id')
        if not income_id:
            return {'success': False, 'message': 'Missing income ID'}

        income_rec = request.env['automobile.finance.income'].sudo().browse(income_id)
        if income_rec.exists():
            income_rec.unlink()
            return {'success': True, 'message': 'Income record deleted successfully'}
        else:
            return {'success': False, 'message': 'Income record not found'}

    @http.route('/delete_expense_finance', type='json', auth='user')
    def delete_finance_expense(self, **rec):
        rec = request.httprequest.get_json()
        expense_id = rec.get('expense_id')
        if not expense_id:
            return {'success': False, 'message': 'Missing expense ID'}

        expense_rec = request.env['automobile.finance.expense'].sudo().browse(expense_id)
        if expense_rec.exists():
            expense_rec.unlink()
            return {'success': True, 'message': 'Expense record deleted successfully'}
        else:
            return {'success': False, 'message': 'Expense record not found'}


print(AutomobileFinance.__dict__)