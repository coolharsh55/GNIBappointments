$(document).ready(function() {
	var div = $('<div id="interface-sticky-header">'
 	+	'<div id="interface-title">GNIB Extension</div>'
 	+	'<button id="interface-btn-check-appointments" class="interface-btn">Check Appointments</button>'
 	+	'<button id="interface-btn-load-data" class="interface-btn">Load Form</button>'
 	+	'<button id="interface-btn-save-data" class="interface-btn">Save Form</button>'
 	+	'<button id="interface-btn-ask-appointment" class="interface-btn">Ask for Appointment</button>'
	+'</div>').appendTo('body');

	// show all fields
	$('#dvSubCat').show();
	$('#SubCategory').html("");
	$('#dvDeclareCheck').show();
	$('#dvDeclareNew').hide();
	$('#dvDeclareRenew').show();
	$('#dvRenew').show();
	$('#dvPPNo').show();
	$('#dvPPRes').hide();	

	document.getElementById('interface-btn-check-appointments').addEventListener("click", function() {
	    check_appointments();
	}, false);

	document.getElementById('interface-btn-save-data').addEventListener("click", function() {
		console.log("category", $('#Category').val());
		console.log("subcategory", $('#SubCategory').val());
		console.log("gnib", $('#ConfirmGNIB').val());
		console.log("gnib_no", $('#GNIBNo').val());
		console.log("gnib_expiry", $('#GNIBExDT').val());
		console.log("user_declaration", $('#UsrDeclaration').val());
		console.log("given_name", $('#GivenName').val());
		console.log("surname", $('#SurName').val());
		console.log("dob", $('#DOB').val());
		console.log("nationality", $('#Nationality').val());
		console.log("email", $('#Email').val());
		console.log("email_confirm", $('#EmailConfirm').val());
		console.log("family_application", $('#FamAppYN').val());
		console.log("passport", $('#PPNoYN').val());
		console.log("passport_no", $('#PPNo').val());

		var category = $('#Category').val();
		var subcategory = $('#SubCategory').val();
		var gnib = $('#ConfirmGNIB').val();
		var gnib_no = $('#GNIBNo').val();
		var gnib_expiry = $('#GNIBExDT').val();
		var user_declaration = $('#UsrDeclaration').val();
		var given_name = $('#GivenName').val();
		var surname = $('#SurName').val();
		var dob = $('#DOB').val();
		var nationality = $('#Nationality').val();
		var email = $('#Email').val();
		var email_confirm = $('#EmailConfirm').val();
		var family_application = $('#FamAppYN').val();
		var passport = $('#PPNoYN').val();
		var passport_no = $('#PPNo').val();

		chrome.storage.sync.set({
			data: {
				"category": category,
				"subcategory": subcategory,
				"gnib": gnib,
				"gnib_no": gnib_no,
				"gnib_expiry": gnib_expiry,
				"user_declaration": user_declaration,
				"given_name": given_name,
				"surname": surname,
				"dob": dob,
				"nationality": nationality,
				"email": email,
				"email_confirm": email_confirm,
				"family_application": family_application,
				"passport": passport,
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
	    	$('#Category').val(data.category);
	    	$('#SubCategory')
		         .append($("<option></option>")
		         .attr("value",data.subcategory)
		         .text(data.subcategory));
			$('#SubCategory').val(data.subcategory);
			$('#ConfirmGNIB').val(data.gnib);
			$('#GNIBNo').val(data.gnib_no);
			$('#GNIBExDT').val(data.gnib_expiry);
			if (data.user_declaration == 'Y') {
				$('#UsrDeclaration').val('Y');
				$('#UsrDeclaration').prop('checked', true);
			} else {

			}
			$('#GivenName').val(data.given_name);
			$('#SurName').val(data.surname);
			$('#DOB').val(data.dob);
			$('#Nationality').val(data.nationality);
			$('#Email').val(data.email);
			$('#EmailConfirm').val(data.email_confirm);
			$('#FamAppYN').val(data.family_application);
			$('#PPNoYN').val(data.passport);
			$('#PPNo').val(data.passport_no);

	    });
	}, false);

	document.getElementById('interface-btn-ask-appointment').addEventListener("click", function() {
	    // allowLook4App();
	    $('#btEditDetails').show();
		$('#btLook4App').hide();
		$('#dvSelectChoice').show();
		$('#AppSelectChoice').val('S');
		$("#dvAppOptions").hide();
		$("#dvSubmitContent").hide();
		//var resetBut = '<button id="rpbtTop" type="button" class="btn btn-default btn-sm" onclick="resetAppSelect(true)"><span' 		
		//	+ ' class="glyphicon glyphicon-repeat"></span> Reset </button>'
			
		var sCat = "cat=" + $('#Category').val();
		var sSCat = "&sbcat=All" //+ $('#SubCategory').val();
		var sTyp = "&typ=" + $('#ConfirmGNIB').val();
		var dataThis = sCat + sSCat + sTyp
		$('#btSrch4Apps').prop('disabled', true);
		var stPath = "/Website/AMSREG/AMSRegWeb.nsf/(getAppsNear)?openpage";
		$.ajax({
	        datatype: "json",
	        cache: false,
	        type: "GET",
	        url: "https://burghquayregistrationoffice.inis.gov.ie/Website/AMSREG/AMSRegWeb.nsf/(getAppsNear)?openpage",
	        data: dataThis,
	        async: true,
	        success: function(data) {
	            $("#dvAppOptions").show();
				if (!(data.error === undefined || data.error === null)) {
					$("#dvAppOptions").html("<span class=\"appOpMsg\">" + data.error + "</span>");
					$('#btSrch4Apps').prop('disabled', false);
			
				} else if (!(data.empty === undefined || data.empty === null)) {
					$("#dvAppOptions")
					.html(
					"<table class=\"table\"><tr><td></td><td>No appointment(s) are currently available</td></tr></table>");
					$('#btSrch4Apps').prop('disabled', false);
					
				} else {
					var sTmp = '';
					//sTmp += '<div id="avSlotsTop" class="avSlotsRSDV">' + resetBut + '</div>'
					for (i = 0; i < data.slots.length; i++) {
						sTmp += '<div id="rw'
							+ data.slots[i].id
							+ '" class="appOption"><table class="table"><tr><td id="td'
							+ data.slots[i].id
							+ '"><button type="button" class="btn btn-success" onclick="bookit(\''
							+ data.slots[i].id
							+ '\')">Book This</button></td><td>'
							+ data.slots[i].time
							sTmp += '</td></tr></table></div>'
							$('#btSrch4Apps').prop('disabled', false);
					}

					$("#dvAppOptions").html(sTmp);
				}
	        }
	    });
	    $(window).scrollTop($('#dvSelectChoice').offset().top);
	});
});