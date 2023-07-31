Adaptation of Python Annotator for VideoS repository for the Drosophila Grooming labeling and analysis.

# Instructions

1. Open the folder containing the code in terminal.
2. Install requriments with the following command:
```
pip install -r requriments.txt
```
3. In folder *Required software for Windows* run *K-Lite_Codec_Pack_1532_Basic.exe* (installation will open, in most cases you can just click Next all the way)
4. Open the folder in Visual Studio Code
5. Run the cropper.py (by opening the file in Visual Studio Code and pres F5). Do the cropping
6. Run the pasv.py and do the labeling.

---
---

# PAVS Repo Readme

## Python Annotator for VideoS
PAVS - A simple video labeling tool developed in PyQt5 for managing the dataset of the ASDetect Project

Annotate videos in common formats(mp4, avi, mkv, wav, mp3)

You can easily annotate video files per frame or in groups and label the video files either based on their category or create a custom label.
In the example below we have annotated an mp4 file. You can see the video player and the data after annotating the particular frames. This data table can be exported and imported into a CSV File.
Refer help.txt before proceeding with the usage of the application.

![example](https://raw.githubusercontent.com/kevalvc/Python-Annotator-for-VideoS/master/Examples/example.PNG)

### Installation
 * Dependencies

   * python-pyqt5
   * python-pyqt5.Qtmultimedia
   * python-pyqt5.QtMultimediaWidgets
   * python-pyqt5.QtCore
   * python-pyqt5.QtGui
   * os
   * csv
   * sys
   * python-numpy

### Usage
   * Running the annotator
 ```
     python pavs.py
```

### Shortcuts
- Load video: L
- Previous frame: Left Arrow
- Next frame: Right Arrow
- Add Start Time: [
- Add End Time: ]
- Frame after next 10 frames: Shift + Left Arrow
- Frame before prev 10 frames: Shift + Right Arrow
- Clear entire table: C
