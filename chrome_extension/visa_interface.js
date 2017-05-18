$(document).ready(function() {

    check_appointments();

	var div = $('<div id="interface-sticky-header">'
 	+	'<div id="interface-title">Visa Appointments</div>'
 	+	'<button id="interface-btn-check-appointments" class="interface-btn">Check Appointments</button>'
 	+	'<button id="interface-btn-load-data" class="interface-btn">Load Form</button>'
 	+	'<button id="interface-btn-save-data" class="interface-btn">Save Form</button>'
	+'</div>').appendTo('body');

	document.getElementById('interface-btn-check-appointments').addEventListener("click", function() {
	    check_appointments();
	}, false);

	document.getElementById('interface-btn-save-data').addEventListener("click", function() {
		console.log("gnib_no", $('#GNIBNo').val());
		console.log("given_name", $('#GivenName').val());
		console.log("surname", $('#Surname').val());
		console.log("dob", $('#DOB').val());
		console.log("appointment_type", $('#AppointType').val());
		console.log("visa_type", $('#AppointType').val());
		console.log("num", $('#AppsNum').val());
		console.log("nationality", $('#Nationality').val());
		console.log("email", $('#Email').val());
		console.log("email_confirm", $('#EmailConfirm').val());
		console.log("passport_no", $('#PassportNo').val());


		var gnib_no = $('#GNIBNo').val();
		var given_name = $('#GivenName').val();
		var surname = $('#Surname').val();
		var dob = $('#DOB').val();
		var appointment_type = $('#AppointType').val();
		var visa_type = $('#AppointType').val();
		var num = $('#AppsNum').val();
		var nationality = $('#Nationality').val();
		var email = $('#Email').val();
		var email_confirm = $('#EmailConfirm').val();
		var passport_no = $('#PassportNo').val();

		chrome.storage.sync.set({
			data: {
				"gnib_no": gnib_no,
				"given_name": given_name,
				"surname": surname,
				"visa_type": visa_type,
				"num": num,
				"dob": dob,
				"appointment_type": appointment_type,
				"nationality": nationality,
				"email": email,
				"email_confirm": email_confirm,
				"passport_no": passport_no
			}
		}, function() {
			swal({
				title: "Form data saved",
				type: "success"
			});
		});
	}, false);

	document.getElementById('interface-btn-load-data').addEventListener("click", function() {
	    chrome.storage.sync.get("data", function(data) {
	    	console.log(data.data);
	    	data = data.data;
	    	if (data == undefined || data == null) {
	    		swal({
	    			title: "form data could not be found",
	    			type: "error"
	    		});
	    		return;
	    	}
            $('#VisaType')
                .append($('<option></option>')
                .attr("value", data.visa_type)
                .text(data.visa_type));
			$('#GNIBNo').val(data.gnib_no);
			$('#GivenName').val(data.given_name);
			$('#Surname').val(data.surname);
			$('#DOB').val(data.dob);
			$('#Nationality').val(data.nationality);
			$('#Email').val(data.email);
			$('#EmailConfirm').val(data.email_confirm);
			$('#PassportNo').val(data.passport_no);
			$('#AppsNum').val(data.num);
			$('#AppointType').val(data.appointment_type);
			$('#VisaType').val(data.visa_type);

	    });
	}, false);

});
