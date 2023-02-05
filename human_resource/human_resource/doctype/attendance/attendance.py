# Copyright (c) 2023, hr and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime, timedelta
from frappe import utils


class Attendance(Document):

	def validate(self):
		self.cal_work_hours()
		self.update_status()

	def cal_work_hours(self):
		settings = frappe.get_doc("Attendance Settings")
		not_late = datetime.strptime(settings.start_time, '%H:%M:%S') + timedelta(minutes=settings.late_entry_grace_period)
		not_early = datetime.strptime(settings.end_time, '%H:%M:%S') - timedelta(minutes=settings.early_exit_grace_period)
		late_entry = 0
		early_exit = 0
		if datetime.strptime(self.check_in, '%H:%M:%S') <= not_late:
			checkin = settings.start_time
		else:
			checkin = self.check_in
			late_entry = utils.time_diff_in_hours(self.check_in, settings.start_time) - settings.late_entry_grace_period/60

		if datetime.strptime(self.check_out, '%H:%M:%S') >= not_early:
			checkout = settings.end_time
		else:
			checkout = self.check_out
			early_exit = utils.time_diff_in_hours(settings.end_time, self.check_out) - settings.early_exit_grace_period/60

		workhours = utils.time_diff_in_hours(checkout, checkin)
		self.work_hours = workhours

		if late_entry < 0:
			late_entry = 0

		if early_exit < 0:
			early_exit = 0
			
		late = late_entry + early_exit
		self.late_hours = late

	def update_status(self):
		absent_lvl = frappe.db.get_single_value("Attendance Settings", "working_hours_threshold_for_absent")
		if absent_lvl > 0 and self.work_hours < absent_lvl:
			self.status = "Absent"
		else:
			self.status = "Present"
