fa2icon
=========
A python script to convert font awesome fonts to icons.


Install
=========

install dependant python modules

```
% easy_install -U PIL
% easy_install -U tinycss
```

Run
=========

```
% ./fa2icon.py -h
Usage: ./fa2icon.py [options]
 -h|--help		Print this message
 -v|--verbose		Print debug info
 --update		Update the latest ttf and css files from github
 -c|--color=<color>     The color used to fill texts, can be #rrggbb or color names, default "white"
 --size=<size>		The canvas size of generated images, default 100
 -d|--dir=<dir>		The directory where generated images stores, default ./icons
 --filetmpl=<tmpl>	The filename template, default %s.png
```
