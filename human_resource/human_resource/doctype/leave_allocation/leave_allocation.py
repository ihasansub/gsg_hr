# Copyright (c) 2023, hr and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
import frappe.utils
from frappe import _


class LeaveAllocation(Document):

	def validate(self):
		self.leave_allocation_validation()

	def leave_allocation_validation(self):
		if self.employee and self.from_date and self.to_date and self.leave_type:
			leave_allocated = frappe.db.sql(""" select * from `tabLeave Allocation` 
			where employee = %s and leave_type = %s and from_date <= %s and to_date >= %s """,
											(self.employee, self.leave_type, self.from_date, self.to_date), as_dict=1)

			if leave_allocated:
				frappe.throw(_("Employee has leave allocation for selected period and leave type"))

		else:
			frappe.throw(_("please fill all data"))