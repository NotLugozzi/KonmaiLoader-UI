# KonmaiLoader
funny haha loader for most (take that with a grain of salt) dll-based bemani titles. Fully backwards compatible with spice/BT5

## Features (or rather, why did i do this)
The project started when i first tried to boot up a dll-based game on my steam deck and all i could get was a hard crash and having to reboot the device. I tried looking into the old loader's source code but i couldn't understand it - so i just started making my own, and i went with rust for it.

The main goals of this one were live patching, which basically means copying the game's binary, patching it at runtime and deleting it once the game disposes devices and kills the audio backend. Allowing you to have clean data for troubleshooting, it then adds some QoL features such as:
- Better Discord RPC! Now all your friends can see you spend 17 hours on sdvx every single day! (KFC and LDJ/TDJ only for now)
- Built-in Nvcuda/nvcuvid binaries. Helps with playing newer KFC builds on amd/intel arc cards
- Easier steam hooking for getting the game to run under proton without too many hiccups.
- Last, but not least - a nice new UI made in Dart and Flutter, with material you support and with game autodetection/easier setup. 


it also adds openshock support if you're into that, allowing you to send events on track fail and on a score threshold [wip as in i need to get working on it lol]



Sadly since the loader itself is still in early stages all we can provide now is the UI that (should) be fully backwards compatible with Spice and BT5, although there is still more code cleanup to do.


Now, if you *really* want to try this god awful clump of spaghetti code let's move onto building.

## Building and testing

to build you'll need the following:

- Flutter (any recent version will do)
- NuGet (necessary for some webview stuff)
- MsBuild 2019 (we strongly suggest 2022)
- Python (anything >3.10 will do)

Building in debug mode is fairly easy:  

clone the repository using git:
`git clone https://github.com/NotLugozzi/KonmaiLoader-UI.git`   


cd into the konmailoader-ui folder
`cd KonmaiLoader-UI`   


run flutter and select desktop target
`flutter run`   



## Contributing:
You can easily contribute to the UI by opening an issue/submitting a PR. for now access is limited to the half broken dart ui but we will later expand to the loader's rust files and the ui variants, including GTK4, Qt5
