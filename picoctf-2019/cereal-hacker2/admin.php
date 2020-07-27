<?php

require_once('cookie.php');

if(isset($perm) && $perm->is_admin()){
?>
	
	<body>
		<div class="container">
			<div class="row">
				<div class="col-sm-9 col-md-7 col-lg-5 mx-auto">
					<div class="card card-signin my-5">
						<div class="card-body">
							<h5 class="card-title text-center">Welcome to the admin page!</h5>
							<h5 style="color:blue" class="text-center">Flag: Find the admin's password!</h5>
						</div>
					</div>
				</div>
			</div>
		</div>

	</body>

<?php
}
else{
?>
	
	<body>
		<div class="container">
			<div class="row">
				<div class="col-sm-9 col-md-7 col-lg-5 mx-auto">
					<div class="card card-signin my-5">
						<div class="card-body">
							<h5 class="card-title text-center">You are not admin!</h5>
							<form action="index.php" method="get">
								<button class="btn btn-lg btn-primary btn-block text-uppercase" name="file" value="login" type="submit" onclick="document.cookie='user_info=; expires=Thu, 01 Jan 1970 00:00:18 GMT; domain=; path=/;'">Go back to login</button>
							</form>
						</div>
					</div>
				</div>
			</div>
		</div>

	</body>

<?php
}
?>
