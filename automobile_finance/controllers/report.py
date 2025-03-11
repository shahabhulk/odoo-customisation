from odoo import http
from odoo.http import request
import base64
from datetime import datetime
from werkzeug.utils import secure_filename
from werkzeug.wrappers import Response

class FinanceReportController(http.Controller):

    @http.route('/get_finance_report_pdf', type='http', auth='user')
    def get_finance_report_pdf(self, start_date=None, end_date=None):
        if not start_date or not end_date:
            return Response("Missing start_date or end_date", status=400)

        # Convert string dates to datetime objects
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        # Search for finance income records in the given date range
        finance_records = request.env['automobile.finance.income'].sudo().search([
            ('date', '>=', start_date),
            ('date', '<=', end_date)
        ])

        if not finance_records:
            return Response("No records found for the given date range", status=404)

        # Generate PDF
        pdf_content, _ = request.env.ref('automobile_finance.finance_report_template')._render_qweb_pdf(finance_records.ids)

        # Encode PDF to base64
        pdf_base64 = base64.b64encode(pdf_content)

        # Create response
        response = request.make_response(pdf_content, headers=[
            ('Content-Type', 'application/pdf'),
            ('Content-Disposition', 'attachment; filename="Finance_Report.pdf"')
        ])
        return response
