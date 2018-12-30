<html>
<head>
</head>
<body>
<ul> 
<?php
$command = escapeshellcmd('sudo -u www-data python /var/www/takeAPicture.py');
$output = shell_exec($command);
//echo nl2br($output);
$fp = fopen('/var/www/images/currentImage/log.txt', 'w');
$now = date('l jS \of F Y h:i:s A');
fwrite($fp, $now);
fwrite($fp, $output);
fclose($fp);
header("Location: showCurrentImage.php");
die();
?>
/ul>
</body>
</html>