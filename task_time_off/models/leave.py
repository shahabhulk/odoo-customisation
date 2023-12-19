# from odoo import api, fields, models
# from dateutil.relativedelta import relativedelta
# from datetime import date, timedelta
#
#
# class HrLeave(models.Model):
#     _inherit = 'hr.leave'
#
#     @api.constrains('request_date_from', 'request_date_to', 'employee_id', 'holiday_status_id')
#     def check_leave(self):
#         for rec in self:
#             if rec.employee_id and rec.holiday_status_id.id == 2:
#                 # Calculate the start and end of the month for the request_date_from
#                 start_of_month = rec.request_date_from.replace(day=1)
#                 end_of_month = start_of_month + relativedelta(day=30)
#
#                 # Search for approved leave requests for the same employee within the same month
#                 approved_leave = self.env['hr.leave'].search([
#                     ('request_date_from', '>=', start_of_month),
#                     ('request_date_to', '<=', end_of_month),
#                     ('employee_id', '=', rec.employee_id.id),
#                     ('holiday_status_id', '=', rec.holiday_status_id.id),
#                     ('state', '=', 'validate'),  # Check if the leave request is approved
#                 ])
#
#                 if approved_leave:
#                     raise models.ValidationError(
#                         "You can't apply leave in the same month with an approved leave request")
#
#                 # Check if this is the first leave request in the month
#                 first_leave_request_in_month = not self.env['hr.leave'].search([
#                     ('request_date_from', '>=', start_of_month),
#                     ('request_date_to', '<=', end_of_month),
#                     ('employee_id', '=', rec.employee_id.id),
#                     ('holiday_status_id', '=', rec.holiday_status_id.id),
#                     ('state', '=', 'validate'),  # Exclude canceled leave requests and unapproved ones
#                 ])
#
#                 if not first_leave_request_in_month:
#                     raise models.ValidationError("You can't apply leave more than once in the same month")
from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from datetime import date, timedelta


class HrLeave(models.Model):
    _inherit = 'hr.leave'

    validate_leave_list = []

    @api.constrains('request_date_from', 'request_date_to', 'employee_id', 'holiday_status_id')
    def check_leave(self):
        for rec in self:
            if rec.employee_id.id and rec.holiday_status_id.id == 2:
                # Calculate the start and end of the month for the request_date_from
                start_of_month = rec.request_date_from.replace(day=1)
                end_of_month = start_of_month + relativedelta(day=30)

                # Search for approved leave requests for the same employee within the same month
                validate_leave = self.env['hr.leave'].search([
                    ('request_date_from', '>=', start_of_month),
                    ('request_date_to', '<=', end_of_month),
                    ('employee_id', '=', rec.employee_id.id),
                    ('holiday_status_id', '=', rec.holiday_status_id.id),
                    ('state', '=', 'validate'),  # Check if the leave request is approved
                ])
                print(validate_leave)

                # Append the search results directly to the list