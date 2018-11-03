<?php 
error_reporting(~E_ALL & ~E_STRICT);     // Keine Fehler reporten (auch nicht E_STRICT)
ini_set("display_errors", false);        // Fehler nicht direkt via PHP ausgeben
if (isset($_REQUEST['url']))
{
    $curl = curl_init() or die("cURL init error");
	curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
	curl_setopt($curl, CURLOPT_HTTPAUTH, constant(CURLAUTH_ANY));
	curl_setopt($curl, CURLOPT_CUSTOMREQUEST, "GET");
	curl_setopt($curl, CURLOPT_FOLLOWLOCATION, true);
	curl_setopt($curl, CURLOPT_USERAGENT,'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36');
	curl_setopt($curl, CURLOPT_URL, "https://".substr($_REQUEST['url'],8));
	$out = curl_exec($curl);
	curl_close($curl); 
	if ($out === false )
	{
		die("cURL read error");
	}	
	else
	{
		echo $out;
	}
	exit;
}
else
{
	echo "Error - URL correct?";
}
