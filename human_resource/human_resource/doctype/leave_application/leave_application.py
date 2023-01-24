# Copyright (c) 2023, hr and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
import frappe.utils
from frappe import _

class LeaveApplication(Document):
	def validate(self):
		self.set_total_leave_days()
		self.get_total_leave_allocated()
		self.check_balance_leave()

	def on_submit(self):
		self.update_leave_allocated()

	def on_cancel(self):
		self.refund_cancel_leave()

	def set_total_leave_days(self):
		if self.to_date and self.from_date:
			total_leave_day = frappe.utils.date_diff(self.to_date, self.from_date)
			if total_leave_day>=0:
				self.total_leave_days = total_leave_day + 1

	def get_total_leave_allocated(self):
		if self.employee and self.from_date and self.to_date and self.leave_type:
			leave_allocated = frappe.db.sql(""" select * from `tabLeave Allocation` 
			where employee = %s and leave_type = %s and from_date <= %s and to_date >= %s """,
			(self.employee, self.leave_type, self.from_date, self.to_date), as_dict=1)

			if leave_allocated:
				self.leave_balance_before_application = str(leave_allocated[0].total_leaves_allocated)

	def check_balance_leave(self):
		if self.total_leave_days and self.leave_balance_before_application:
			if float(self.total_leave_days) > float(self.leave_balance_before_application):
				frappe.throw(_("Insufficient leave balance of ") + self.leave_type)

	def update_leave_allocated(self):
		new_leaves_allocated = float(self.leave_balance_before_application) - float(self.total_leave_days)
		frappe.db.sql(""" update `tabLeave Allocation` set total_leaves_allocated = %s
			where employee = %s and leave_type = %s and from_date <= %s and to_date >= %s """,
			(new_leaves_allocated, self.employee, self.leave_type, self.from_date, self.to_date), as_dict=1)
		frappe.db.commit

	def refund_cancel_leave(self):
		if self.employee and self.from_date and self.to_date and self.leave_type:
			leave_allocated = frappe.db.sql(""" select * from `tabLeave Allocation` 
			where employee = %s and leave_type = %s and from_date <= %s and to_date >= %s """,
											(self.employee, self.leave_type, self.from_date, self.to_date), as_dict=1)

			if leave_allocated:
				current_leave_balance = str(leave_allocated[0].total_leaves_allocated)

		new_leaves_allocated = float(current_leave_balance) + float(self.total_leave_days)
		frappe.db.sql(""" update `tabLeave Allocation` set total_leaves_allocated = %s
					where employee = %s and leave_type = %s and from_date <= %s and to_date >= %s """,
					  (new_leaves_allocated, self.employee, self.leave_type, self.from_date, self.to_date), as_dict=1)
		frappe.db.commit
