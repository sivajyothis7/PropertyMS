# Copyright (c) 2023, enfono and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import add_days, today, getdate, add_months, get_datetime, now

from pms.api import invoice_schedule

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
	# frappe.msgprint("This is the parameter passed: " + str(leasedoc))

	lease_contract=frappe.get_doc("Lease Contract",str(leasedoc))

	item_payment_frequency={
		"Monthly":1.00,
		"Quarterly":3.00,
		"6 months":6.00,
		"Annually":12.00
		}
	idx = 1
		

	# if len(lease_contract.lease_item) >= 1 and lease_contract.rent_end_date >= getdate(today()):

	# 	lease_payment_schedule_list = frappe.get_list(
    #             "Lease Payment Schedule",
    #             fields=["name", "parent", "invoice_number", "date_to_invoice"],
    #             filters={
    #                 "parent": lease_contract.name,
    #                 "date_to_invoice": ("<", lease_contract.rent_start_date),
    #             },
    #         )
		
	# 	for lease_payment_schedule in lease_payment_schedule_list:
	# 		frappe.delete_doc("Lease Payment Schedule",lease_payment_schedule.name)


	# 	lease_payment_schedule_list = frappe.get_list(
    #             "Lease Payment Schedule",
    #             fields=[
    #                 "name",
    #                 "parent",
    #                 "lease_item",
    #                 "invoice_number",
    #                 "date_to_invoice",
    #             ],
    #             filters={"parent": lease_contract.name},
    #         )
	# 	lease_items_list = frappe.get_list(
    #             "Lease Items",
    #             fields=["name", "parent", "lease_item"],
    #             filters={"parent": lease_contract.name},
    #         )
	# 	# frappe.msgprint(str(lease_items_list))
	# 	lease_item_name_list = [
    #             lease_item["lease_item"] for lease_item in lease_items_list
		
	# 	]
	# 	for lease_payment_schedule in lease_payment_schedule_list:
	# 			if lease_payment_schedule.lease_item not in lease_item_name_list:
	# 				frappe.delete_doc(
    #                     "Lease Payment Schedule", lease_payment_schedule.name
    #                 )

	for item in lease_contract.lease_item:
				# frappe.msgprint("Lease item being processed: " + str(item.lease_item))
				lease_payment_schedule_list= frappe.get_all(
						"Lease Payment Schedule",
						fields=[
							"name",
							"parent",
							"lease_item",
							"qty",
							"invoice_number",
							"date_to_invoice"
						],
						filters={"parent":lease_contract.name,"lease_item":item.lease_item},
						order_by="date_to_invoice",
					)	
				frappe.msgprint(str(lease_payment_schedule_list))

				frequency_factor=item_payment_frequency.get(item.frequency)
				invoice_qty= float(frequency_factor)
				end_date=lease_contract.rent_end_date
				invoice_date= lease_contract.rent_start_date

				if not lease_payment_schedule_list:
					while end_date>=invoice_date:
						invoice_period_end=add_days(
							add_months(invoice_date,frequency_factor),-1
						)

						invoice_schedule(
							invoice_date,
							item.lease_item,
							item.paid_by,
							item.lease_item,
							lease_contract.name,
							invoice_qty,
							item.amount,
							idx,
							item.document_type,
							
							
						)
						idx+=1
						invoice_date= add_days(invoice_period_end,1)


	
		
				
	# frappe.msgprint("Completed making of invoice schedule.")

				

		