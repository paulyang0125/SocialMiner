<?php
/**
 * ckip-test-driver.php
 *
 * PHP version 5
 *
 * @category PHP
 * @package  /
 * @author   Fukuball Lin <fukuball@gmail.com>
 * @license  No Licence
 * @version  Release: <1.0>
 * @link     http://fukuball@github.com
 

require_once "CKIPClient.php";

define(CKIP_SERVER,'140.109.19.104');
define(CKIP_PORT,'1501');
define(CKIP_USERNAME,'paulyang0125');
define(CKIP_PASSWORD,'Admin@12');

$ckip_client_obj = new CKIPClient(
   CKIP_SERVER,
   CKIP_PORT,
   CKIP_USERNAME,
   CKIP_PASSWORD
);

$raw_text = "獨立音樂需要大家一起來推廣，\n".
            "歡迎加入我們的行列！。\n";

$return_text = $ckip_client_obj->send($raw_text);
//echo $return_text;

$return_sentence = $ckip_client_obj->getSentence();
//print_r($return_sentence);

$return_term = $ckip_client_obj->getTerm();
//print_r($return_term);
echo '$return_term';*/



?>
<form action="http://173.254.41.118:8080/mycorpus/chinesesegs" type="post">
    <input type="hide" value="匿蹤戰機維基百科，自由的百科全書
隱形飛機真的不能被發現嗎？科技文明小蕃薯問號小博士
印度將斥資億美元向俄羅斯購買戰機新華軍事新華網
超過千架飛機在神祕內華達三角失蹤奥秘网
鬼祟似曾蔭權棄專車避示威七一遊行新聞頻道新浪網
新春京阪遊：飛行國泰航空台北大阪飛機餐免稅商品的美食樂園無名小站
曾空襲利比亞和伊拉克的隱形飛機參與應對朝鮮威脅奇摩新聞
府：馬主席搭座機國民黨付費國內政治中央社即時新聞
怕座機遭扣押阿總統租英包機國際焦點中央社即時新聞
有趣問題–隱形戰機
伊朗征服者隱形戰機英美質疑：假的！
秘密飛機棚場創業公司
博客來書籍館黑蝙蝠中隊飛機的秘密：飛機圖鑑繪本
探秘機長與空姐在飛機上的私密事新華時政新華網
飛機火車的生活世界留言板天空部落
桃園機場看飛機大園鄉私密看飛機景點旅行攝影生活隨意窩日誌
美國發射飛行器執行秘密試飛任務新華科技新華網
美軌道飛行器將再次發射執行秘密試飛任務軍事中國網權威防務資訊
源主子的世界沒有飛機的日子天空部落
探秘機長與空姐在飛機上的私密事組圖旅遊頻道光明網
美生物學家揭示鳥類飛行秘密︰胸肌是天然發動機（圖）倍可親全球快訊
糖果屋的秘密飛機的一天～科學小秘密無名小站">
    
    <input type="submit">
</form>