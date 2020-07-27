<?php

require_once('../sql_connect.php');

// I got tired of my php sessions expiring, so I just put all my useful information in a serialized cookie
class permissions
{
	public $username;
	public $password;
	
	function __construct($u, $p){
		$this->username = $u;
		$this->password = $p;
	}

	function is_admin(){
		global $sql_conn;
		if($sql_conn->connect_errno){
			die('Could not connect');
		}
		//$q = 'SELECT admin FROM pico_ch2.users WHERE username = \''.$this->username.'\' AND (password = \''.$this->password.'\');';
		
		if (!($prepared = $sql_conn->prepare("SELECT admin FROM pico_ch2.users WHERE username = ? AND password = ?;"))) {
		    die("SQL error");
		}

		$prepared->bind_param('ss', $this->username, $this->password);
	
		if (!$prepared->execute()) {
		    die("SQL error");
		}
		
		if (!($result = $prepared->get_result())) {
		    die("SQL error");
		}

		$r = $result->fetch_all();
		if($result->num_rows !== 1){
			$is_admin_val = 0;
		}
		else{
			$is_admin_val = (int)$r[0][0];
		}
		
		$sql_conn->close();
		return $is_admin_val;
	}
}

/* legacy login */
class siteuser
{
	public $username;
	public $password;
	
	function __construct($u, $p){
		$this->username = $u;
		$this->password = $p;
	}

	function is_admin(){
		global $sql_conn;
		if($sql_conn->connect_errno){
			die('Could not connect');
		}
		$q = 'SELECT admin FROM pico_ch2.users WHERE admin = 1 AND username = \''.$this->username.'\' AND (password = \''.$this->password.'\');';
		
		$result = $sql_conn->query($q);
		if($result->num_rows != 1){
			$is_user_val = 0;
		}
		else{
			$is_user_val = 1;
		}
		
		$sql_conn->close();
		return $is_user_val;
	}
}


if(isset($_COOKIE['user_info'])){
	try{
		$perm = unserialize(base64_decode(urldecode($_COOKIE['user_info'])));
	}
	catch(Exception $except){
		die('Deserialization error.');
	}
}

?>
