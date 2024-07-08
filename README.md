# All Out Hell Simple Mapper

A simple script to quickly sew together a map of an [All Out Hell](https://all-out-hell.fandom.com/wiki/All_Out_Hell_Wiki) suburb from a bunch of screenshots.


### Requirements ###

 * Python 3 interpreter
 * [Pillow](https://python-pillow.org) library (In Debian: `python3-pil` package)


### Usage ###

`./aoh_mapper.py -i input.txt -o output.png`


### Input file syntax ###

Input file contains a series of lines, either listing a screenshot file with a fragment of the map, or directing the map builder. Empty lines are ignored. The example file is in this repository.

The possible lines are:

 * `:target x_min y_min x_max y_max`: the in-game GPS coordinates of the corners of the resulting map. One and only one line of this type must be included in the input file.
 * `:mapxy x y`: the pixel coordinates of the top left corner of the map in a screenshot. There must be at least one line of this type before any screenshot entries, and it affects every screenshot after it until the next `:mapxy` line (if there is one). NOTE: it must be the coordinates of the map tile itself, not the black frame around the map.
 * `path/to/screenshot gps_x gps_y`: the path to a screenshot, along with the in-game GPS coordinates of the central tile.
