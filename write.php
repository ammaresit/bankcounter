<?php
	
   $username = 'root';
   $password = '';
   $host = '127.0.0.1';
   $db_name = 'bankcounter';
   
   $id;
   $sira = '';
   $gise1 = '';
   $gise2 = '';

   if(isset($_GET['id'])){

   		$id = $_GET['id'];
        $sira = $_GET['sira'];
        $gise1 = $_GET['gise1'];
        $gise2 = $_GET['gise2'];

        $db = mysqli_connect(
          $host,
          $username,
          $password,
          $db_name);

        $result = mysqli_query($db, "SELECT * FROM bankcounter WHERE id='".$id."'");

        if($row = mysqli_fetch_assoc($result)){

        	$result = mysqli_query($db, "UPDATE bankcounter SET sira='".$sira."', gise1='".$gise1."', gise2='".$gise2."' 
	        	WHERE id='".$id."'");

	        mysqli_close($db);

	        print(json_encode(array(
	        	'success' => true,
	        	'found' => 'yes'
	        )));
        }else {

	        print(json_encode(array(
	        	'success' => true,
	        	'found' => 'no'
	        )));
	    }
    }
    else{
        print(json_encode(array(
            'success' => false
        )));
    }



?>