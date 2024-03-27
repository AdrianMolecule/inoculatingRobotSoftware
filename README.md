All screws are 3 mm except frothe metal bed fastening ones that are 5 mm ( the four large ones)
There are 2 layers to the bed. The bottom layer and the toplayer which is the framelayer where labware modules go.

I provided the original Fusion360 files so you can change the parameters (from Design mode/Modify/change parameters. The last several operations in the design history sometimes contain a cutting rectangle to print just a small section of the final product to test for fit. They can be disables by moving down in history (bottom) several steps until you see the full body.
All CNC cutting is done with 2 mm 2 flute end mill. The cheap ones work fine.
In case the bed is not perfectly flat and you use wood you can do a facing operation to make it paralel. That should  work with plastic too.
If you want to be cheap and fast you can use 3.175 mm mdf of plywood. Make sure it's flat. You can use HDPE plastic or ABS. In my case I used a thick 7 mm MDF base with a thick 8ish mm frame.  Neither thicknesses are important but you will have to adjust the cutting depth for your cut thickness or use a spoil board.
For the bed you can use acrylic, either 1/8 or 1/4 inch for the base and 1/8 for the frame.
There are extra holes in case you want to use more screws to attach the plasticware like Petri dish holder to the bed.
The frame and the base are attached to the aluminum machine bed with the 4 thick screws. I had only small t-nut metal sliders so I printed an adapter so they don't come out loose. You can use directly the appropriate size t-nuts that slide in your bed. I think some will come with the machine. I use a cheap 3018 clone that is similar to https://www.sainsmart.com/products/sainsmart-genmitsu-cnc-router-3018-pro-diy-kit
I printed in ABS as I always do but PLA or something more advance should work too. The claws on the Petri dish holder are easy to break under larger force. A super fast acetone dunk of the holder or a vapour treatment (Google acetone vapours ABS) - will make them stronger. Breaking the claws will not affect functionality as long as you still have some left.
After you print the plastic pieces you have to remove the spindle and push in the head attachment. After that connect the loop holder with the 2 screws. You can use regular nuts not the cylinder ones like I did. The hole for the inoculating loop is intentinally left large to accomodate any size. The model will print 2 additional plastic shims to bridge that gap if necessary. You can use tape around the loop handle if you need it but the 2 screws that tighten the lopp handle should be enough.
The slots are same size as Opentrons's slots (slotSizeX=127.76; slotSizeY=85.48 ) and the plate is also incuded in the Opentrons library. See comment and url in the software. I used an OS compatibility wrapper called pyLabRobot that is intended to allow you to write the code once and execute it on several robots like Hamilton, Opentrons etc.
    # https://docs.pylabrobot.org
	
My code is only several files all under labRobot in GitHub. Just copy them in a local directory, make sure pylabrobot is installed and go. Places where you need (media  z distance) or might want to make adjustments are tagged with "#change here" so do a search for that string in the code.
	the start point file is start.py. There are unused files that might be useful so only the files referred fromstar.py are mandatory.
The gnerated gcode file is called gcode.txt and that is what you load in Candle.

As per industrial robots you need a general calibration and sometimes an experiment calibration.
If you don't have limits on your machine which is what happens to mine you need to set zeroes manually. Use the Candle or other software and move the robot until the top of the loop barely touches the bed and set Z =0. Then lift and bring the tip in the lower left corner of the lower left slot and hit X=0 Y=0.

After that it would be good to check a simple program that goes to a well in the plate let's say H12. Check that it goes there properly and readjust the XY if necessary.

The loop interior diam is < 1mm. It transferred about 20% of a 360ul well into about 200 points so about .3 ul per drop. That is probably better than a regular pipette for this purpose. It's good to have small volumes.

If you don't have a 96 well plate ask me to design some simple container.

Similar to the industrial robots you need to 'calibrate  the height of the medial in the agar plate". Put the plate with agar in and lower the loop until it barely touches the top of the LB.Agar media. Take the z value and assign it to calibrationMediaHeight in a.py.


It's good to test with something simple as a big plus sign that put a drop in the middle of the plate and 4 more around. Just uncomment the call to drawBibPlusSign in a.py.

In order to 'draw/inoculate something' you need a file with the dots saved in a x, y 'Python format".
The subdirectory called /images contain some code like imageToDotsArrayNoFiles.py to take a file and produce an outline and an array of dots. You can change the block size to get dots within the -40 and +40 for the dots. The dots are relative to the center of the Petri dish which is about  -  diameter = 84.8 mm interior diameter (see adUtil.py/createPetri... if you want to change it which should not be necessary. You don't need taht directory if you want to produce the array using othre means.

It's OK to stab the agar but it's even better if you just touch the surface of the Agar. You will see the liquid held in the eye of the loop sucked in the media when the loop touches the surface. 
To my surprise, I managed to achieve the from the first try but it's possible the agar surface is not horizontal so it might not touchdown in somecases. Don't worry. Change the calibrationMediaHeight with a lower value and re-run the program.
I used GFP in the MarpleLeaf.
My first try was with about 150 points and it lasted about 1 hour. If you change the value of safe_z to a lower value and the allocation of the source well to a closer one you should be able to cut that down to 30 min.
I 'flame' my loop directly in the machine. If you don't have a loop check out our web at specyal.com on how to make one based on another article by this great guy Alex.
The CNC machine is "as it was in the box". I payed about 200 US$ for it. There are kits to extend x and y and maybe z. The system should run on a different machine but some elements will probably need redesign. I might add some auto zero limit switches.
The precision is very good, probably around .3 mm mostly due to play as the internal precision is much better.
The Opentrons's bays are 1 2 and 3 on the bottom row and 4,5,6 on next one etc. That is why my top left slot is 4 not 3 as it would normally be. The simulator will show you where to put labware and the picture with the points you will get. The zoom is not updating the picture at this point but that should not be an issue.
All works well and it took several months of work to get it where it is. It was done while juggling several things including TA-ing on the HTGAA.org
Shuld the community like it, I will continue adding features. My main interest is molecular biology so I consider this as enablement.

I hope to add a microscope to it. Most likely based on OpenFlexure.