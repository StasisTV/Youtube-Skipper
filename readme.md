# Youtube Auto Skipper

![alt text](https://imgur.com/eH1Lm9n.png)

Automatically skips skippable youtube ads

Uses <i><b>OpenCV</b></i> and <i><b>PIL</b></i> to screenshot the screen and detect a <i>"skip ad"</i> button on screen then moves the mouse and clicks on the button


### Settings
- mouseReturn: 
  - If true the mouse will return to its previous position after clicking the skip button
- maxSpeed: 
  - the minimum amount of seconds before screen checks
- sizes: 
  - the array of size mulitpliers to check for the skip button
- threshold: 
  - the minimum maxVal to detect the skip button
- doubleCheck: 
  - If true a "Skip ads" image will be checked for aswell as the default "Skip ad" (large performance hit)
- systemTray: 
  - if disable there will be no system tray icon for the program (not reccommended)

