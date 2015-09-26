<?php
/*
ini_set('display_errors',1);
ini_set('display_startup_errors',1);
error_reporting(-1);*/
header('Content-type: text/html; Charset= UTF-8');
include('util.php');
include("restclient.php");

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
$id=$_GET['id'];
if ($user) {
	try {
    // Proceed knowing you have a logged in user who's authenticated.
		$user_profile = $facebook->api('/me');
		$posts= $facebook->api($id."/statuses?access_token=read_stream&format=json&limit=1000&since=$time");
		$friends= $facebook->api('/me/friends');
		//$readStream = $facebook->api("/method/fql.query?query=SELECT+read_stream+FROM+permissions+WHERE+uid+=+me()");
	} catch (FacebookApiException $e) {
		error_log($e);
		$user = null;
	}
}
foreach ($posts["data"] as $key=>$value) {
	
	$message= $value['message'];
	$array['p'.$key]= array("'{$message}'");
	//$date['p'.$key]= $value['updated_time'];
	$text['p'.$key]= $value['message'];
}

//$friends['data'][0]['id'].'-'.$_GET['overall'];
$data = array('_id'=> "$id",
              'POST' => $array
);

$data =json_encode($data);
//$data= json_encode($data);
$url = "http://173.254.41.118:8080/mycorpus/chinesesegs";

$response = \Httpful\Request::post($url)->sendsJson()->body($data)->send();    // And you're ready to go!   
$code= $response->code;

if($code==200){
    $url = "http://173.254.41.118:8080/mycorpus/lsa";
    $lsa_post = array(  '_id'     => "$id",
		    '_dbid'=>"$id"
                  );
    $lsa_post= json_encode($lsa_post);
    $response = \Httpful\Request::post($url)->sendsJson()->body($lsa_post)->send();
    $code= $response->code;
	
    if($code==200){
		$url = "http://173.254.41.118:8080/mycorpus/chinesesegs/".$id;
		$response = \Httpful\Request::get($url)->send();
		$chinesesegs=($response->body->POST_sentiment);
		$code= $response->code;
		//echo $chinesesegs['p12']['0']; 
		
	
		if($code==200){
			//////	sentiment
			$url = "http://173.254.41.118:8080/mycorpus/sentiment";
			$response = \Httpful\Request::post($url)->sendsJson()->body($lsa_post)->send();    // And you're ready to go!   
			$code= $response->code;
			//http://173.254.41.118:8080/mycorpus /sentiment
			
			if($code==200){
				$url = "http://173.254.41.118:8080/mycorpus/sentiment/".$id;
				$response = \Httpful\Request::get($url)->send();
				$sentiment=($response->body->sentiment);
				$code= $response->code;
				//http://173.254.41.118:8080/mycorpus /sentiment/ + myPost["_id"]
				
				
				//print_r($sentiment);
				
				
				if($code==200){
					$url = "http://173.254.41.118:8080/mycorpus/lsa/".$id;
					$restclient = new RestClient(); 
					$result = $restclient->get($url);
					$lsa = json_decode($result->response,true);
					//print_r($lsa);
					
					$lsa_post= $lsa['post_assignments'];
					$lsa_topic= $lsa['topic_assignments'];
					//print_r($lsa_topic);
					
					foreach($lsa_topic['0'] as $value){
						$str= strlen($value);
						if($str>=4){
							$topic_01[]=$value;
						}
					}
					
					foreach($lsa_topic['1'] as $value){
						$str= strlen($value);
						if($str>=4){
							$topic_02[]=$value;
						}
					}
					
					foreach($lsa_topic['2'] as $value){
						$str= strlen($value);
						if($str>=4){
							$topic_03[]=$value;
						}
					}
					
					
					$lsa_topic_01= implode ("，",$topic_01);
					$lsa_topic_02= implode ("，",$topic_02);
					$lsa_topic_03= implode ("，",$topic_03);
					
					
				}
			}
		}
	}
}



$po= (array_merge_recursive((array)$lsa_post,(array)$sentiment));
//print_r(array_merge_recursive($po,$text));
$post= (array)(array_merge_recursive($po,$text));




$result= array(
	0=> array(
		'title'=> $lsa_topic_01
	),
	1=> array(
		'title'=> $lsa_topic_02
	),
	2=> array(
		'title'=> $lsa_topic_03
	),
	3=> array(
		'title'=> '無法辨識'
	)
);

foreach ($post as $key=> $post) {
	//echo ($post[]);
	//echo get_type($post[0]);
	if($post[0]=='0'){
		$result[0]['content']["$key"]=array(
			'text'=> $post[2],
			'sentiment'=> $post[1]	
		);
		
	}
	
	if($post[0]=='1'){
		$result[1]['content']["$key"]=array(
			'text'=> $post[2],
			'sentiment'=> $post[1]	
		);
	}
	if($post[0]=='2'){
		$result[2]['content']["$key"]=array(
			'text'=> $post[2],
			'sentiment'=> $post[1]	
		);	
	}
	if($post[0]=='NB'){
		$result[3]['content']["$key"]=array(
			'text'=> $post[2],
			'sentiment'=> $post[1]	
		);
	}
}

?>

<html manifest="manifest.appcache">
    <head>
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
		<script src="http://code.jquery.com/jquery-1.10.1.min.js"></script>
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
				height: auto;
				
				margin:10px auto;
				background: #fff;
			}
			.header{
				height:60px;width: auto;background: #fff;
			}
			
			.header .previous{
				position: relative;
				top: -80px;
				padding: 15px;
				
			}
			
			.scroll {
				border-bottom: 1px solid #A4AEB3;
				
			}
			.scroll p{
				margin: 20px;
				font-size:20px;
				font-weight:700;
				
				
			}
			.scroll .content{
				
				 width: 750px;height:auto;background: #fff;border-bottom: 1px solid #EBEBE5;
				
			}
			.scroll .content p{
				
				font-weight: 100;
				font-size: 14px;
				
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



div.container_tip{position:absolute;
top:160px;
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
				觀看依據主題分類的朋友動態及對方的心情指數
			</div>
			<s>
				<i></i>
			</s>
		</div>
        <div class="view">
			<div class="header" >
				<h1 style="padding:10px;text-align: center;">Social-network miner</h1>
				<a href="facebook_friends.php" ><div class="previous"><button>friends list</button></div></a>
			</div>
				<ul>
					<?php foreach ($result as $key=> $lsa) {?>
					<?php// $ignore_title=FALSE;?>
					<li>
						<div id="title" class="scroll">
							<p><?php echo $lsa['title']?></p>
							<div hidden class="content" >
								<ul style="margin-left:30px;">
									<?php foreach ($lsa['content'] as $key => $value) {?>
									<?php //if($ignore_title==FALSE){$ignore_title= true;continue;}?>
									<li style="border-bottom: 1px solid #EBEBE5;">
										<p><span><img height="60" src="image/emotoicon_<?php echo $value['sentiment']?>.png"></span><?php  echo $value['text']?></p>
										<!--<p><?php echo $value['sentiment']?></p>-->
									</li>
									<?php }?>
								</ul>
							</div>
						</div>
					</li>
					<?php }?>
				</ul>	
		</div>
    </body>
</html>