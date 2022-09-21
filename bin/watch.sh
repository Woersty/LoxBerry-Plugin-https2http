#!/bin/bash

. $LBHOMEDIR/libs/bashlib/loxberry_log.sh
PACKAGE=kidlox
NAME=daemon
FILENAME=${LBPLOG}/${PACKAGE}/daemon.log
APPEND=1
 
LOGSTART "kidlox daemon started."
#LOGDEB "This is a DEBUG message (severity 7)"
#LOGINF "This is an INFO message (severity 6)"
#LOGOK "This is an OK message (severity 5)"
#LOGWARN "This is a WARNING message (severity 4)"
#LOGERR "This is an ERROR message (severity 3)"
#LOGCRIT "This is a CRITICAL message (severity 2)"
#LOGALERT "This is a ALERT message (severity 1)"
#LOGEMERGE "This is a EMERGENCY message (severity 0)"

monitoring_start_day=0       
monitoring_end_day=7         
monitoring_start_time=0      
monitoring_end_time=23       

if  [ "`date +%w`" -ne "5" ] && [ "`date +%w`" -ge "$monitoring_start_day" ] && [ "`date +%w`" -le "$monitoring_end_day" ] ; then

LOGOK "Nicht die Freitagsregel"
if [ `date +%H` -ge $monitoring_start_time ] && [ `date +%H` -le $monitoring_end_time ]; then
  if [ `date +%H` -ge 8 ] && [ `date +%H` -le 9 ]; then
	# Um 9:xx und 10:xx ok
	LOGOK "Spielzeit 8xx-9xx"
   elif [ `date +%H` -ge 11 ] && [ `date +%H` -le 12 ]; then
        # Um 13:xx und 14:xx ok
        LOGOK "Spielzeit 11xx-12xx"
   elif [ `date +%H` -ge 15 ] && [ `date +%H` -le 16 ]; then
	# Um 13:xx und 14:xx ok
	LOGOK "Spielzeit 15xx-16xx"
  elif [ `date +%H` -ge 19 ] && [ `date +%H` -le 20 ]; then
	# Um 17:xx und 18:xx ok
	LOGOK "Spielzeit 19xx-20xx"
  else
	LOGOK  "keine Spielzeit"
        wget -qO- "http://GamingLaptop-Moritz.fritz.box:8009/warn" > /dev/null &
	 wget -qO- "http://GamingLaptop-Oskar.fritz.box:8009/warn" > /dev/null &
        sleep 60
        wget -qO- "http://GamingLaptop-Moritz.fritz.box:8009/sleep" > /dev/null &
	 wget -qO- "http://GamingLaptop-Oskar.fritz.box:8009/sleep" > /dev/null &

  fi;
 fi;
fi;
if [ `date +%w` -eq 5 ]; then
LOGOK "Freitagsregel"
if [ `date +%H` -ge $monitoring_start_time ] && [ `date +%H` -le $monitoring_end_time ]; then
  if [ `date +%H` -ge 9 ] && [ `date +%H` -le 10 ]; then
        # Um 9:xx und 10:xx ok
       LOGOK  "Freitag Spielzeit 9xx-10xx"
  elif [ `date +%H` -ge 13 ] && [ `date +%H` -le 14 ]; then
        # Um 13:xx und 14:xx ok
       LOGOK "Freitag Spielzeit 13xx-14xx"
  elif [ `date +%H` -ge 16 ] && [ `date +%H` -le 17 ]; then
        # Um 16:xx und 17:xx ok
        LOGOK "Freitag Spielzeit 16xx-17xx"
  elif [ `date +%H` -eq 20 ] && [ `date +%H` -le 21 ] ; then
        # Um 20:xx und 21:xx ok
        LOGOK "Freitag Spielzeit 20xx-21xx"
  else
        LOGOK "Freitag - keine Spielzeit"
        wget -qO- "http://GamingLaptop-Moritz.fritz.box:8009/warn" > /dev/null &
         wget -qO- "http://GamingLaptop-Oskar.fritz.box:8009/warn" > /dev/null &
        sleep 60
        wget -qO- "http://GamingLaptop-Moritz.fritz.box:8009/sleep" > /dev/null &
         wget -qO- "http://GamingLaptop-Oskar.fritz.box:8009/sleep" > /dev/null &

  fi;
 fi;
fi;

LOGEND "Processing successfully finished"