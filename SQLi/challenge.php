<?php
include "./config.php";
$db = dbconnect();
if (isset($_GET['id'])) {
    $id = $_GET['id'];
} else {
    $id = ''; 
}
if (isset($_GET['pw'])) {
    $pw = $_GET['pw'];
} else {
    $pw = ''; 
}
if (preg_match('/\b(select|union|insert|update|delete|drop|;|--|\/\*|\*\/|\\\\|\'|")\b/i', $pw)) exit("HeHe");
if(preg_match('/prob|_|\.\|\(\)/i', $pw)) exit("No Hack ~_~");
if(preg_match('/sleep|benchmark/i',$pw))exit("HeHe");
$query = "select id from users where id='guest' and pw='{$pw}' ";
echo "<hr>query: <strong>{$query}</strong><hr><br>";
$result = @mysqli_fetch_array(@mysqli_query($db,$query));

if(isset($result['id']) && $result['id'] != ''){
    echo "<h2>Hello {$result['id']}</h2>";
}


$pw = addslashes($pw);
$query = "select pw from users where id='admin' and pw='{$pw}' ";
$result = @mysqli_fetch_array(@mysqli_query($db,$query));
if (isset($result['pw']) && $result['pw']) {
    solve("Challenge");
}
highlight_file(__FILE__);
?>
