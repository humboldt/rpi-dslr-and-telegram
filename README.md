# DSLR & Telegram
This is a python script, which runs on the Rasperry Pi (Raspbian).
It allows the user to send commands via the Telegram messenger to control a DSLR.

This script needs two add-ons to run:
- Telepot: https://github.com/nickoala/telepot
- gPhoto2: https://github.com/gonzalo/gphoto2-updater

Please make sure your OS is up to date!

##### The chat syntax

Chat Command    |Description
----------------|----------------------------
/start    		|Start the bot
/info 			|Returns syntax information
/getCam 		|Returns connected cameras			
/getISO 		|Returns available ISO values
/setISO <value>	|Sets ISO value
/getAV 			|Retunrs available AV value
/setAV <value>	|Sets AV value
/getTV 			|Returns available TV value
/setTV <value> 	|Sets TV value
/pic 			|Takes picture and sends it

##### Furter information.
More about this software, and how to use it:
--- no blog link ---