<?php
echo gettype($_POST) ; 
//$name = $_POST["name"];
//$email = $_POST["email"];
$file ='m.txt';
file_put_contents($file, print_r($_POST, true), FILE_APPEND);
// Success Message
?>
