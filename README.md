# py_gear_gen
An Involute spur gear generation library I made due to not finding any gear existing free software with ring gear functionality to my liking. 
This was my first foray into the geometry of gear profile generation, so don't be surprised if you find errors within the mathematics. 

## Features
- Involute profile of adjustable accuracy.
- Gear root filleting.
- Internal ring gearing option.
- Adjustable module, tooth number, and pressure angle (14.5 and 20 tested) 
- Adjustable backlash, to allow for manufacturing tolerances. 

## Showoff 
Check out the uploaded SVG files to see the gears I used to model the planetary gearset in the below image. 
Note that these were made at a fairly low `max_steps` accuracy of 100, so the involute profile is a bit innacurate. 

In order to compensate for a less accurate profile, increase the backlash so that gears will still mesh, albeit with some angular play. 

![Planetary Gearset](https://github.com/heartworm/py_gear_gen/raw/master/example_planetary.png)

## Documentation
For now check out `example_usage.py` and the comments within `involute_gear.py` for usage details. 

## TODO
- Working DXF file output. 
- Review all mathematics and algorithms. 
- Get fillets working on internal gears
- STL file output for helical and other funky gears. 
