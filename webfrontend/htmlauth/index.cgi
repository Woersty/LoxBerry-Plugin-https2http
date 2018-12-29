#!/usr/bin/perl

# Copyright 2018 Wörsty (git@loxberry.woerstenfeld.de)
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

use LoxBerry::System;
use LoxBerry::Web;
use LoxBerry::Log;
use MIME::Base64;
use List::MoreUtils 'true','minmax';
use HTML::Entities;
use CGI::Carp qw(fatalsToBrowser);
use CGI qw/:standard/;
use Config::Simple '-strict';
use warnings;
use strict;
no  strict "refs"; 

# Variables
my $maintemplatefilename 		= "https2http.html";
my $errortemplatefilename 		= "error.html";
my $helptemplatefilename		= "help.html";
my $pluginconfigfile 			= "https2http.cfg";
my $languagefile 				= "language.ini";
my $logfilename 				= "https2http.log";
my $template_title;
my $no_error_template_message	= "<b>https2http:</b> The error template is not readable. We must abort here. Please try to reinstall the plugin.";
my $version 					= LoxBerry::System::pluginversion();
my $helpurl 					= "http://www.loxwiki.eu/display/LOXBERRY/https2http";
my $log 						= LoxBerry::Log->new ( name => 'https2http', filename => $lbplogdir ."/". $logfilename, append => 1 );
my $plugin_cfg 					= new Config::Simple($lbpconfigdir . "/" . $pluginconfigfile);
my %Config 						= $plugin_cfg->vars() if ( $plugin_cfg );
my $error_message				= "";
my @pluginconfig_strings        = ""; 

# Logging
my $plugin = LoxBerry::System::plugindata();

LOGSTART "New admin call."      if $plugin->{PLUGINDB_LOGLEVEL} eq 7;
$LoxBerry::System::DEBUG 	= 1 if $plugin->{PLUGINDB_LOGLEVEL} eq 7;
$LoxBerry::Web::DEBUG 		= 1 if $plugin->{PLUGINDB_LOGLEVEL} eq 7;
$log->loglevel($plugin->{PLUGINDB_LOGLEVEL});

LOGDEB "Init CGI and import names in namespace R::";
my $cgi 	= CGI->new;
$cgi->import_names('R');

if ( $R::delete_log )
{
	my $log = LoxBerry::Log->new ( name => 'https2http', filename => $lbplogdir ."/". $logfilename);
	LOGDEB "Oh, it's a log delete call. ".$R::delete_log;
	LOGWARN "Delete Logfile: ".$logfilename;
	LOGSTART "Logfile restarted.";
	print "Content-Type: text/plain\n\nOK";
	LOGEND;
	exit;
}
else 
{
	LOGDEB "No log delete call. Go ahead";
}

LOGDEB "Get language";
my $lang	= lblanguage();
LOGDEB "Resulting language is: " . $lang;

LOGDEB "Check, if filename for the errortemplate is readable";
stat($lbptemplatedir . "/" . $errortemplatefilename);
if ( !-r _ )
{
	LOGDEB "Filename for the errortemplate is not readable, that's bad";
	$error_message = $no_error_template_message;
	LoxBerry::Web::lbheader($template_title, $helpurl, $helptemplatefilename);
	print $error_message;
	LOGCRIT $error_message;
	LoxBerry::Web::lbfooter();
	LOGCRIT "Leaving http2https Plugin due to an unrecoverable error";
	LOGEND;
	exit;
}

LOGDEB "Filename for the errortemplate is ok, preparing template";
my $errortemplate = HTML::Template->new(
		filename => $lbptemplatedir . "/" . $errortemplatefilename,
		global_vars => 1,
		loop_context_vars => 1,
		die_on_bad_params=> 0,
		associate => $cgi,
		%htmltemplate_options,
		debug => 1,
		);
LOGDEB "Read error strings from " . $languagefile . " for language " . $lang;
my %ERR = LoxBerry::System::readlanguage($errortemplate, $languagefile);

LOGDEB "Check, if filename for the maintemplate is readable, if not raise an error";
$error_message = $ERR{'ERRORS.ERR_MAIN_TEMPLATE_NOT_READABLE'};
stat($lbptemplatedir . "/" . $maintemplatefilename);
&error if !-r _;
LOGDEB "Filename for the maintemplate is ok, preparing template";
my $maintemplate = HTML::Template->new(
		filename => $lbptemplatedir . "/" . $maintemplatefilename,
		global_vars => 1,
		loop_context_vars => 1,
		die_on_bad_params=> 0,
		%htmltemplate_options,
		debug => 1
		);
LOGDEB "Read main strings from " . $languagefile . " for language " . $lang;
my %L = LoxBerry::System::readlanguage($maintemplate, $languagefile);

LOGDEB "Check if plugin config file is readable";
if (!-r $lbpconfigdir . "/" . $pluginconfigfile) 
{
	LOGWARN "Plugin config file not readable.";
	LOGDEB "Check if config directory exists. If not, try to create it. In case of problems raise an error";
	$error_message = $ERR{'ERRORS.ERR_CREATE_CONFIG_DIRECTORY'};
	mkdir $lbpconfigdir unless -d $lbpconfigdir or &error; 
	LOGDEB "Try to create a default config";
	$error_message = $ERR{'ERRORS.ERR_CREATE_CONFIG_FILE'};
	open my $configfileHandle, ">", $lbpconfigdir . "/" . $pluginconfigfile or &error;
		print $configfileHandle "[https2http]\n";
	close $configfileHandle;
	LOGWARN "Default config created. Display error anyway to force a page reload";
	$error_message = $ERR{'ERRORS.ERR_NO_CONFIG_FILE'};
	&error; 
}

$maintemplate->param( "LBPPLUGINDIR" , $lbpplugindir);

LOGDEB "Call default page";
&defaultpage;

#####################################################
# Subs
#####################################################

sub defaultpage 
{
	LOGDEB "Sub defaultpage";
	LOGDEB "Set page title, load header, parse variables, set footer, end";
	$template_title = $L{'H2H.MY_NAME'};
	LoxBerry::Web::lbheader($template_title, $helpurl, $helptemplatefilename);
	$maintemplate->param( "LOGO_ICON"		, get_plugin_icon(64) );
	$maintemplate->param( "HTTP_HOST"		, $ENV{HTTP_HOST});
	$maintemplate->param( "HTTP_PATH"		, "/plugins/" . $lbpplugindir);
	$maintemplate->param( "VERSION"			, $version);
	$maintemplate->param( "LOGLEVEL" 		, $L{"H2H.LOGLEVEL".$plugin->{PLUGINDB_LOGLEVEL}});
	$lbplogdir =~ s/$lbhomedir\/log\///; # Workaround due to missing variable for Logview
	$maintemplate->param( "LOGFILE" , $lbplogdir . "/" . $logfilename );
	LOGDEB "Check for pending notifications for: " . $lbpplugindir . " " . $L{'H2H.MY_NAME'};
	my $notifications = LoxBerry::Log::get_notifications_html($lbpplugindir, $L{'H2H.MY_NAME'});
	LOGDEB "Notifications pending" if $notifications;
	LOGDEB "No notifications pending." if !$notifications;
    $maintemplate->param( "NOTIFICATIONS" , $notifications);
    
    our $https2http_url = "http://".$ENV{'HTTP_HOST'} . $ENV{'SCRIPT_NAME'}; 
		$https2http_url =~ s/admin\///ig;
		$https2http_url =~ s/index.cgi/?url=/ig;
    $maintemplate->param( "https2http_url" , $https2http_url);
	
    
    print $maintemplate->output();
	LoxBerry::Web::lbfooter();
	LOGDEB "Leaving https2http Plugin normally";
	LOGEND;
	exit;
}

sub error 
{
	LOGDEB "Sub error";
	LOGERR $error_message;
	LOGDEB "Set page title, load header, parse variables, set footer, end with error";
	$template_title = $ERR{'ERRORS.MY_NAME'} . " - " . $ERR{'ERRORS.ERR_TITLE'};
	LoxBerry::Web::lbheader($template_title, $helpurl, $helptemplatefilename);
	$errortemplate->param('ERR_MESSAGE'		, $error_message);
	$errortemplate->param('ERR_TITLE'		, $ERR{'ERRORS.ERR_TITLE'});
	$errortemplate->param('ERR_BUTTON_BACK' , $ERR{'ERRORS.ERR_BUTTON_BACK'});
	print $errortemplate->output();
	LoxBerry::Web::lbfooter();
	LOGDEB "Leaving https2http Plugin with an error";
	LOGEND;
	exit;
}

