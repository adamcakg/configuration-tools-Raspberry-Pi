
# Configuration tools for Raspberry Pi OS
This configuration tool helps with setting up the operating system as well as it helps with maintaining it.



This repository contains two configuration tools.
  - First start utility
  - Settings utility
 
 
### First start utility
 
 <img width="389" alt="first_1" src="https://user-images.githubusercontent.com/51970723/106365166-03e94300-6334-11eb-86d1-ceab8844d978.png">
 
 
### Settings utility

System settings are also one of the main parts of the operating system. They are created modularly, so there is no problem with adding new screens, removing them or changing the order in the application.

 <img width="462" alt="sett_1" src="https://user-images.githubusercontent.com/51970723/106365217-490d7500-6334-11eb-9875-335bdd594673.png">
 

### Extensibility

Each screen in applications is represented by a separate direcotry in the application. The screen consists of at least the following files:
 - \__init__.py - screen initialization file
 - handler.py - the functions in this file take care of events that occur on given screen
 - .glade file - a page layout is defined in this file

In both applications, default blank screen is created, so creating new screens is easy.



This tools was designed to be extensible as much as they can. Feel free to extend them as you like.


### Installation
There are no dependencies. Simply download and go to the directory:

```sh
$ cd {repository}
```

Then simply run the command:

```sh
$ sudo python3 setup.py
```

If we want show the first start utility right after the Raspberry Pi boots up we need to add additional parameter when installing.
```sh
$ sudo python3 setup.py -i
```


The settings utility is accesible through menu of the Raspbian operating system.

<img width="354" alt="settings_menu" src="https://user-images.githubusercontent.com/51970723/106365690-655ee100-6337-11eb-835d-2fbafd5616f3.png">


### Contribution
We will be happy if you contribute :)
Big thanks to all the contributors!


