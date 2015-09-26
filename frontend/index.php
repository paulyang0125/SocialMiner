<!doctype html>
<html xmlns:fb="http://www.facebook.com/2008/fbml">
  <head>
    <title>php-sdk</title>
    <style>
      body {
	background: #eaeaea;  
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
      #menu {
      	  margin: 100px auto;
	  width: 300px;
	  height: 400px;
	  background: white;
	  
	  
	  border: 5px solid #b7b7b7;
	  /* support Safari, Chrome */
	-webkit-border-radius: 5px;
	/* support firefox */
	-moz-border-radius: 5px;
	border-radius: 5px;
	
      }
      #menu #icon {
	  width: 300px;
	  height: 80px;
	  background: #C0778EE;
	  /*border: 5px solid #fff;*/
	  
	  
      }
       #menu #icon a:link img{
       		 filter: Alpha(Opacity=30);
       		opacity: .3;
       		-webkit-filter: grayscale(100%);
       }
       #menu #icon a:visited img{
       		 filter: Alpha(Opacity=30);
       		opacity: .3; 
       		-webkit-filter: grayscale(100%);
       }
       /*#menu #icon a:hover img{
       
	 filter: Alpha(Opacity=100);
       		opacity: 1; 
	
	 
      }*/
    </style>
  </head>
  <body>
    <div id="menu">
	<div id="icon"><a href="facebook_friends.php"><img  style="-webkit-filter: grayscale(0%);filter: Alpha(Opacity=100);opacity: 1;" src="image/fb-icon.png"></a></div>
	<div id="icon"><a href="#"><img src="image/twitter-icon.jpg"></a></div>
	<div id="icon"><a href="#"><img src="image/weibo-icon.png"></a></div>
	<div id="icon"><a href="#"><img src="image/plurk-icon.png"></a></div>
	<div id="icon"><a href="#"><img src="image/google-icon.png"></a></div>
    </div>
    
  </body>
</html>