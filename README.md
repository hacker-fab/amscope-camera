# amscope-camera
Python code to control the AmScope camera (model: MU2003-BI)

This is based on the SDK provided by AmScope [(see here)](https://amscope.com/pages/software-downloads) - you will need to search for your camera model and download the appropriate SDK.

For our project, we used their Python base code which grabs frames from the camera. AmScope provides the following files:
* amcam.py - this file provides an API for the camera. For more information about the API, see API.html.
* simplest.py - this file provides a simple example that opens the camera and grabs frames from the camera, though it does not display these frames.
* qt.py - this file provides an example that grabs frames from the camera and renders them in a GUI.
