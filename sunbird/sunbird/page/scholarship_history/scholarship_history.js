frappe.pages['scholarship-history'].on_page_load = function(wrapper) {
    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'Scholarship History',
        single_column: true
    });

    page.set_title('Scholarship Details');
    page.set_title_sub('View all the details regarding scholarships');

    // Create filter containers
    const filterContainer = $('<div class="filters row"></div>').appendTo(page.main);
    $('<div class="col-md-4"><input type="text" id="student-id" class="form-control" placeholder="Student ID"></div>').appendTo(filterContainer);
    $('<div class="col-md-4"><input type="text" id="institute-id" class="form-control" placeholder="Institute ID"></div>').appendTo(filterContainer);
    $('<div class="col-md-4"><input type="number" id="year" class="form-control" placeholder="Year"></div>').appendTo(filterContainer);

    // Add a fetch button
    const fetchButton = $('<button class="btn btn-primary fetch-btn">Fetch Scholarships</button>').appendTo(page.main);

    // Create a table to display the data
    const tableContainer = $('<div class="table-responsive"></div>').appendTo(page.main);
    const table = $(`
        <table class="table table-bordered">
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Student Name</th>
                    <th>Institute ID</th>
                    <th>Student Type</th>
                    <th>Scholarship Amount</th>
                    <th>End Date</th>
                    <th>Year</th>
                </tr>
            </thead>
            <tbody></tbody>
        </table>
    `).appendTo(tableContainer);

    // Loading indicator
    const loadingIndicator = $('<div class="text-center my-3" style="display: none;">Loading...</div>').appendTo(page.main);

    // Function to fetch and display scholarship data
    function fetchScholarshipData() {
        // Show loading indicator
        loadingIndicator.show();
        fetchButton.prop("disabled", true);

        // Get filter values
        const studentId = $('#student-id').val();
        const instituteId = $('#institute-id').val();
        const year = $('#year').val();

        frappe.call({
            method: "sunbird.sunbird.page.scholarship_history.scholarship_history.get_scholarships",
            args: {
                student_id: studentId,
                institute_id: instituteId,
                year: year
            },
            callback: function(response) {
                const scholarships = response.message || [];

                // Clear existing table data
                table.find('tbody').empty();

                // Populate the table with scholarship records
                if (scholarships.length > 0) {
                    scholarships.forEach(scholarship => {
                        const row = $(`
                            <tr>
                                <td>${scholarship.name}</td>
                                <td>${scholarship.student_name}</td>
                                <td>${scholarship.institute_id}</td>
                                <td>${scholarship.type_of_student}</td>
                                <td>${scholarship.scholarship_amount}</td>
                                <td>${scholarship.scholarship_end_date}</td>
                                <td>${scholarship.current_scholarship_year}</td>
                            </tr>
                        `);
                        table.find('tbody').append(row);
                    });
                } else {
                    // Show a message if no records are found
                    table.find('tbody').append('<tr><td colspan="7" class="text-center">No scholarships found for the selected filters.</td></tr>');
                }
            },
            error: function() {
                frappe.msgprint(__('Failed to fetch scholarship data. Please try again.'));
            },
            always: function() {
                // Hide loading indicator and re-enable the fetch button
                loadingIndicator.hide();
                fetchButton.prop("disabled", false);
            }
        });
    }

    // Attach event to fetch button
    fetchButton.on('click', fetchScholarshipData);
};
