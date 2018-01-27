# RPi: DSLR & Telegram

## 1 Description

This is a small python script, which runs on the Rasperry Pi (Raspbian). It allows you to send commands via the Telegram messenger to control a DSLR.

This scripts dependecies are:
- Telepot: https://github.com/nickoala/telepot
- gPhoto2: https://github.com/gonzalo/gphoto2-updater

For a more detailed description feel free to visit my website:

- [English](http://deloarts.com/en/scripts/raspberry/telegram-bot).
- [German](http://deloarts.com/de/scripts/raspberry/telegram-bot).

### 1.1 Chat syntax

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

## 2 License

This project is licensed under the GNU GPLv3 open source license. Thus anybody is allowed to copy and modify the source code, provided all changes are open source too and the author is in knowledge of all done changes. This can happen either via eMail or directly on GitHub, in other words at this repository.

## 3 Disclaimer

I am not responsible for anything in conjunction with this project, including bugs, failure, fire, harm of equipment and harm of persons. Reasonably foreseeable misapplication:

- Bug in the code
- Failure of used parts due to a bug in the code or a wrong wiring diagram, including a wrong design.
- Fire due to a wrong wiring diagram, including a wrong design.
- Harm of equipment, meaning third party parts (cameras, flashes, etc.) due to a bug in the code or a wrong wiring diagram, including a wrong design.
- Harm of persons due to any failure of the system, a wrong wiring diagram or a wrong behaviour.

**It is your own responsibility to use these contents**. Be careful, this project includes lethal electrical voltage. Put yourself in knowledge about the risks before you start with this project.