#!/bin/bash

ANKI_PLUGIN=~/Library/Application\ Support/Anki/plugins

#echo $ANKI_PLUGIN

cp -f mcdsupport.py "$ANKI_PLUGIN/"
cp -Rf mcd "$ANKI_PLUGIN/"

