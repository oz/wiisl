#!/bin/sh

if [ 2 != `ps auxww | grep shell-fm | grep -v grep | wc -l` ]; then
    echo 'Starting lastfm daemon'
    sudo service lastfm start
else
    echo 'Stopping lastfm daemon'
    sudo service lastfm stop
fi
