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
include('util.php');
$time= time();

if($_GET['overall']==1){
    $time= $time-518400;
}elseif($_GET['overall']==2){
    $time= $time-2505600;
}elseif ($_GET['overall']==3) {
    $time= $time-31622400;
}else{
    $time= $time-31622400;
}

//$post= $facebook->api("me/statuses?format=json&since=$time");
if ($user) {
    try {
    // Proceed knowing you have a logged in user who's authenticated.
		$user_profile = $facebook->api('/me');
		$posts= $facebook->api("100000162986283/statuses?access_token=read_stream&format=json&limit=1000&since=$time");
		
		//$readStream = $facebook->api("/method/fql.query?query=SELECT+read_stream+FROM+permissions+WHERE+uid+=+me()");
	} catch (FacebookApiException $e) {
		error_log($e);
		$user = null;
	}
}

?>



<!doctype html>
<html xmlns:fb="http://www.facebook.com/2008/fbml">
  <head>
    <title>php-sdk</title>
    <style>
      body {
	background: #D5D5D5;  
        font-family: 'Lucida Grande', Verdana, Arial, sans-serif;
	margin: 0px;
      }
      h1 a {
        text-decoration: none;
        color: #3b5998;
      }
      h1 a:hover {
        text-decoration: underline;
      }
      #header {
	  width: 100%;
	  height: 80px;
	  background: #0A9DC2;
	  border-bottom: 3px solid #A0D6DB;
	  position: relative;
	  margin-bottom: 30px;
      }
      #menu {
	  background: #5198D6;
	  width: 200px;
	  height: 400px;
	  border: 6px solid #AAD3F3;	  
      }
      
      #main {
	  height: 500px;
	  width: 900px;
	  position: relative;
	  left: 250px;
	  top: -420px;
	  background: white;
	  border:6px solid #72BFF2;
      }
    </style>
  </head>
  <body>
    <div id="header">
	
    </div>
    <div id="menu">
	<ul>
	    <li><a>funtion1</a></li>
	    <li><a>funtion2</a></li>
	    <li><a>funtion3</a></li>
	</ul>   
    </div>
    <div id="main">
	<pre><?php 
	    foreach ($posts["data"] as $value) {
		
		echo $value['message'].'<br>';
	    }
	
	?><pre>
    </div>
      
      
      <?php if ($user){ ?>
	<a href="<?php echo $logoutUrl; ?>">Logout</a>
      <?php }else{ ?>
	<div>
		Login using OAuth 2.0 handled by the PHP SDK:
		<a href="<?php echo $loginUrl; ?>">Login with Facebook</a>
	</div>
      <?php } ?>
      
   
  </body>
</html>
