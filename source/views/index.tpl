<!DOCTYPE html>
<html>
<head>
    <title>GNIB appointments</title>
    <link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/tachyons/4.6.2/tachyons.min.css">
</head>
<body>
<article class="athelas">
	<div class="vh-100 dt w-100 tc bg-dark-gray white cover">
		<div class="dtc v-mid">
			<header class="white-70">
      	<h2 class="f6 fw1 ttu tracked mb2 lh-title">last refreshed at {{ last_checked }}</h2>
      	<a class="link" href="https://burghquayregistrationoffice.inis.gov.ie/Website/AMSREG/AMSRegWeb.nsf/AppSelect?OpenForm">
      		<span class="light-yellow">go to booking site</span>
        </a>
  		</header>
  		<h1 class="f1 f-headline-l fw1 i white-60">GNIB Appointments</h1>
  		% if appointments is None:
  		<h3 class="f2 f-subheadline-l fw3 white-80">Sorry, no appointments are currently available</h3>
  		% else:
  		% for appointment in appointments:
  		<h5 class="f2 fw3 white">{{ appointment }}</h5>
  		% end
  		% end
      <footer class="white-30">
      <a class="link b f3 f2-ns dim white-40 lh-solid" href="https://github.com/coolharsh55/GNIBappointments">source code</a><br/>
      <a class="link b f5 f5-ns dim white-20" href="https://harshp.com/">made by harshvardhan pandit</a>
    </footer>
		</div>
	</div>

</article>
</body>
</html>