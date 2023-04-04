# Copyright (c) 2023, enfono and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class LeaseContract(Document):
	
	def validate(self):
		

		if self.agreement_status=="Signed agreement received":
			self.validate_agreement_received()
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


	def validate_agreement_received(self):

		unit=frappe.get_doc("Unit",self.unit_name)
		if unit.status=="Leased":
			frappe.throw("This Unit is Already Leased")


	def validate_agreement_cancelled(self):

		unit=frappe.get_doc("Unit",self.unit_name)
		if unit.status=="Available":
			frappe.throw("Unit Agreement cannot be cancelled without having proper leasing agreement ")
	

		

	