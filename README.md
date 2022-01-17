# RedMinerIDLE
## Why using this script ?
The Windows Task Scheduler does a very poor job at doing precision scheduling. Its also both confusing and honestly kinda trash (specially compared to linux services and such). This script will run and trigger your mining software automatically but will also properly kill it<sup>1</sup>. Its simple, reliable and configurable to your specific needs with a bit of python.

<sup>1</sup> The teamredminer program do not listen to the STDIN, meaning its impossible to send the `q` command to it. Because of this, any overclocking setting set as argument on the `teamredminer.exe` program won't be properly reverted. 

## Setting the windows task
Create a Task in your Task Scheduler on Windows. For the general setup, make sure to set the following:

* Run only when user is logged in
* Run with highest privileges
* Hidden
* Configure for: Windows 10

For the triggers, you'll require 2 of them:

* At system startup
* At task creation/modification

Finally for the action, use the start a program command. For the script, using Python 3.8, select your `pythonw.exe` (do not use `python.exe` because you'll see a command window). Make sure the task starts inside your teamredminer folder with the `idle_miner.pyw` inside. Finally add `idle_miner.pyw` as argument.

## Configuring the script
You have to set a couple of settings for the miner to properly work:

* **On line 27**, you can change how many seconds of idleness is needed for the miner to start, defaults to 5 minutes (300 seconds).
* **On line 52**, you have to set your pool's url and port. 
* **On line 53**, you can set your prefered configuration for ethash.
* **On line 54**, you have to set you address and worker name.

__Note__: This is only the basic configuration, read the [teamredminer github](https://github.com/todxx/teamredminer) for more in-depth settings.

## Look at the miner's logs
The STDOUT and STDERR of the miner and the script are sent to the `output.log` file in the same folder. You can watch it in realtime using the PowerShell command: `Get-Content output.log -wait` inside the folder.
