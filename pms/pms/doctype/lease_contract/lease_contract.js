// Copyright (c) 2023, enfono and contributors
// For license information, please see license.txt

frappe.ui.form.on('Lease Contract', {
    refresh: function(frm) {
        // frm.refresh_field('lease_payment_schedule')
        frm.add_custom_button(__('Make Invoice Schedule'), function(){
            frappe.call({
                method: "pms.pms.doctype.lease_contract.lease_contract.make_lease_payment_schedule",
                args:{
                    leasedoc:frm.doc.name
                },
                // freeze:true,
                // freeze_message:__('Calling frappe_call Method'),
                callback: function(response) {
                    // console.log(response.message);
                    // $.each(response.message,function(i,d){
                    // var new_row = frm.add_child("lease_payment_schedule");
                    // new_row.date_to_invoice = d.date_to_invoice;
					// new_row.lease_item=d.lease_item;
					// new_row.paid_by=d.paid_by;

                    // new_row.item_name = d.item_name;
                    // new_row.item_group = d.item_group;
                    // new_row.brand = d.brand;
                    // })
                    frm.reload_doc();
                    frm.refresh_field('lease_payment_schedule')

                    //}
            }
        });
        });
    }
});