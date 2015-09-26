<?php
include('util.php');
header("location:$loginUrl");

if ($user) {
    try {
    // Proceed knowing you have a logged in user who's authenticated.
		$user_profile = $facebook->api('/me');
		//$posts= $facebook->api($id."/statuses?access_token=read_stream&format=json&limit=1000&since=$time");
		$friends= $facebook->api('/me/friends');
		//$readStream = $facebook->api("/method/fql.query?query=SELECT+read_stream+FROM+permissions+WHERE+uid+=+me()");
	} catch (FacebookApiException $e) {
		error_log($e);
		$user = null;
	}
}

$friends= $friends['data'];
/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
?>

<html manifest="manifest.appcache">
    <head>
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
		<script src="http://code.jquery.com/jquery-1.10.1.min.js"></script><script src="http://code.jquery.com/jquery-1.10.1.min.js"></script>
		<script>
			$(document).ready(function(){
				
				$("body").click(function(){
					$( "#effect:visible" ).removeAttr( "style" ).fadeOut();
				});
				
				$(".scroll").click(function(){
					//alert();
					$(this).find(".content").animate({
						opacity: 1,
						top: '+=0',
						height: 'toggle'
					}, 500, function() {
    // Animation complete.
					});
				});			
			});
		</script>
 		<style>		
			body
			{
				font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
				font-size: 16px;
				margin: 0;
				padding: 0;
				background-color: #eaeaea;
				position: relative;
				word-wrap: break-word;
				-ms-text-size-adjust: none;
				overflow-y: scroll;
				
			}

			ul{
				list-style-type: none;
				padding: 0px;
				margin: 0px;	
			}
			.view
			{
				max-width: 800px;
				height: 650px;
				margin:10px auto;
				background: #fff;
				 
	  border: 5px solid #eaeaea;
	  /* support Safari, Chrome */
	-webkit-border-radius: 5px;
	/* support firefox */
	-moz-border-radius: 5px;
	border-radius: 5px;
			}
			.header{
				height:60px;width: auto;background: #fff;;
			}
			.header .previous{
				position: relative;
				top: -80px;
				padding: 15px;
				
			}
			
			.scroll {
				border: 1px solid #A4AEB3;
				
			}
			.scroll p{
				margin: 20px;
				
				
			}
			.scroll .content{
				
				 width: 750px;height:auto;background: #fff;border-right: 0px solid #EBEBE5;border-bottom: 1px solid #EBEBE5;
				
			}
			
button{
pointer-events: none;
min-width: 50px;
height: 30px;
line-height: 25px;
font-weight: bold;
font-size: 13px;
text-align: center;
color: #fff;
padding: 0 4px;
text-decoration: none;
border: 0;
background-color: rgba(0,0,0,.1);
cursor: pointer;
border-radius: 2px;
}
.main{
	margin: 47px;
	height: 540px;
	overflow: scroll;
	
}
.main li{
	float: left;
	
	
}
.friend{
	
	width: 110px;
	height: 140px;
	background: #fff;
	padding: 15px;
}
.friend p{
	text-align: center;
	margin: 5px;
	
	
	
}

div.container_tip{position:absolute;
top:200px;
left:10px;
font-size: 9pt;
display:block;
height:100px;
width:200px;
background-color:transparent;
*border:1px solid #666;
}
div.container_tip s{
position:absolute;
top:-20px;
*top:-22px;
left:160px;
display:block;
height:0;
width:0;
font-size: 0; 
line-height: 0;
border-color:transparent transparent #666 transparent;
border-style:dashed dashed solid dashed;
border-width:10px;
}
div.container_tip i{position:absolute;
top:-9px;
*top:-9px;
left:-10px;
display:block;
height:0;
width:0;
font-size: 0;
line-height: 0;
border-color:transparent transparent #fff transparent;
border-style:dashed dashed solid dashed;
border-width:10px;
}
.content_tip{
border:1px solid #666;
-moz-border-radius:3px;
-webkit-border-radius:3px;
position:absolute;
background-color:#fff;
width:100%;
height:100%;
padding:5px;
*top:-2px;
*border-top:1px solid #666;
*border-top:1px solid #666;
*border-left:none;
*border-right:none;
*height:102px;
box-shadow: 3px 3px 4px #999;
-moz-box-shadow: 3px 3px 4px #999;
-webkit-box-shadow: 3px 3px 4px #999;
/* For IE 5.5 - 7 */
filter: progid:DXImageTransform.Microsoft.Shadow(Strength=4, Direction=135, Color=#999999);
/* For IE 8 */
-ms-filter: "progid:DXImageTransform.Microsoft.Shadow(Strength=4, Direction=135, Color='#999999')"; }

		</style>					
    </head>
	<body>
		<div id="effect" class="container_tip">
			<div class="content_tip"><br />
				點選你要注意及關心的朋友
			</div>
			<s>
				<i></i>
			</s>
		</div>
        <div class="view">
			<div class="header" >
				<h1 style="text-align: center;">Social-network miner</h1>
				<a href="index.php" ><div class="previous"><button>Type list</button></div></a>
			</div>
			<div class="main">
				<ul>
					<?php foreach ($friends as $list) {?>
					<li>
						<a href="facebook_index.php?id=<?php echo $list['id'];?>">
							<div class="friend">
								<img style="width: 110px;box-shadow:0 0 10px #94A7A4;" src="https://graph.facebook.com/<?php echo $list['id']; ?>/picture">
								<p><?php echo $list['name'];?></p>
							</div>
						</a>
					</li>
					<?php }?>
				</ul>
				
			</div>	
			
				
		</div>
    </body>
</html>