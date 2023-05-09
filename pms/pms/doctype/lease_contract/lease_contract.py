# Copyright (c) 2023, enfono and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import add_days, today, getdate, add_months, get_datetime, now
from dateutil.relativedelta import relativedelta


from pms.api import getDateMonthDiff

class LeaseContract(Document):
	
	def validate(self):
		

		if self.agreement_status=="Signed agreement received":
			# self.validate_agreement_received()
			unit=frappe.get_doc("Unit",self.unit_name)
			unit.status="Leased"
			unit.save()

			tenant_doc=frappe.get_doc("Tenant",self.lease_customer)
			tenant_doc.unit=self.unit_name
			tenant_doc.rent_start_date=self.rent_start_date
			tenant_doc.rent_end_date=self.rent_end_date
			tenant_doc.agreement_current_status=self.agreement_status
			tenant_doc.save()

		
		elif self.agreement_status=="Agreement Cancelled":
			self.validate_agreement_cancelled()
			unit=frappe.get_doc("Unit",self.unit_name)
			unit.status="Available"
			unit.save()


			tenant_doc=frappe.get_doc("Tenant",self.lease_customer)
			tenant_doc.unit=""
			tenant_doc.rent_start_date=""
			tenant_doc.rent_end_date=""
			tenant_doc.agreement_current_status=self.agreement_status
			tenant_doc.save()


	# def validate_agreement_received(self):

	# 	unit=frappe.get_doc("Unit",self.unit_name)
	# 	if unit.status=="Leased":
	# 		frappe.throw("This Unit is Already Leased")


	def validate_agreement_cancelled(self):

		unit=frappe.get_doc("Unit",self.unit_name)
		if unit.status=="Available":
			frappe.throw("Unit Agreement cannot be cancelled without having proper leasing agreement ")


@frappe.whitelist()
def make_lease_payment_schedule(leasedoc):
    lease_contract = frappe.get_doc("Lease Contract", str(leasedoc))

    lease_payment_schedule = []

    item_payment_frequency = {
        "Monthly": 1.00,
        "Quarterly": 3.00,
        "6 months": 6.00,
        "Annually": 12.00
    }

    for lease_item in lease_contract.lease_item:
        frequency_factor = item_payment_frequency.get(lease_item.frequency)
        invoice_qty = float(frequency_factor)

        rent_start_date = lease_contract.rent_start_date
        rent_end_date = lease_contract.rent_end_date
        # lease_period_months = (rent_end_date.year - rent_start_date.year) * 12 + rent_end_date.month - rent_start_date.month + 1

        while rent_end_date >= rent_start_date:
            invoice_period_end = add_days(add_months(rent_start_date, frequency_factor), -1)
            if invoice_period_end > rent_end_date:
                invoice_qty = getDateMonthDiff(rent_start_date, rent_end_date, 1)

            lease_payment_schedule.append({
                "date_to_invoice": rent_start_date,
                "lease_item": lease_item.lease_item,
                "lease_item_name": lease_item.lease_item,
                "rate": lease_item.amount,
                "qty": invoice_qty,
                "paid_by": lease_item.paid_by
            })

            rent_start_date = add_days(invoice_period_end, 1)

    lease_contract.set("lease_payment_schedule", lease_payment_schedule)
    lease_contract.save()

    frappe.msgprint("Completed making of invoice schedule.")

# def erase_lease_payment_schedule_on_delete(doc, method):
#     if method == "on_trash":
#         lease_contract = frappe.get_doc("Lease Contract", doc.parent)
#         lease_contract.set("lease_payment_schedule", [])
#         lease_contract.save()

# # Register the trigger function to the "Lease Item" doctype
# frappe.delete_doc("Lease Item", "on_trash", erase_lease_payment_schedule_on_delete)


# @frappe.whitelist()
# def make_lease_payment_schedule(leasedoc):
#     lease_contract = frappe.get_doc("Lease Contract", leasedoc)

#     frequency_factors = {
#         "Monthly": 1,
#         "Quarterly": 3,
#         "6 months": 6,
#         "Annually": 12
#     }

#     lease_contract.lease_payment_schedule = []

#     for lease_item in lease_contract.lease_item:
#         frequency_factor = frequency_factors.get(lease_item.frequency, 1)
#         invoice_qty = float(frequency_factor)

#         rent_start_date = lease_contract.rent_start_date
#         rent_end_date = lease_contract.rent_end_date

#         # while rent_end_date >= rent_start_date:
#         #     invoice_period_end = add_days(add_months(rent_start_date, frequency_factor), -1)
#         #     if invoice_period_end > rent_end_date:
#         #         invoice_qty = getDateMonthDiff(rent_start_date, rent_end_date, 1)
#         #     rent_start_date = add_days(invoice_period_end, 1)

#         lease_period_months = (rent_end_date.year - rent_start_date.year) * 12 + rent_end_date.month - rent_start_date.month + 1
#         num_invoices = lease_period_months // frequency_factor

#         invoice_dates = [rent_start_date + relativedelta(months=i * frequency_factor) for i in range(num_invoices)]
#         lease_items = [lease_item.lease_item] * num_invoices
#         lease_item_names = [lease_item.lease_item] * num_invoices
#         rates = [lease_item.amount] * num_invoices
#         qtys = [invoice_qty] * num_invoices
#         paid_bys = [lease_item.paid_by] * num_invoices

#         for invoice_date, lease_item, lease_item_name, rate, qty, paid_by in zip(invoice_dates, lease_items, lease_item_names, rates, qtys, paid_bys):
#             invoice = lease_contract.append('lease_payment_schedule', {})
#             invoice.date_to_invoice = invoice_date
#             invoice.lease_item = lease_item
#             invoice.lease_item_name = lease_item_name
#             invoice.rate = rate
#             invoice.qty = qty
#             invoice.paid_by = paid_by

#     lease_contract.save()
#     frappe.msgprint("Completed making of invoice schedule.")


# @frappe.whitelist()		
# def make_lease_payment_schedule(leasedoc):
#  	# frappe.msgprint("This is the parameter passed: " + str(leasedoc))

# 	lease_contract=frappe.get_doc("Lease Contract",str(leasedoc))

# 	# lease_items=lease_contract.lease_item

# 	lease_contract.set('lease_payment_schedule',[])

# 	item_payment_frequency={
# 		"Monthly":1.00,
# 		"Quarterly":3.00,
# 		"6 months":6.00,
# 		"Annually":12.00
# 		}
	
# 	for lease_item in lease_contract.lease_item:

# 		frequency_factor=item_payment_frequency.get(lease_item.frequency)
# 		invoice_qty = float(frequency_factor)


# 		if lease_item.frequency== "Monthly":
# 			rent_start_date=lease_contract.rent_start_date
# 			rent_end_date=lease_contract.rent_end_date
# 			# lease_period_months = (rent_end_date.year - rent_start_date.year) * 12 + rent_end_date.month - rent_start_date.month + 1

# 			while rent_end_date >= rent_start_date:
# 				invoice_period_end = add_days(add_months(rent_start_date, frequency_factor), -1)
# 				if invoice_period_end > rent_end_date:
# 					invoice_qty = getDateMonthDiff(rent_start_date, rent_end_date, 1)
# 				lease_payment_schedule = lease_contract.append('lease_payment_schedule', {})
# 				lease_payment_schedule.date_to_invoice = rent_start_date
# 				lease_payment_schedule.lease_item = lease_item.lease_item
# 				lease_payment_schedule.lease_item_name = lease_item.lease_item
# 				lease_payment_schedule.rate = lease_item.amount
# 				lease_payment_schedule.qty = invoice_qty
# 				lease_payment_schedule.paid_by = lease_item.paid_by
# 				rent_start_date = add_days(invoice_period_end, 1)


# 		elif lease_item.frequency == "Quarterly":
# 			rent_start_date=lease_contract.rent_start_date       	
# 			rent_end_date=lease_contract.rent_end_date
# 			lease_period_months = (rent_end_date.year - rent_start_date.year) * 12 + rent_end_date.month - rent_start_date.month + 1
# 			# num_invoices = lease_period_months // 3

# 			while rent_end_date >= rent_start_date:
# 				invoice_period_end = add_days(add_months(rent_start_date, frequency_factor), -1)
# 				if invoice_period_end > rent_end_date:
# 					invoice_qty = getDateMonthDiff(rent_start_date, rent_end_date, 1)
# 				lease_payment_schedule = lease_contract.append('lease_payment_schedule', {})
# 				lease_payment_schedule.date_to_invoice = rent_start_date
# 				lease_payment_schedule.lease_item = lease_item.lease_item
# 				lease_payment_schedule.lease_item_name = lease_item.lease_item
# 				lease_payment_schedule.rate = lease_item.amount
# 				lease_payment_schedule.qty = invoice_qty
# 				lease_payment_schedule.paid_by = lease_item.paid_by
# 				rent_start_date = add_days(invoice_period_end, 1)



# 		elif lease_item.frequency == "6 months":
# 			rent_start_date=lease_contract.rent_start_date       	
# 			rent_end_date=lease_contract.rent_end_date
# 			lease_period_months = (rent_end_date.year - rent_start_date.year) * 12 + rent_end_date.month - rent_start_date.month + 1
# 			# six_invoices = lease_period_months // 6

# 			while rent_end_date >= rent_start_date:
# 				invoice_period_end = add_days(add_months(rent_start_date, frequency_factor), -1)
# 				if invoice_period_end > rent_end_date:
# 					invoice_qty = getDateMonthDiff(rent_start_date, rent_end_date, 1)
# 				lease_payment_schedule = lease_contract.append('lease_payment_schedule', {})
# 				lease_payment_schedule.date_to_invoice = rent_start_date
# 				lease_payment_schedule.lease_item = lease_item.lease_item
# 				lease_payment_schedule.lease_item_name = lease_item.lease_item
# 				lease_payment_schedule.rate = lease_item.amount
# 				lease_payment_schedule.qty = invoice_qty
# 				lease_payment_schedule.paid_by = lease_item.paid_by
# 				rent_start_date = add_days(invoice_period_end, 1)


# 		elif lease_item.frequency == "Annually":
# 			rent_start_date=lease_contract.rent_start_date       	
# 			rent_end_date=lease_contract.rent_end_date
# 			lease_period_months = (rent_end_date.year - rent_start_date.year) * 12 + rent_end_date.month - rent_start_date.month + 1
# 			# six_invoices = lease_period_months // 12

# 			while rent_end_date >= rent_start_date:
# 				invoice_period_end = add_days(add_months(rent_start_date, frequency_factor), -1)
# 				if invoice_period_end > rent_end_date:
# 					invoice_qty = getDateMonthDiff(rent_start_date, rent_end_date, 1)
# 				lease_payment_schedule = lease_contract.append('lease_payment_schedule', {})
# 				lease_payment_schedule.date_to_invoice = rent_start_date
# 				lease_payment_schedule.lease_item = lease_item.lease_item
# 				lease_payment_schedule.lease_item_name = lease_item.lease_item
# 				lease_payment_schedule.rate = lease_item.amount
# 				lease_payment_schedule.qty = invoice_qty
# 				lease_payment_schedule.paid_by = lease_item.paid_by
# 				rent_start_date = add_days(invoice_period_end, 1)

# 	lease_contract.save()
# 	frappe.msgprint("Completed making of invoice schedule.")



