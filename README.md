project is functional, stabile and has been tested. No immediate plans to change and no outstanding bugs.
see https://github.com/AdrianMolecule/inoculatingRobot/tree/main/documentation readme for most instructions.


This contains two different parts, the main robot software and an utility to convert image files into files with dot coordinates that can be loaded by the robot file and "painted" on a Petri dish.
The image convertor is at:
https://github.com/AdrianMolecule/inoculatingRobotSoftware/blob/main/image/dist/ImageConverter.exe
You can use that to load an image file and convert it to an .npy file that contains coordinates of points.


You sould really use create a real development environment for the main part because after all you want to change the code.
Just in case you just want to just use inoculate the image as produced by the imageConverter you can download just dist/labRobot folder and click on the labrobot.exe afterwards in Windows. Please be aware that at the start a message box appears and you need to press OK for the main window to appear. Sometimes the messagebox appears under the main window and unless you switch to it and press OK you are stuck. That is annoying so I will fix that but I need to repack so it's not high on my list now.
