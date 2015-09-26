<?php 
	$dns ='mysql:host=localhost;dbname=thecity4_leon_test';
	$username ='thecity4';
	$password ='Admin@12';
	$con = mysql_connect("localhost","thecity4","Admin@12");
	mysql_query("SET NAMES 'utf8'");
	if (!$con)
	{
		die('Could not connect: ' . mysql_error());
	}
	mysql_select_db("thecity4_leon_test", $con);
?>
<table>
	<thead>
		<tr>
			<td>name</td>
			<td>gender</td>
			<td>category</td>
			<td>count</td>
		</tr>
	</thead>
	<tbody>

<?
	$sql_list ="SELECT COUNT(  `likes`.`category` ) AS  `count` ,  `likes`.`category` ,  `likes`.`username` ,  `users`.`name` ,`users`.`gender`
				FROM  `likes` 
				INNER JOIN  `users` ON  `users`.`username` =  `likes`.`username` 
				GROUP BY  `username` ,  `category`";
	$list_query =mysql_query($sql_list,$con);
	while($row = mysql_fetch_array($list_query)){?>
		<?php $this_name=$row["name"];?>
		<?php if($this_name==$previous_name){$this_name='';$row["gender"]='';}?>
		<tr>
			<td><?php echo $this_name;?></td>
			<td><?php echo $row["gender"];?><td/>
			<td><?php echo $row["category"];?></td>
			<td><?php echo $row["count"];?></td>
		</tr>
		<?php $previous_name=$row["name"];?>
<?php	}?>
	</tbody>
</table>



