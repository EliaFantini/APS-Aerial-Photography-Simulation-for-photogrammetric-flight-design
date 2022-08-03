<p align="center">
  <img alt="🛩️Aerial_Photography_Simulation" src="https://user-images.githubusercontent.com/62103572/182640843-de64f439-5458-4d57-8cb9-da0beba42aaf.png">
  <img alt="GitHub commit activity" src="https://img.shields.io/github/commit-activity/y/EliaFantini/edU-command-line-text-editor-w-multiple-Un-Redo">
  <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/EliaFantini/edU-command-line-text-editor-w-multiple-Un-Redo">
  <img alt="GitHub code size" src="https://img.shields.io/github/languages/code-size/EliaFantini/edU-command-line-text-editor-w-multiple-Un-Redo">
  <img alt="GitHub repo size" src="https://img.shields.io/github/repo-size/EliaFantini/edU-command-line-text-editor-w-multiple-Un-Redo">
  <img alt="GitHub file count" src="https://img.shields.io/github/directory-file-count/EliaFantini/edU-command-line-text-editor-w-multiple-Un-Redo">
  <img alt="GitHub follow" src="https://img.shields.io/github/followers/EliaFantini?label=Follow">
  <img alt="GitHub fork" src="https://img.shields.io/github/forks/EliaFantini/edU-command-line-text-editor-w-multiple-Un-Redo?label=Fork">
  <img alt="GitHub watchers" src="https://img.shields.io/github/watchers/EliaFantini/edU-command-line-text-editor-w-multiple-Un-Redo?abel=Watch">
  <img alt="GitHub star" src="https://img.shields.io/github/stars/EliaFantini/edU-command-line-text-editor-w-multiple-Un-Redo?style=social">
</p>

# AERIAL-PHOTOGRAPHY-SIMULATION-FOR-PHOTOGRAMMMETRIC-FLIGHT-DESIGN-

The goal of the project is to create a python program with a graphic interface, capable of
simulating an aerial photograph by applying the collinearity equations to the data contained within a
DEM and an orthophoto, both provided by the user as files in GeoTIFF format.

The Python programming language was chosen to create the required software. The reason
of this choice is due to the fact that for it there are several libraries extremely optimized for
work on n-dimensional arrays of data. These libraries are:

- RasterIO
- Numpy
- OpenCV
- Scipy

In particular, RasterIO is the library for reading and manipulating the rasters contained in GeoTIFF files.
It was chosen over the standard Python GDAL because, unlike it, it does not suffer from
problems with pointers that can crash the program.
For the graphic interface the PyQt5 library was used. The code was executed by a Python interpreter
3.7 in an Anaconda3 environment, since the installation of some libraries such as RasterIO
would have been particularly complicated otherwise.
## INTERFACE AND RESULTS

- Settings interface

<img width="482" alt="Immagine1" src="https://user-images.githubusercontent.com/62103572/131254214-5a0a912d-edce-4103-8608-7ad5c6fdd5ba.png">

- Given dataset: orthophoto and DTM

![Immagine2](https://user-images.githubusercontent.com/62103572/131254218-f573315c-0bc6-4bc7-8580-f713d419476d.png)

![Immagine3](https://user-images.githubusercontent.com/62103572/131254217-fb1955ef-4bb9-4dd3-856e-a24691a0d529.png) 

- Result of a 80x80mm camera sensor's simulated photo

![Immagine4](https://user-images.githubusercontent.com/62103572/131254211-a8724372-3635-486e-a14b-7636eba40530.jpg)


## HOW TO INSTALL AERIAL PHOTOGRAPHY SIMULATION 

Step 1 Install Anaconda3: 
- download Anaconda 3 from official website: https://www.anaconda.com/products/individual 
- run the executable to install it; 
- always press next and accept default options. 
<br />
Step 2 Create a new environment: 

- open up anaconda prompt as an administrator; 
- write on the terminal “ conda create -n myenv python=3.7 anaconda “ and press enter. 
<br />
Step 3 Install libraries: 

- write on the same terminal “ conda install -n myenv rasterio “ and press enter; 
- write on terminal “ conda install -n myenv scipy “ and press enter, it might be already 
installed; 
- write on terminal “ activate myenv “ and press enter; 
- write on terminal “ pip install opencv-python ” and press enter; 
- write on terminal “ pip install pyqt5 ” and press enter; 
- write “conda list” and check if all packages installed correctly; 
<br />
Step 4 Run MainWindowGUI.py: 

- from the same terminal window, with myenv activated, navigate to source file folder with 
“cd” command. 
- Once in the folder containing MainWindowGUI.py and all other source files, write on the 
terminal “ python MainWindowGUI.py “ and press enter; 
- If everything went fine, APS’s should now open. 
