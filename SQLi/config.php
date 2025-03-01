<?php
function dbconnect() {
    $servername = "localhost";
    $username = "root";
    $password = "";
    $dbname = "my_challenge";

    $conn = new mysqli($servername, $username, $password, $dbname);
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }
    return $conn;
}

function solve($challenge) {
    echo "Congratulations! You solved the {$challenge}! The Flag is FLAG'{YOU_SKILLED_BLIND_SQLI}'";
}

ini_set('log_errors','1');
ini_set('error_log',"")
?>
