# amscope-camera
Python code to control the AmScope camera (model: MU2003-BI).

This is based on the SDK provided by AmScope [(see here)](https://amscope.com/pages/software-downloads) - you will need to search for your camera model and download the appropriate SDK. The Python code was run on an x64 computer for our testing; be sure to use the appropriate .dll file for your computer.

AmScope provides the following files in Python, which are in this repository for reference:
* amcam.py - this file provides an API for the camera. For more information about the API, see [API.pdf](API.pdf).
* simplest.py - this file provides a simple example that opens the camera and grabs frames from the camera, though it does not display these frames.
* qt.py - this file provides an example that grabs frames from the camera and renders them in a GUI.
