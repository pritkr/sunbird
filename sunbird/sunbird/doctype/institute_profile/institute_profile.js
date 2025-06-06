function validate_year(year, field_label) {
    //console.log("Utils loaded")
    let currentYear = new Date().getFullYear();

    if (!/^\d{4}$/.test(year)) {
        frappe.msgprint(__(field_label + ' must be a four-digit year.'));
        return false;
    } else if (year < 1800 || year > currentYear) {
        frappe.msgprint(__(field_label + ' should be between 1800 and ' + currentYear + '.'));
        return false;
    }
    return true;
}

frappe.ui.form.on('Institute Profile', {
    year_of_establishment: function (frm) {
        let year = frm.doc.year_of_establishment;
        if (year && !validate_year(year, 'Year of Establishment')) {
            frm.set_value('year_of_establishment', '');
        }
    },
    year_of_partnership_with_sunbird: function (frm) {
        let year_of_partnership = frm.doc.year_of_partnership_with_sunbird;
        let year_of_establishment = frm.doc.year_of_establishment;

        // Check if year_of_partnership is valid and not before year_of_establishment
        if (year_of_partnership) {
            // Validate the year first
            if (!validate_year(year_of_partnership, 'Year of Partnership with Sunbird')) {
                frm.set_value('year_of_partnership_with_sunbird', '');
            }
            // Now check if it is not before year_of_establishment
            else if (year_of_partnership < year_of_establishment) {
                frappe.msgprint(__('Year of Partnership should not be before Year of Establishment.'));
                frm.set_value('year_of_partnership_with_sunbird', ''); // Clear the field if validation fails
            }
        }
    },
    verify_email: function (frm) {
        if (!frm.email_verification_status && frm.doc.email_id) {
            // make the verify email read only
            frm.set_df_property('verify_email', 'hidden', 1);
            console.log("email_verification_status", frm.email_verification_status)
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
                            frm.set_value('email_verification_status', 1);
                        }
                    }
                    frm.set_df_property('verify_email', 'hidden', 0);
                }
            });
        }
    }

});
