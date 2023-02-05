# api
import frappe
from frappe import utils


@frappe.whitelist()
def create_attendance(attendance_date, check_in, check_out):
    qry_employee = frappe.db.sql("""select name from `tabEmployee` where link_user = %s""", (frappe.session.user), as_dict=1)
    employee = qry_employee[0].name
    frappe.db.sql(""" update tabAttendance set employee = %s, attendance_date = %s, check_in = %s, check_out = %s """,
                  (employee, utils.getdate(attendance_date), utils.get_time(check_in), utils.get_time(check_out)))

    frappe.db.commit
