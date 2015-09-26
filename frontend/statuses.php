<?php
/**
 * Copyright 2011 Facebook, Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may
 * not use this file except in compliance with the License. You may obtain
 * a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 * License for the specific language governing permissions and limitations
 * under the License.
 */

require 'fb-library/src/facebook.php';

// Create our Application instance (replace this with your appId and secret).
$facebook = new Facebook(array(
	'appId'  => '502243603166501',
	'secret' => '75067b7bbc77c8f02dd90a5741933f82',
));

// Get User ID
$user = $facebook->getUser();
// We may or may not have this data based on whether the user is logged in.
//
// If we have a $user id here, it means we know the user is logged into
// Facebook, but we don't know if the access token is valid. An access
// token is invalid if the user logged out of Facebook.

if ($user) {
	try {
    // Proceed knowing you have a logged in user who's authenticated.
		$user_profile = $facebook->api('/me');
		$statuses = $facebook->api('/me/statuses');
		$checkins = $facebook->api('/me/checkins');
	} catch (FacebookApiException $e) {
		error_log($e);
		$user = null;
	}
}

// Login or logout url will be needed depending on current user state.
if ($user) {
	$logoutUrl = $facebook->getLogoutUrl();
}else {
	$loginUrl = $facebook->getLoginUrl();
}

// This call will always work since we are fetching public data.
$naitik = $facebook->api('/naitik');

?>
<?php 
	$dns ='mysql:host=localhost;dbname=thecity4_leon_test';
	$username ='thecity4';
	$password ='Admin@12';
	$con = mysql_connect("localhost","thecity4","Admin@12");
	mysql_query("SET NAMES 'utf8'");
	if (!$con)
	{
		die('Could not connect: ' . mysql_error());
	}
	mysql_select_db("thecity4_leon_test", $con);
?>
<?php
	/*$name =$user_profile['name'];
	$username =$user_profile['username'];
	$gender =$user_profile['gender'];
	$email =$user_profile['email'];
	$time=date("Y-m-d H:i:s");
	if($username==''){
		$username =mktime(0, 0, 0, date('m'), date('d'), date('Y')).'unknow_user';
		$name =mktime(0, 0, 0, date('m'), date('d'), date('Y')).'unknow_user';
	}*/
?>
<?php /*
	$sql_check ="SELECT `id` FROM `users` WHERE `username`='$username'";
	$check_id_query =mysql_query($sql_check,$con);
	while($row = mysql_fetch_array($check_id_query)){
		$check_id=$row['id'];
	}*/
		?>
<!doctype html>
<html xmlns:fb="http://www.facebook.com/2008/fbml">
  <head>
    <title>php-sdk</title>
    <style>
      body {
        font-family: 'Lucida Grande', Verdana, Arial, sans-serif;
      }
      h1 a {
        text-decoration: none;
        color: #3b5998;
      }
      h1 a:hover {
        text-decoration: underline;
      }
    </style>
  </head>
  <body>
    <h1>php-sdk</h1>

	<?php if ($user): ?>
	<a href="<?php echo $logoutUrl; ?>">Logout</a>
	<?php else: ?>
	<div>
		Login using OAuth 2.0 handled by the PHP SDK:
		<a href="<?php echo $loginUrl; ?>">Login with Facebook</a>
	</div>
	<?php endif ?>
	
	<?php if ($user )://&& !$check_id): ?>
	<h3>You</h3>
	<img src="https://graph.facebook.com/<?php echo $user; ?>/picture">

	<h3>Your User Object (/me)</h3>
	<pre><?php print_r($checkins);?></pre>
	<?php /*foreach ($statuses['data'] as $statuses)://for statuses?>
	
	<pre><?php echo ($statuses['message'])?></pre>
	<br>
	<pre><?php echo  '    '.$statuses['updated_time'];?></pre>

	<?  endforeach;*/?>
	
	<?php /*
		$sql_user ="INSERT INTO `users` (`name`,`username`,`gender`,`email`,`created`)VALUES('$name','$username','$gender','$email','$time')";
		$insert_user =mysql_query($sql_user,$con);*/
	?>
	<?php/* foreach($likes['data'] as $likes):*/?>
	<?php
		/*$likes_category =$likes['category'];
		$likes_name =$likes['name'];
		$likes_id =$likes['id'];
		$sql_likes ="INSERT INTO `likes` (`username`,`category`,`likes_name`,`likes_id`)VALUES('$username','$likes_category','$likes_name','$likes_id')";
		mysql_query($sql_likes,$con);*/
		?>
	<?php /*endforeach*/;?>
    <?php else: ?>
      <strong><em>You are not Connected.or did it</em></strong>
    <?php endif ?>
  </body>
</html>
