
# Configuration tools for Raspberry Pi OS
This configuration tool helps with setting up the operating system as well as it helps with maintaining it.



This repository contains two configuration tools.
  - First start utility
  - Settings utility
 
 
### First start utility
 
 <img width="389" alt="first_1" src="https://user-images.githubusercontent.com/51970723/106365166-03e94300-6334-11eb-86d1-ceab8844d978.png">
 
 
### Settings utility
 <img width="462" alt="sett_1" src="https://user-images.githubusercontent.com/51970723/106365217-490d7500-6334-11eb-9875-335bdd594673.png">
 

### Extensibility
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

### Contribution
We will be happy if you contribute :)
Big thanks to all the contributors!


