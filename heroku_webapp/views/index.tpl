<!DOCTYPE html>
<html>
<head>
    <title>GNIB appointments</title>
    <link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/tachyons/4.6.2/tachyons.min.css">
</head>
<body>
<article class="athelas">
	<div class="vh-100 dt w-100 tc bg-dark-gray white cover">
		<div class="dtc pv3">
			<header class="white-70">
      	<h2 class="f4 fw1 mb2">last refreshed {{ last_checked }}mins ago</h2>
        <div class="light-yellow">
            <span>go to </span>
            <a class="link red" href="https://burghquayregistrationoffice.inis.gov.ie/Website/AMSREG/AMSRegWeb.nsf/AppSelect?OpenForm">GNIB</a> 
            <span>site | go to </span>
            <a class="link red" href="https://reentryvisa.inis.gov.ie/website/INISOA/IOA.nsf/AppointmentSelection?OpenForm">VISA</a> 
            <span>site</span><br/>
            <p>timings are not official and may not reflect actual appointments</p>
        </div>
  		</header>
  		<h1 class="f1 fw1 i gold">Appointments</h1>

        <div class="f2 f-subheadline fw2 yellow">GNIB</div>
  		% if gnib_appointments is None:
  		<p class="red f4">Sorry, no appointments are currently available</p>
  		% else:
  		% for appointment in gnib_appointments:
  		<p class="f4 fw3 light-blue"><a href="https://burghquayregistrationoffice.inis.gov.ie/Website/AMSREG/AMSRegWeb.nsf/AppSelect?OpenForm" class="link f4 fw3 light-blue">{{ appointment }}</a></p>
  		% end
  		% end
        
        <div class="f2 f-subheadline fw2 yellow">VISA</div>
  		% if visa_appointments is None:
  		<p class="red f4">Sorry, no appointments are currently available</p>
  		% else:
  		% for appointment in visa_appointments:
  		<p class="f4 fw3 light-blue"><a href="https://reentryvisa.inis.gov.ie/website/INISOA/IOA.nsf/AppointmentSelection?OpenForm" class="link f4 fw3 light-blue">{{ appointment }}</a></p>
  		% end
  		% end
      
      <footer class="white-30 pv3">
      <a class="link b f3 f2-ns dim white-60 lh-solid" href="https://harshp.com/dev/projects/gnib-appointments/">published blog posts</a><br/>
      <a class="link b f4 f2-ns dim white-40" href="https://github.com/coolharsh55/GNIBappointments">source code</a><br/>
      <a class="link b f5 f5-ns dim white-20" href="https://harshp.com/">made by harshvardhan pandit</a>
    </footer>
		</div>
	</div>

</article>
</body>
</html>
