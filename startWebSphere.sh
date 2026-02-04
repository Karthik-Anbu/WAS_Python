#!/bin/bash

###########################################################################################
#                                                                                         #
# Tool Name     : startWebSphere.sh.                                                      #
# Explanation   : CRSO WebSphere tool to start the JVMs and nodeagent in an environment.  #
#                                                                                         #
# Date          : 11/21/2012.                                                             #
# Version       : 2.0v                                                                    #
# Dependencies  : /opt/WebSphere/v85/wcc/bin/jvmrecycle/ck_WAS.list.                      #
#                                                                                         #
# Modifications : 03/26/2013 - Cleaned up the tool. Updated to version 2.0v.              #
# Notes         : This scritp does not manage the dmgr process.                           #
#                                                                                         #
# Contact       : CRSO WebSphere team.                                                    #
#                                                                                         #
#                                                                                         #
###########################################################################################

# Environment dependent variables. Make sure these are provided.
VERSION=v90
ENV=dev
PROFILE_NAME=node11

# Match the hostnumbers with the JVM numbers. Example {p1qwpws2[3]g} is JVMNUMBER_ON_THREE_HOST and has JVM names as {CoreGroupCoord[1]}.
# For above example: JVMNUMBER_ON_THREE_HOST=1
JVMNUMBER_ON_ONE_HOST=1
JVMNUMBER_ON_TWO_HOST=x
JVMNUMBER_ON_THREE_HOST=x
JVMNUMBER_ON_FOUR_HOST=x
JVMNUMBER_ON_FIVE_HOST=x
JVMNUMBER_ON_SIX_HOST=x
JVMNUMBER_ON_SEVEN_HOST=x
JVMNUMBER_ON_EIGHT_HOST=x
JVMNUMBER_ON_NINE_HOST=x
JVMNUMBER_ON_ZERO_HOST=x


#############################################################################################################################################################################################
#                                                                                                                                                                                           #
# ------------------------------------------------------------------ DO NOT MAKE ANY CHANGES AFTER THIS LINE. ----------------------------------------------------------------------------- #
#                                                                                                                                                                                           #
#############################################################################################################################################################################################

# Non-dependent variables.
batch=5
START_TIMEOUT=240
JAVASHAREDRESOURCES="/tmp/javasharedresources"
ret=0
JVMLISTFILE=/opt/WebSphere/v90/wcc/bin/jvmrecycle/ck_WAS.list
HOST=`hostname`
echo $HOST

# Checks
if [ ! -d /opt/WebSphere/$VERSION/AppServer/profiles/$PROFILE_NAME ]; then
   echo "[FATAL ERROR:] Check the environment variables inside the tool."
   exit 1
fi

if [ ! -s $JVMLISTFILE ]; then
   echo "The file $JVMLISTFILE is missing or empty."
   exit 1
fi

# Functions
function serverStarted
{
    VERSION=$1
    ENV=$2
    PROFILE_NAME=$3
    APPLICATION_SERVER=$4
    
    WAS_CMD="/opt/WebSphere/$VERSION/AppServer/profiles/$PROFILE_NAME/bin/serverStatus.sh $APPLICATION_SERVER"
    $WAS_CMD | grep "STARTED"
}

function startServer
{
    VERSION=$1
    ENV=$2
    PROFILE_NAME=$3
    APPLI_SERVER=$4

    ps -ef|grep $APPLI_SERVER |grep -v grep > /dev/null 2>&1
    if [[ $? -eq 0 ]]; then 
       echo "WARNING: PID associated with $APPLI_SERVER exists, Process may be *ALREADY* running ???"
    else
       if [[ $APPLI_SERVER = "nodeagent" ]]; then
          /opt/WebSphere/$VERSION/AppServer/profiles/$PROFILE_NAME/bin/startNode.sh | grep "open for e-business"
       else
          /opt/WebSphere/$VERSION/AppServer/profiles/$PROFILE_NAME/bin/startServer.sh $APPLI_SERVER -nowait -quiet
       fi
    fi
}

# Main
#Clean javasharedresources
if [[ -d $JAVASHAREDRESOURCES ]]
  then
    rm $JAVASHAREDRESOURCES/*semaphore* > /dev/null 2>&1
    rm $JAVASHAREDRESOURCES/*memory* > /dev/null 2>&1
fi

#Reinforce WAS file system permission
chmod -R g+w /opt/WebSphere/$VERSION/AppServer/profiles/$PROFILE_NAME

echo "INFO: Starting nodeagent..."
startServer $VERSION $ENV $PROFILE_NAME "nodeagent"
if [[ $? -ne 0 ]]; then
   echo "ERROR: nodeagent cannot be started."
   echo "INFO: Websphere start *FAILED*."
   exit 1
fi
BATCH_LIST=""
count=0

# Orginal WPO regex to grab last character from hostname and popluate HOSTNUMBER
#HOSTNUMBER=`echo $HOST|sed 's/^.........//;s/.$//'`
# CRSO's new method for grabing last character from hostname and populating HOSTNUMBER
HOSTNUMBER=`echo $HOST|cut -c -99|rev|cut -c 1`
if [[ $HOSTNUMBER -eq 1 ]]; then
       JVM_NUMBER=$JVMNUMBER_ON_ONE_HOST
elif [[ $HOSTNUMBER -eq 2 ]]; then
       JVM_NUMBER=$JVMNUMBER_ON_TWO_HOST
elif [[ $HOSTNUMBER -eq 3 ]]; then
       JVM_NUMBER=$JVMNUMBER_ON_THREE_HOST
elif [[ $HOSTNUMBER -eq 4 ]]; then
       JVM_NUMBER=$JVMNUMBER_ON_FOUR_HOST
elif [[ $HOSTNUMBER -eq 5 ]]; then
      JVM_NUMBER=$JVMNUMBER_ON_FIVE_HOST
elif [[ $HOSTNUMBER -eq 6 ]]; then
       JVM_NUMBER=$JVMNUMBER_ON_SIX_HOST
elif [[ $HOSTNUMBER -eq 7 ]]; then
       JVM_NUMBER=$JVMNUMBER_ON_SEVEN_HOST
elif [[ $HOSTNUMBER -eq 8 ]]; then
       JVM_NUMBER=$JVMNUMBER_ON_EIGHT_HOST
elif [[ $HOSTNUMBER -eq 9 ]]; then
       JVM_NUMBER=$JVMNUMBER_ON_NINE_HOST
elif [[ $HOSTNUMBER -eq 0 ]]; then
       JVM_NUMBER=$JVMNUMBER_ON_ZERO_HOST
fi
APP_SERVER_LIST=`cat $JVMLISTFILE |grep $JVM_NUMBER|egrep -v '(^[[:space:]]*#|^[[:space:]]*$)'`
if [[ $? -ne 0 ]]; then
   echo "ERROR: $JVMLISTFILE did not populated properly.INFO: Check the matching of hostnumber with JVMs-numbers."
   exit 1
fi

for APP_SERVER in $APP_SERVER_LIST
do
  if [[ $count -gt $batch ]]
    then
      for JVM in $BATCH_LIST
      do
        IS_STARTED="false"
        TIME_USED=0
        while [[ $IS_STARTED != "true" && $TIME_USED -lt $START_TIMEOUT ]]
        do
          serverStarted $VERSION $ENV $PROFILE_NAME $JVM
          if [[ $? -ne 0 ]]
            then
              sleep 10
              TIME_USED=$TIME_USED+10
          else
            IS_STARTED="true"
          fi
        done
        if [[ $IS_STARTED != "true" ]]
          then
            echo "ERROR: $JVM cannot be started timely. Please contact CRSO WAS support."
            ret=1
        fi
      done
      BATCH_LIST=""
      count=0
  fi
  echo "INFO: Starting $APP_SERVER..."
  BATCH_LIST=$BATCH_LIST" "$APP_SERVER
  count=$count+1
  startServer $VERSION $ENV $PROFILE_NAME $APP_SERVER
done

echo "INFO: Checking the status..."

for JVM in nodeagent $BATCH_LIST
do
  IS_STARTED="false"
  TIME_USED=0
  while [[ $IS_STARTED != "true" && $TIME_USED -lt $START_TIMEOUT ]]
  do
    serverStarted $VERSION $ENV $PROFILE_NAME $JVM
    if [[ $? -ne 0 ]]
      then
        sleep 10
        TIME_USED=$TIME_USED+10
    else
      IS_STARTED="true"
    fi
  done
  if [[ $IS_STARTED != "true" ]]
    then
      echo "ERROR: $JVM cannot be started timely. Please contact CRSO WAS support."
      ret=1
  fi
done

echo "INFO: startWebSphere.sh on node(`hostname`) is completed."
exit $ret

#Niam
