# at3dcv

This is a project for "Advanced Topics in 3D Computer Vision" Praktikum course, offered by TUM in Winter Semester 2019. In this project, we have implemented a pipline to do a 3D recunstrion of a scene, using a depth camera, segment the objects and then use the data to do augmentations.

## Getting Started

These instructions will help you running the code on your local machine.

### Prerequisites

* One of the libraries we use is [Open3D](http://open3d.org), which does not support Python 3.7. We recommend running the code using a Python Enviroment.
* For Mac users, the SDK of the [Intel® RealSense](https://github.com/IntelRealSense/librealsense/tree/master/wrappers/python) (the RGBD camera which we use) is not available, so you have to build the lib files from source and add them to the 'pyrealsenseformac' folder.



### Running

To run the whole pipline with UI, go to the root directory and run main.py.
```
python main.py
```
