# Copyright (c) 2023, hr and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
import frappe.utils


class Employee(Document):
	def validate(self):
		self.cal_age()
		self.check_mobile()
		self.add_full_name()
		self.check_status()
		self.check_education()

	def cal_age(self):
		if self.date_of_birth:
			age_diff = frappe.utils.date_diff(frappe.utils.today(), self.date_of_birth) // 365
			self.age = age_diff
		else:
			frappe.throw("Please add DOB")

	def add_full_name(self):
		if self.first_name and self.middle_name and self.last_name:
			self.full_name = self.first_name + " " + self.middle_name + " " + self.last_name
		else:
			frappe.throw("Please, add all name component")

	def check_mobile(self):
		if self.mobile:
			if len(self.mobile) != 10:
				frappe.throw("Mobile number should be 10 digits")

			if self.mobile.startswith("059"):
				pass
			else:
				frappe.throw("Mobile number should starts with 059")
		else:
			frappe.throw("Please add mobile number")

	def check_education(self):
		count_employee_education = 0
		for x in self.employee_education:
			count_employee_education = count_employee_education + 1

		if count_employee_education < 2:
			frappe.throw("Employee Education should at lease be 2")

	def check_status(self):
		if self.status == "Active" and self.age >= 60:
			frappe.throw("Active Employee can't be over 60")
