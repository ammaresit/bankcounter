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

        $db = mysqli_connect(
          $host,
          $username,
          $password,
          $db_name);

        $result = mysqli_query($db, "SELECT * FROM bankcounter WHERE id='".$id."'");

        if($row = mysqli_fetch_assoc($result)) {

  		    print(json_encode(array(
  		      	'success' => true,
  		       	'found' => 'yes',
  		       	'id' => $row['id'],
  	           	'sira' => $row["sira"],
  	           	'gise1' => $row["gise1"],
  	           	'gise2' => $row['gise2']
  	       	)));

  	    }else {

  	    	print(json_encode(array(
  		      	'success' => true,
  		       	'found' => 'no'
  	       	)));
  	    }

        mysqli_close($db);
    }
    else{
        print(json_encode(array(
            'success' => false
        )));
    }



?>
