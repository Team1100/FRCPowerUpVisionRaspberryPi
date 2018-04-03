# How to have the pi automatically run client.py
You may know that you can run a python file in a CLI with python3 client.py
We are going to edit the file /etc/rc.local. The script already runs on startup, and all it does is output the Pi's IP address once, so you can easily add our command at the end of the file.

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
