// Copyright (c) 2024, T4GC and contributors
// For license information, please see license.txt

frappe.ui.form.on("Institute POC", {
	verify_email: function(frm) {
        if (!frm.email_verifed && frm.doc.email_id) {
            frm.set_df_property('verify_email', 'hidden', 1);
            console.log("email_verifed", frm.email_verifed)
            frappe.call({
                method: "sunbird.utils.email_verification",
                args: {
                    email: frm.doc.email_id
                },
                callback: function (r) {
                    console.log("r", r)
                    if (r.message) {
                        frappe.show_alert({
                            message: __(r.message.message),
                            indicator: r.indicator
                        }, 5);
                        if (r.message.email_verification_status) {
                            frm.set_value('email_verifed', 1);
                            
                        }
                        frm.set_df_property('verify_email', 'hidden', 0);
                    }
                }
            });
        }

	},
});
