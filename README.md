RoboShot
======================

Original project
here https://hectorbot.de/

Minimal Requirements 
---
	- RaspberryPi 3
	- Debian bases Linux (to use installscript)
    - Python 3.8

Prepare Raspberry
---
Activate I2C:

    sudo raspi-config 

Here go to "Interfacing Options" and Activate/Enable I2C 

PWM update:
----
Since this library and the onboard Raspberry Pi audio both use the PWM, they cannot be used together. You will need to blacklist the Broadcom audio kernel module by creating a file /etc/modprobe.d/snd-blacklist.conf with:
    blacklist snd_bcm2835

If the audio device is still loading after blacklisting, you may also need to comment it out in the /etc/modules file.

On headless systems you may also need to force audio through hdmi Edit config.txt and add:

    hdmi_force_hotplug=1
    hdmi_force_edid_audio=1
don't force if you have screen with the flex port.

Install on RaspberryPi
----
First you have to clone the github repo of Hector

	git clone https://github.com/H3c702/Hector9000.git

This repository doesn't contain a frontent. To get the original Hector9000 frontend see: 

	https://github.com/H3c702/Hector9000WebUI

To start the Hector software first move into the directory:

	cd Hector9000

Then run this command to setup all necessary tools:

	./setup.sh

Or run it with the option "-c" to preset the mqtt preconfigure for the WebUI

	./setup.sh -c

To start the software run:

	./start.sh


Add Drinks
---

To add a new Drink you have to modify the `drinks.py` file and add a new item into the `drink_list` array formatted as followed:

	{
        "name": "NAME OF DRINK",
        "recipe": [
            ("ingr", "INGREDIENT1", AMOUNT1),
            ("ingr", "INGREDIENT2", AMOUNT2)
        ]	
    }

All strings in `UPPERCASE` are placeholders, all lowercase strings have to be used literally in the definition. The `INGREDIENTx` names are not cleartext but are identifiers referencing into the `ingredients` list below in the same file. The `AMOUNTx` values are numerical values of the corresponding ingredient's amount in grams.

At the moment there are only some ingredients but feel free to put in some new. You can add them in src/Hector/conf/database.py .
Or you can use the WebUI when it is implemented.

A future extension might allow multi-language UIs.

Add Ingredients
---
To edit the Ingredients that can be used you can edit the 
database.py or use the tool in the tools folder.

    python3 Hector9000/tools/Editingredients.py


Assigning valves
---
The available ingredients are also moved to the db and can initial be edited in the databas.py 
or over the WEB UI in the future.

For the meantime you can use the script "SetValveIng.py".

    python3 Hector9000/tools/SetValveIng.py





Development on non-Hector hardware :
---

In the `HectorServer.py` you have to comment line :
	
	#from HectorHardware import HectorHardware as Hector

and uncomment:

	from HectorSimulator import HectorSimulator as Hector



## Info 

If you have some ideas or a fix or something else to make 
Hector better, don't be afraid to send us a pullrequest ;-)

---
Special thanks to
<div>
  <a>
   Hector 9000 Team
	git clone https://github.com/H3c702/Hector9000.git
  </a>
  <a href="https://www.jetbrains.com/pycharm/">
    <img alt="PyCharm" width="128" heigth="128" hspace="40" src="./images/PyCharm_logo.png">
  </a>

</div>

