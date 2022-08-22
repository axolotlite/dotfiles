#!/bin/bash
arr=($(python -m rotate))
orientation=${arr[0]}
arr=(${arr[@]/$orientation})
touchpad=${arr[-1]}
coords=${arr[@]/$touchpad}
#condition to check if a change happened
case $orientation in
    "normal" )
        swaymsg output eDP-1 transform 0;
        swaymsg input 1:1:AT_Translated_Set_2_keyboard events enabled
        echo "This is normal";;
    "inverted" )
        swaymsg output eDP-1 transform 180;
        swaymsg input 1:1:AT_Translated_Set_2_keyboard events disabled
        echo "The screen is inverted";;
    "left" )
        swaymsg output eDP-1 transform 270;
        swaymsg input 1:1:AT_Translated_Set_2_keyboard events disabled
        echo "The screen should be left";;
    "right" )
        swaymsg output eDP-1 transform 90;
        swaymsg input 1:1:AT_Translated_Set_2_keyboard events disabled
        echo "The screen should be right";;
esac
swaymsg input type:tablet_tool calibration_matrix $coords
swaymsg input type:touch calibration_matrix $coords
swww img -o eDP-1 ~/Pictures/wallpapers/default.gif
# echo $orientation $coords $touchpad