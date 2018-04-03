# How to have the pi automatically run client.py

 1. Navigate to /etc/
 2. Give yourself permssion to edit /etc/rc.local
 
        sudo chown pi:pi ./rc.local
 3. Begin editing ./rc.local
 
        vi rc.local
 4. Arrow down to the line before "exit 0". Add the following:
 
        sudo python3 /home/pi/vision/client.py &
 5. Save and quit:
 
        :w
        :q
 6. Test it out. Code should run ~10s after boot:
 
        sudo reboot
