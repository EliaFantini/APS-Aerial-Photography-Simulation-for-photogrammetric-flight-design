<p align="center">
  <img alt="🛩️Aerial_Photography_Simulation" src="https://user-images.githubusercontent.com/62103572/182640843-de64f439-5458-4d57-8cb9-da0beba42aaf.png">
  <img alt="GitHub commit activity" src="https://img.shields.io/github/commit-activity/y/EliaFantini/APS-Aerial-Photography-Simulation-for-photogrammetric-flight-design">
  <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/EliaFantini/APS-Aerial-Photography-Simulation-for-photogrammetric-flight-design">
  <img alt="GitHub code size" src="https://img.shields.io/github/languages/code-size/EliaFantini/APS-Aerial-Photography-Simulation-for-photogrammetric-flight-design">
  <img alt="GitHub repo size" src="https://img.shields.io/github/repo-size/EliaFantini/APS-Aerial-Photography-Simulation-for-photogrammetric-flight-design">
  <img alt="GitHub follow" src="https://img.shields.io/github/followers/EliaFantini?label=Follow">
  <img alt="GitHub fork" src="https://img.shields.io/github/forks/EliaFantini/APS-Aerial-Photography-Simulation-for-photogrammetric-flight-design?label=Fork">
  <img alt="GitHub watchers" src="https://img.shields.io/github/watchers/EliaFantini/APS-Aerial-Photography-Simulation-for-photogrammetric-flight-design?abel=Watch">
  <img alt="GitHub star" src="https://img.shields.io/github/stars/EliaFantini/APS-Aerial-Photography-Simulation-for-photogrammetric-flight-design?style=social">
</p>

The goal of the project is to create a python program with a graphic interface, capable of
simulating an aerial photograph by applying the collinearity equations to the data contained within a
DEM and an orthophoto, both provided by the user as files in GeoTIFF format.

The left image shows a drawing that explains the different coordinate systems and the parameters to be considered, while the right image shows a possible result of the software.
<p align="center">
<img width="299" alt="Immagine 2022-08-03 172951" src="https://user-images.githubusercontent.com/62103572/182648072-611d0d3e-3757-4f4c-8b2b-e8c0a7e8a8ab.png">
<img width="471" alt="Immagine 2022-08-03 173233" src="https://user-images.githubusercontent.com/62103572/182648812-fc51a8f5-dfcd-45ee-bf6d-de627b1ef749.png">

</p>

## Author
- [Elia Fantini](https://www.github.com/EliaFantini)

## Demo 
![ezgif com-gif-maker (5)](https://user-images.githubusercontent.com/62103572/182819323-883918a3-a2be-4a0f-a4ce-f750057533d6.gif)


## Requirements

The Python programming language was chosen to create the required software. The reason
of this choice is due to the fact that for it there are several libraries extremely optimized for
work on n-dimensional arrays of data. These libraries are:

- RasterIO
- Numpy
- OpenCV
- Scipy

In particular, RasterIO is the library for reading and manipulating the rasters contained in GeoTIFF files.
It was chosen over the standard Python GDAL because, unlike it, it does not suffer from problems with pointers that can crash the program.
For the graphic interface the PyQt5 library was used. The code was executed by a Python interpreter
3.7 in an Anaconda3 environment, since the installation of some libraries such as RasterIO
would have been particularly complicated otherwise.

## How to install

Step 1 Install Anaconda3: 
- download Anaconda 3 from official website: https://www.anaconda.com/products/individual 
- run the executable to install it; 
- always press next and accept default options. 
<br />
Step 2 Create a new environment: 

- open up anaconda prompt as an administrator; 
- write on the terminal 
```bash
conda create -n myenv python=3.7 anaconda 
```
<br />
Step 3 Install libraries: 

- write on the same terminal 
```bash
conda install -n myenv rasterio  
```
- write on terminal 
```bash
conda install -n myenv scipy 
```
- write on terminal 
```bash
activate myenv 
```
- write on terminal 
```bash
pip install opencv-python
```
- write on terminal 
```bash
pip install pyqt5
```
- write on terminal 
```bash
conda list
```
- check if all packages installed correctly; 

<br />
Step 4 Run MainWindowGUI.py: 

- from the same terminal window, with myenv activated, navigate to source file folder with 
“cd” command. 
- Once in the folder containing MainWindowGUI.py and all other source files, write on the 
terminal 
```bash
python MainWindowGUI.py
```
If everything went fine, APS’s should now open. 

## How to use
**The dataset in the Data folder contains a compressed version of the original orthophoto file, which originally was 200MB. There was no GeoTIFF compressor available online so it is put there just to be visualized but it won't work in the software as it lacks the geographical informations which make a TIFF image a GeoTIFF image. If anyone would like to try the software on my dataset feel free to open an issue or contact me and I will provide a cloud link to download the whole file.**

The graphic interface allows the user to set the following parameters: 
- File path of the orthophoto in .tif format. the user may choose to manually write the path 
to the file or select it by clicking the browse button. If the path does not exist or the file 
valid file, the path is automatically reset; 
- File path of the DEM in .tif format. Similar functionality to the file path above; 
- File path of the .txt text file containing the names of the images to be simulated, the coordinates of the 
centre of take of each of them (X, Y, Z) and their three attitude angles (ω, φ, ϰ), and 
optionally, the rotation matrix (direct cosines). These parameters shall be provided 
spaced by a single tabular key character (HT) and in the following order: PhotoID, X, Y, Z, 
Omega, Phi, Kappa, (r11, r12, r13, r21, r22, r23, r31, r32, r33). Each set of parameters shall be 
separated from the previous one by an Enter character ("\n"). This format reflects that generated 
automatically by various photogrammetry software; 
- Path of the folder in which the processed images are to be saved; 
- Photographic sensor size (mm x mm), selectable from several presets; 
- Resolution of the simulated photograph, selectable from several presets; 
- Customised sensor size and image resolution, selectable manually 
by clicking the button marked "..."; 
- Focal length of the camera in mm (distance of the grip centre from the sensor); 
- Main point co-ordinates (ξ,η) in mm (co-ordinates of the projection of the grip centre on the 
sensor); 
- Resampling algorithm applied in the process of rototranslation of the DEM file to make 
correspond, in the georeferenced 3-dimensional space, the elevation information of the pixel (i,j) 
in the DEM to the RGB colour information of pixel (i,j) in the orthophoto; 
- Resampling algorithm applied to the simulated image to fill pixels without information.

The following image shows the settings interface:

<img width="auto" alt="Immagine1" src="https://user-images.githubusercontent.com/62103572/131254214-5a0a912d-edce-4103-8608-7ad5c6fdd5ba.png">


The two following images represent the dataset I was given (left: orthophoto - right: DEM):
<p align="left">
<img width="400" alt="Immagine1" src="https://user-images.githubusercontent.com/62103572/131254218-f573315c-0bc6-4bc7-8580-f713d419476d.png">
<img width="400" alt="Immagine1" src="https://user-images.githubusercontent.com/62103572/131254217-fb1955ef-4bb9-4dd3-856e-a24691a0d529.png">
</p>

Once pressed start, a loading bar will tell how much time is left. The following image shows the result of a random 80x80mm camera sensor's simulated photo:

![Immagine4](https://user-images.githubusercontent.com/62103572/131254211-a8724372-3635-486e-a14b-7636eba40530.jpg)

For a more detailed description of how the code works and some example with more extreme paramaters settings, such as with strongly a angled camera which will have stronger prospective distortions, read the abstract file ( the pdf is written in italian, I suggest the use of an automated translation tool).

## 🛠 Skills
Python. Collinearity equations, basics of photogrammetry. Usage of Python GUI libraries.

## 🔗 Links
[![portfolio](https://img.shields.io/badge/my_portfolio-000?style=for-the-badge&logo=ko-fi&logoColor=white)](https://eliafantini.github.io/Portfolio/)
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/-elia-fantini/)


