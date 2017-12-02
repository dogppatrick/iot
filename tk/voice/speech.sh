#!/bin/bash
say() { local IFS=+;/usr/bin/mplayer -volume 100 -ao alsa -really-quiet -noconsolecontrols "http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q=$*&tl=En-gb"; }
say $*
