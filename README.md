# Bedload Simulation

This repository was created for the study of the influence of shape in turbulent bedload transport.
This document aims to give the informations necessary to use this framework.

## Getting started

### Prerequisites

Be sure to use a linux operating system. At least Ubuntu and Debian distributions should work. 
You will need a slightly modified version of YADE DEM to use the code and run the examples.
To get it clone or download the project at [https://gitlab.com/remi.monthiller/trunk](https://gitlab.com/remi.monthiller/trunk).
Move to the branch ***hydro_force_engine*** and compile the code.

In order to compile the code and install all prerequisites, you may want to see the instructions 
given on the Yade dem website before [https://yade$-dem.org/doc/](https://yade-dem.org/doc/).
Be sure to install all prerequisites mentionned on the website or the code won't compile.
Take a look to the ***Installation*** section and the ***Compilation*** subsection. The process of compilation is the same.

When all the prerequisites are installed, you could run the following commands for example, to launch the compilation :

```
git https://gitlab.com/remi.monthiller/trunk.git
cd trunk
git checkout hydro_force_engine
cd ..
mkdir build install
cd build 
cmake -DCMAKE_INSTALL_PREFIX=../install ../trunk
make
make install
```

The executable should be in the folder ***../install/bin***.
For convenience, you may want to rename the executable to ***yade*** and add the install folder to your path :

```
cd ../install/bin
mv yade-$$$.git-$$$ yade 
PATH=$PATH:$PWD
```

### Get the framework

Clone or download the project and unzip it. 
Then move to its location with a terminal to get started. For example :

```
git clone https://github.com/LeDernier/bedload_simulation.git
cd bedload_simulation
```

### Running first tests

