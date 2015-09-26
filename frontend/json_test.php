<?php
    
    include('httpful.phar');
    
    // And you're ready to go!
    $response = \Httpful\Request::get('http://173.254.41.118:8080/mycorpus/chinesesegs/c18')->send();
    
    $test=($response->body->POST->p1);
    
    print_r($test);

    
    ?>

<?php

//include("httpful.phar");


/*
$url = "http://search.twitter.com/search.json?q=" . urlencode('#PHP');
$response = Request::get($url)
    ->withXTrivialHeader('Just as a demo')
    ->send();
 
foreach ($response->body->results as $tweet) {
    echo "@{$tweet->from_user} tweets \"{$tweet->text}\"\n";
}
*/
// And you're ready to go!
//$response = \Httpful\Request::get('http://example.com')->send();

//$uri= "http://173.254.41.118:8080/mycorpus/chinesesegs/c18";
//$uri = "https://www.googleapis.com/freebase/v1/mqlread?query=%7B%22type%22:%22/music/artist%22%2C%22name%22:%22The%20Dead%20Weather%22%2C%22album%22:%5B%5D%7D";
//$response = Request::get($uri)->send();
 
//$test= ($response->body);
//gettype($test);
//print_r($test);
/*
include_once('HttpClient.php');
 
$Client = new HttpClient();
$url = "http://173.254.41.118:8080/mycorpus/chinesesegs/c18";
$method = "GET";
$data= array();
/*$data = array('id'     => 'c100',
                 	'POST' => array(
			    'p1'=>array(
				"密胸發動機","全球快訊"
				
			    ),
			    'p2'=>array(
				"深夜食堂／吉林路尾麵攤 傍晚家鄉味"," 美食-欣傳媒-最好吃" 
				
			    ),
			    'p3'=>array(
				"可以食堂說吃一個蘋果!! @ 循環木~大明星 :: 隨意窩 Xuite日誌"
				
			    )
			    
			    
			)  
    );
 
//$data= json_encode($data);

$ret = $Client->HttpRequest($url,$method, $data);
 
//echo $ret['body'];

//$test_decode= json_decode($ret);


//echo gettype($ret);
//echo print_r($ret['body']).'<br>';
$TEST=$ret['body'];
echo '<pre>';
print_r($TEST);
echo '<pre>';
echo "<br>";
if($TEST['POST']){
    gettype($TEST['POST']);
    
};

//echo gettype($ret['body']['p1']);
//echo $TEST['POST'];

 * 
 */
?>