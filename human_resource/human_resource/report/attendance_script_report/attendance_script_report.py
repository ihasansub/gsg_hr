# Copyright (c) 2023, hr and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns, data = [], []
	data = get_all_attendance(filters)
	columns = get_columns()
	return columns, data

def get_all_attendance(filters):
	return frappe.db.get_all("Attendance", ['employee_name', 'attendance_date', 'status', 'check_in', 'check_out', 'work_hours', 'late_hours'], filters=filters)

def get_columns():
	columns = [
		# {'fieldname': 'employee', 'label': 'Employee', 'fieldtype': 'Data'},
		{'fieldname': 'employee_name', 'label': 'Employee Name', 'fieldtype': 'Data'},
		{'fieldname': 'attendance_date', 'label': 'Attendance Date', 'fieldtype': 'Date'},
		{'fieldname': 'status', 'label': 'Status', 'fieldtype': 'Data'},
		{'fieldname': 'check_in', 'label': 'Check In', 'fieldtype': 'Time'},
		{'fieldname': 'check_out', 'label': 'Check Out', 'fieldtype': 'Time'},
		{'fieldname': 'work_hours', 'label': 'Work Hours', 'fieldtype': 'Float'},
		{'fieldname': 'late_hours', 'label': 'Late Hours', 'fieldtype': 'Float'},
	]
	return columns
