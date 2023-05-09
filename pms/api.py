import frappe
from frappe.utils import add_days, today, date_diff, getdate, add_months
import calendar


@frappe.whitelist()
def getDateMonthDiff(rent_start_date, rent_end_date, month_factor):
    month_count = 0
    no_month = 0
    month_float = 0
    # frappe.msgprint("start_date: " + str(start_date) + "  --- end_date: " + str(end_date))
    while rent_start_date <= rent_end_date:
        period_end_date = add_days(add_months(rent_start_date, month_factor), -1)
        # frappe.msgprint("start_date: " + str(start_date) + "  --- period_end_date: " + str(period_end_date))
        if period_end_date <= rent_end_date:
            # add month and set new start date to calculate next month_count
            month_count = month_count + month_factor
            rent_start_date = add_months(rent_start_date, month_factor)
        else:
            # find last number of days
            days = float(
                date_diff(getdate(rent_end_date), getdate(add_months(rent_start_date, no_month)))
                + 1
            )
            # msg = "no_month = 0 so Days calculated: " + str(days) + " between " + str(start_date) + " and " + str(end_date)
            # frappe.msgprint(msg)
            # start_date to cater for correct number of days in month in case the start date is feb
            no_days_in_month = float(
                calendar.monthrange(
                    getdate(rent_start_date).year, getdate(rent_start_date).month
                )[1]
            )
            # msg = "no_month = 0 so No of Days calculated: " + str(no_days_in_month) + " between " + str(start_date) + " and " + str(end_date)
            # frappe.msgprint(msg)
            month_float = days / no_days_in_month
            # frappe.msgprint("month_float = " + str(month_float) + " for days = " + str(days) + " and total number of days = " + str(no_days_in_month))
            rent_start_date = add_months(rent_start_date, month_factor)
    month_count = month_count + no_month + month_float
    return month_count



# def invoice_schedule(
#     date,
#     item,
#     paid_by,
#     item_name,
#     name,
#     qty,
#     rate,
#     idx,
#     # currency=None,
#     document_type="Sales Invoice"
# ):
#     date_to_invoice = add_days(date, -1 * (0))
#     payment_schedule=frappe.get_doc(
#         dict(
#             idx=idx,
#             doctype="Lease Payment Schedule",
#             parent=name,
#             parentfield="lease_payment_schedule",
#             parenttype="lease_contract",
#             date_to_invoice=date_to_invoice,
#             # schedule_start_date=date,
#             lease_item=item,
#             paid_by=paid_by,
#             lease_item_name=item_name,
#             qty=qty,
#             rate=rate,
#             # currency=currency,
#             document_type=document_type
#         )
#     )
#     payment_schedule.insert(ignore_permissions=True)
#     # return payment_schedule
#     # frappe.msgprint("Orientation meeting created")