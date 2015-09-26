<?
//存入時間 做格式化
function get_now(){
        $t=time();
        $t=date("Y-m-d H:i:s ",$t);
        return $t;
}

//取星座
function get_zodiac_sign($month, $day)
{
//檢查參數
if ($month < 1 || $month > 12 || $day < 1 || $day > 31)
return false;

$signs = array(
array( "20" => "水瓶座"),
array( "19" => "雙鱼座"),
array( "21" => "白羊座"),
array( "20" => "金牛座"),
array( "21" => "雙子座"),
array( "22" => "巨蟹座"),
array( "23" => "獅子座"),
array( "23" => "處女座"),
array( "23" => "天秤座"),
array( "24" => "天蠍座"),
array( "22" => "射手座"),
array( "22" => "摩羯座")
);
list($sign_start, $sign_name) = each($signs[(int)$month-1]);
if ($day < $sign_start)
list($sign_start, $sign_name) = each($signs[($month -2 < 0) ? $month = 11: $month -= 2]);
return $sign_name;

} // end of function. 
