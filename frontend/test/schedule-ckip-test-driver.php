
<?php
/**
 * schedule-ckip-test-driver.php
 *
 * PHP version 5
 *
 * @category PHP
 * @package  /
 * @author   Fukuball Lin <fukuball@gmail.com>
 * @license  No Licence
 * @version  Release: <1.0>
 * @link     http://fukuball@github.com
 */

define('CKIP_SERVER','140.109.19.104');
define('CKIP_PORT','1501');
define('CKIP_USERNAME','leonyang0124');
define('CKIP_PASSWORD','Admin@12');

require_once "CKIPClient.php";

$ckip_client_obj = new CKIPClient(
   CKIP_SERVER,
   CKIP_PORT,
   CKIP_USERNAME,
   CKIP_PASSWORD
);

$raw_text = "獨立音樂需要大家一起來推廣，歡迎加入我們的行列。";

$raw_text = str_replace("，", "\n", $raw_text);
$raw_text = str_replace("。", "\n", $raw_text);
$raw_text = str_replace(",", "\n", $raw_text);
$raw_text = str_replace(".", "\n", $raw_text);

$raw_text_array = explode("\n", $raw_text);
$raw_text_array = array_filter($raw_text_array);

foreach ($raw_text_array as $raw_sentence) {

   $return_text = $ckip_client_obj->send($raw_sentence);
   echo $return_text;

   $return_term = $ckip_client_obj->getTerm();
   print_r($return_term);

   sleep(5);

}


?>