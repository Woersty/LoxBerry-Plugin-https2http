<?php
#####################################################################################################
# Loxberry Plugin to change protocol from HTTPS to HTTP to be used in the Loxone http-input-Object.
# Version: 2023.08.10
#####################################################################################################

// Error Reporting off
error_reporting(~E_ALL & ~E_STRICT);     // Keine Fehler reporten (auch nicht E_STRICT)
ini_set("display_errors", false);        // Fehler nicht direkt via PHP ausgeben
require_once "loxberry_system.php";
require_once "loxberry_log.php";
$L = LBSystem::readlanguage("language.ini");
$plugindata = LBSystem::plugindata();
ini_set("log_errors", 1);
ini_set("error_log", $lbplogdir."/https2http.log");
touch($lbplogdir."/https2http.log");

$datetime    = new DateTime;
function debug($message = "", $loglevel = 7, $raw = 0)
{
	global $L,$plugindata;
	if ( $plugindata['PLUGINDB_LOGLEVEL'] >= intval($loglevel)  || $loglevel == 8 )
	{
		switch ($loglevel)
		{
		    case 0:
		        // OFF
		        break;
		    case 1:
		        error_log( strftime("%A") ." <ALERT> PHP: ".$message );
		        break;
		    case 2:
		        error_log( strftime("%A") ." <CRITICAL> PHP: ".$message );
		        break;
		    case 3:
		        error_log( strftime("%A") ." <ERROR> PHP: ".$message );
		        break;
		    case 4:
		        error_log( strftime("%A") ." <WARNING> PHP: ".$message );
		        break;
		    case 5:
		        error_log( strftime("%A") ." <OK> PHP: ".$message );
		        break;
		    case 6:
		        error_log( strftime("%A") ." <INFO> PHP: ".$message );
		        break;
		    case 7:
		    default:
		        error_log( strftime("%A") ." PHP: ".$message );
		        break;
		}
		if ( $loglevel < 4 ) 
		{
		  if ( isset($message) && $message != "" ) notify ( LBPPLUGINDIR, $L['H2H.MY_NAME'], $message);
		}
	}
	return;
}

debug($L["ERRORS.ERROR_ENTER_PLUGIN"]." ".$_SERVER['REMOTE_ADDR'],5);
debug("Check Logfile size: ".LBPLOGDIR."/https2http.log",7);
$logsize = filesize(LBPLOGDIR."/https2http.log");
if ( $logsize > 5242880 )
{
    debug($L["ERRORS.ERROR_LOGFILE_TOO_BIG"]." (".$logsize." Bytes)",4);
    debug("Set Logfile notification: ".LBPPLUGINDIR." ".$L['H2H.MY_NAME']." => ".$L['ERRORS.ERROR_LOGFILE_TOO_BIG'],7);
    notify ( LBPPLUGINDIR, $L['H2H.MY_NAME'], $L["ERRORS.ERROR_LOGFILE_TOO_BIG"]." (".$logsize." Bytes)");
	system("echo '' > ".LBPLOGDIR."/https2http.log");
}
else
{
	debug("Logfile size is ok: ".$logsize,7);
}

debug($L["LOG.URL_CALLED"]." ".$_SERVER['REQUEST_URI'],5);
if (isset($_REQUEST['url']))
{
	if (strtolower(substr($_SERVER['QUERY_STRING'],0,18)) != "url=https%3a%2f%2f") 
	{
		debug($L["ERRORS.URL_DOESNT_START_WITH_HTTPS"]." ".$_SERVER['REQUEST_URI'],3);
		die($L["ERRORS.URL_DOESNT_START_WITH_HTTPS"]);
	}
	else
	{
	    $curl = curl_init() or debug($L["ERRORS.CURL_INIT_FAILED"],2);
		curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
		curl_setopt($curl, CURLOPT_HTTPAUTH, constant(CURLAUTH_ANY));
		curl_setopt($curl, CURLOPT_CUSTOMREQUEST, "GET");
		curl_setopt($curl, CURLOPT_FOLLOWLOCATION, true);
		curl_setopt($curl, CURLOPT_USERAGENT,'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36');
		$position1 = strrpos($_REQUEST['url'], '@');
		if ( $position1 )
		{
			debug("@ found at position ".$position1,7);
			$part1 = substr($_REQUEST['url'],8,$position1-8);
			$position2 = strpos($part1, ':');
			$user = urlencode(substr($part1,0,$position2));
			$pass = urlencode(substr($part1,$position2 + 1));
			$part2 = substr($_REQUEST['url'],$position1 + 1);
			debug("Call URL with Digest authentication: 'https://".$part2."' with User '".$user."' and Pass '".$pass."'",7);
			curl_setopt($curl, CURLOPT_USERPWD, "$user:$pass");
			curl_setopt($curl, CURLOPT_HTTPAUTH, CURLAUTH_DIGEST);
			curl_setopt($curl, CURLOPT_URL, "https://".$part2);
		}
		else
		{
			curl_setopt($curl, CURLOPT_URL, "https://".substr($_REQUEST['url'],8));
			debug("Call URL without authentication: "."https://".substr($_REQUEST['url'],8),7);
		}
		
		curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);
		curl_setopt($curl, CURLOPT_SSL_VERIFYSTATUS, false);
		curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, false);
		curl_setopt($curl, CURLOPT_ENCODING, "");
		$out = curl_exec($curl);
		if ($out === false )
		{
			debug($L["ERRORS.CURL_CALL_FAILED"]." (".$_REQUEST['url'].") [".curl_error($curl)."]",3);
			echo $L["ERRORS.CURL_CALL_FAILED"]." (".$_REQUEST['url'].") [".curl_error($curl)."]";
		}	
		else
		{
			debug($L["LOG.CURL_CALL_OK"],5);
			debug("cURL Datas:<br>".highlight_string($out,true),7);
			echo $out;
		}
		curl_close($curl); 
	}
}
else
{
	debug($L["ERRORS.ERROR_NO_URL_PROVIDED"],3);
    echo $L["H2H.MY_NAME"] ." - ". $L["ERRORS.ERROR_NO_URL_PROVIDED"];
}
	debug($L["LOG.PLUGIN_END"]."\n",5);
