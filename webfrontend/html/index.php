<?php 
if (isset($_REQUEST['url']))
{
	$ctx = stream_context_create(array( 'http' => array( 'timeout' => 3 ) ) ); 
  $content = file_get_contents("https://".substr($_REQUEST['url'],8), 0, $ctx);
	if (isset($content) && strlen($content) > 1) 
	{
		echo $content;
		exit;
	}
}
echo "Error - URL correct?";
