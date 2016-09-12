# General Notes
- The default value of *savepath* can be edited in the script
- The images are captured with an ImageJ call `opener.openURL("http://foo.com/bar.jpg")` This is **not** a call to the standard Micro-Manager camera and is probably unique to the setup at the CNI. If someone wants to change this and submit a pull request, please feel free

# Using the quick capture script:

- Start Micro-Manager and load your hardware configuration
- Open the *Script Panel* in the *Tools* menu
- Open the *Stage_Quick_Capture.bsh* script
- Click *Run* when ready to begin, you can also add the script to the list of shorcuts

![micromanager screenshot](https://github.com/BWHCNI/workflow/blob/master/micro-manager/imgs/Capture1.png)

- When the script start you'll be asked if you want to zero the stage
- Position the stage where the origin of the coordinates should be and click *Ok*. Traditionally we have used the intersection of the holder and the chip in position 1

![micromanager screenshot](https://github.com/BWHCNI/workflow/blob/master/micro-manager/imgs/Capture2.png)

- After zeroing the window below will appear

![micromanager screenshot](https://github.com/BWHCNI/workflow/blob/master/micro-manager/imgs/Capture3.png)

- Set the correct values in the window, position the stage at the point you wish to record, and click *Ok*
- Every time the *Ok* button is pressed an image will be captured and the coordinates of the stage and the mag/chip#/notes are recorded
- When you are finished recording points click *Cancel*
- The list of points is written to the file *xy.points.csv*
- Here is an [example list of points](https://github.com/BWHCNI/workflow/blob/master/micro-manager/imgs/xy.points.csv)

| Image      | X-coordinate  | Y-coordinate  | Mag  | chip  | notes  | 
|------------|---------------|---------------|------|-------|--------| 
| image-001  | -0.0          | -0.0          | 10X  | 1     | Test 1 | 
| image-002  | -10.0          | -20.0          | 10X  | 1     | Test 2 | 
| image-003  | -20.0          | -10.0          | 10X  | 1     | Test 3 | 

- The list of points is also transfered to the *Point List* in Micro-Manager, so they can be reviewed if needed
- Note that currently they need to be manually saved in the *Point List* format if desired 

![micromanager screenshot](https://github.com/BWHCNI/workflow/blob/master/micro-manager/imgs/Capture4.png)

- The images and csv file can be passed to our [nikon_rotate_lable script](https://github.com/BWHCNI/workflow/tree/master/nikon_rotate_label)
