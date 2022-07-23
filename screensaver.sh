#!/bin/bash
process() {
while read input; do 
  case "$input" in
    UNBLANK*)   killall omxplayer.bin ;; # This will kill the omxplayer process
    BLANK*)   omxplayer --loop --no-osd --no-keys "/home/pi/proyecto-vending/pizzaNauta.mp4" & ;; # Don't forget the & on the end or it will never stops, just add your movie file path
  esac
done
}

/usr/bin/xscreensaver-command -watch | process


