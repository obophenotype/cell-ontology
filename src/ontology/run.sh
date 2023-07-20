#!/bin/sh
# Wrapper script for docker.
#
# This is used primarily for wrapping the GNU Make workflow.
# Instead of typing "make TARGET", type "./run.sh make TARGET".
# This will run the make workflow within a docker container.
#
# The assumption is that you are working in the src/ontology folder;
# we therefore map the whole repo (../..) to a docker volume.
#
# To use singularity instead of docker, please issue
# export USE_SINGULARITY=<any-value>
# before running this script.
#
# See README-editors.md for more details.

if [ -f run.sh.conf ]; then
    . ./run.sh.conf
fi

# Look for a GitHub token
if [ -n "$GH_TOKEN" ]; then
    :
elif [ -f ../../.github/token.txt ]; then
    GH_TOKEN=$(cat ../../.github/token.txt)
elif [ -f $XDG_CONFIG_HOME/ontology-development-kit/github/token ]; then
    GH_TOKEN=$(cat $XDG_CONFIG_HOME/ontology-development-kit/github/token)
elif [ -f "$HOME/Library/Application Support/ontology-development-kit/github/token" ]; then
    GH_TOKEN=$(cat "$HOME/Library/Application Support/ontology-development-kit/github/token")
fi

ODK_IMAGE=${ODK_IMAGE:-odkfull}
TAG_IN_IMAGE=$(echo $ODK_IMAGE | awk -F':' '{ print $2 }')
if [ -n "$TAG_IN_IMAGE" ]; then
  # Override ODK_TAG env var if IMAGE already includes a tag
  ODK_TAG=$TAG_IN_IMAGE
  ODK_IMAGE=$(echo $ODK_IMAGE | awk -F':' '{ print $1 }')
fi
ODK_TAG=${ODK_TAG:-latest}
ODK_JAVA_OPTS=${ODK_JAVA_OPTS:--Xmx16G}
ODK_DEBUG=${ODK_DEBUG:-no}

TIMECMD=
if [ x$ODK_DEBUG = xyes ]; then
    # If you wish to change the format string, take care of using
    # non-breaking spaces (U+00A0) instead of normal spaces, to
    # prevent the shell from tokenizing the format string.
    echo "Running ${IMAGE} with ${ODK_JAVA_OPTS} of memory for ROBOT and Java-based pipeline steps."
    TIMECMD="/usr/bin/time -f ### DEBUG STATS ###\nElapsed time: %E\nPeak memory: %M kb"
fi

VOLUME_BIND=$PWD/../../:/work
WORK_DIR=/work/src/ontology

if [ -n "$ODK_BINDS" ]; then
    VOLUME_BIND="$VOLUME_BIND,$ODK_BINDS"
fi

if [ -n "$USE_SINGULARITY" ]; then
    
    singularity exec --cleanenv $ODK_SINGULARITY_OPTIONS \
        --env "ROBOT_JAVA_ARGS=$ODK_JAVA_OPTS,JAVA_OPTS=$ODK_JAVA_OPTS" \
        --bind $VOLUME_BIND \
        -W $WORK_DIR \
        docker://obolibrary/$ODK_IMAGE:$ODK_TAG $TIMECMD "$@"
else
    BIND_OPTIONS="-v $(echo $VOLUME_BIND | sed 's/,/ -v /')"
    docker run $ODK_DOCKER_OPTIONS $BIND_OPTIONS -w $WORK_DIR \
        -e ROBOT_JAVA_ARGS="$ODK_JAVA_OPTS" -e JAVA_OPTS="$ODK_JAVA_OPTS" \
        --rm -ti obolibrary/$ODK_IMAGE:$ODK_TAG $TIMECMD "$@"
fi

case "$@" in
*update_repo*|*release*)
    echo "Please remember to update your ODK image from time to time: https://oboacademy.github.io/obook/howto/odk-update/."
    ;;
esac