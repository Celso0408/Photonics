# Photonics

1. Generate the GIF
2. h5ls ez.h5
3. h5topng -t 0:332 -R -Zc dkbluered -a yarg -A wave_guide_bend-eps-000000.00.h5 wave_guide_bend-ez.h5
4. convert wave_guide_bend-e*.png ez.gif
5. run in the base environment 
6. sudo apt install h5utils
