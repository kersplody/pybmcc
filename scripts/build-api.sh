#!/bin/zsh

SWAGGER_FILES=(\
"Camera/AudioControl" \
"common/MediaControl" \
"common/TimelineControl" \
"Camera/ColorCorrectionControl" \
"common/TransportControl" \
"common/EventControl" \
"Camera/PresetControl" \
"Camera/VideoControl" \
"Camera/LensControl" \
"common/SystemControl" \
)

ASYNC_FILES=(\
"asyncAPI/Notification"\
)

DEPS=(\
  "sed" \
  "awk" \
  "swagger-codegen" \
  "curl" \
)

USAGE="USAGE: ./build-api.sh CAMERA_HOSTNAME_OR_IP OUTPUT_DIR"

swagger_codegen () {
  url="http://${1}/control/swagger/${2}/${3}.yaml"
  echo "SWAGGER: Generating ${3} from ${url}..."

  echo "{\"packageName\": \"$3\",\"projectName\": \"$3\"}" > /tmp/swc.json

  swagger-codegen generate -l python -i ${url} -o /tmp/${3} -c /tmp/swc.json
  mv /tmp/${3}/${3} ${4}

  rm /tmp/swc.json
}

async_codegen () {
  #no implemented
}

if [ "$#" -eq 0 ]
then
  echo $USAGE
  exit 1
fi

if [ -z "$2" ]
then
  echo "ERROR: No output path supplied"
  echo $USAGE
  exit 1
fi

outpath=${2}
host=${1}

for dep in "${DEPS[@]}"
do
  if (( ! $+commands[${dep}] ))
  then
    echo "ERROR: ${dep} is required and is not installed or not found"
    exit 1
  fi
done

# Test for connected camera
if ping -c1 ${1} > /dev/null 2> /dev/null
then
  echo "Connecting to camera ${host}..."
else
  echo "FAILED: Camera ${host} not reachable on network"
  exit 1
fi


# Test for connected camera API enabled
if ! curl -is 'http://'${host}'/control/documentation.html' | head -n 1 | grep -q 200
then
  echo "ERROR: Camera ${host} is not responding as expected. The camera must have the HTTP web media manager enabled without security. Please refer to the Camera Control REST API section of your camera\'s manual for help resolving this issue."
fi

for api in "${SWAGGER_FILES[@]}"
do
  file=$(echo ${api} | sed 's/.*\///')
  dir=$(echo ${api} | sed 's/\/[^\/]*$//')
  
  swagger_codegen ${host} ${dir} ${file} ${outpath}
done

for api in "${ASYNC_FILES[@]}"
do
  file=$(echo ${api} | sed 's/.*\///')
  dir=$(echo ${api} | sed 's/\/[^\/]*$//')
  
  async_codegen ${host} ${dir} ${file} ${outpath}
done

