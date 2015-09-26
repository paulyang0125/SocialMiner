<?
function find_user($_id){
	//echo " ".$_id." ";
	global $facebook;
	$user=$facebook->api('/'.$_id);
	$params['last']=get_now();
	$params['fb_uid']=$user['id'];
	$params['link']=$user['link'];
	$params['name']=$user['name'];
	$params['username']=$user['username'];
	$params['locale']=$user['locale'];
	$params['name']=$user['name'];
	$params['about']=$user['about'];
	$params['birthday']=date("Y-m-d",strtotime($user['birthday']));
	$params['gender']=$user['gender'];
	$params['location']=$user['location']['name'];
	$params['hometown']=$user['hometown']['name'];
	$params['education']=$user['education'][0]['school']['name'];
	$params['work']=$user['work'][0]['employer']['name'].'/'.$user['work'][0]['position']['name'];
	$params['relationship_status']=$user['relationship_status'];

	if($user['sports']){
               
		foreach($user['sports'] as $sp){
			$sport.=" ".$sp['name'];
         	}
		$params["sport"]=$sport;
	}
	if($user['favorite_athletes']){
		foreach($user['favorite_athletes'] as $fa){
			$favorite_athletes.=" ".$fa['name'];
		}

		$params["favorite_athletes"]=$favorite_athletes;
	}
	if($user['favorite_teams']){
		foreach($user['favorite_teams'] as $ft){
			$favorite_teams.=" ".$ft['name'];
		}
		$params["favorite_teams"]=$favorite_teams;
	}

	return $params;
}

