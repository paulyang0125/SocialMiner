<?php
require 'fb-library/src/facebook.php';
include('httpful.phar');
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
		$posts= $facebook->api('me/statuses?format=json&limit=1000');
		
		//$readStream = $facebook->api("/method/fql.query?query=SELECT+read_stream+FROM+permissions+WHERE+uid+=+me()");
	} catch (FacebookApiException $e) {
		error_log($e);
		$user = null;
	}
}
 $login_url_params = array(
      'scope' => 'publish_actions,read_stream,offline_access,manage_pages',
      'fbconnect' =>  1,
      'redirect_uri' => 'http://'.$_SERVER['HTTP_HOST'].$_SERVER['REQUEST_URI']
   );

// Login or logout url will be needed depending on current user state.
if ($user) {
	$logoutUrl = $facebook->getLogoutUrl();
}else {
	$loginUrl = $facebook->getLoginUrl($login_url_params);
}
/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
?>
