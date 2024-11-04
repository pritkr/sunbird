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