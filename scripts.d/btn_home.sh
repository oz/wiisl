#!/bin/sh

VOL_FILE="/tmp/volume"

echo 'btn home'
if [ -f "$VOL_FILE" ]; then
    echo 'unmute'
    amixer sset Master `cat $VOL_FILE`
    rm $VOL_FILE
else
    echo 'mute'
    current_vol=`amixer sget Master | sed -n '/Left: Playback /s/.* \([0-9]\+\) \[.*/\1/p'`
    echo "$current_vol" > "$VOL_FILE"
    amixer sset Master '0'
fi
