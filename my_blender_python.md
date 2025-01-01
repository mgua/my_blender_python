# Writing my python code for my blender setup

by Marco Guardigli, mgua@tomware.it
jan 01 2025

This document guides in setting up a python environment that blends-in with 
the blender python, keeping it separated and independent.
This allows you to write python code that will run inside your blender, but
taking advantage of additional packages you may need, like opencv, or any 
other python package.
We will be referencing the blender installation on windows.
at the time of the writing, blender version is 4.3


## A typical blender install on Windows

When you install blender on windows, blender typically installs as a system wide application, requiring administrative rights.
Blender 4.3 on windows 11 installs by default to the following path:
```
C:\Program Files\Blender Foundation\Blender 4.3
```
within this path a number of subfolders are created. A specific subtree is 
dedicated to Blender's embedded python installation, which is in:
```
C:\Program Files\Blender Foundation\Blender 4.3\4.3\python
```
the main python executable python.exe is in 
```
C:\Program Files\Blender Foundation\Blender 4.3\4.3\python\bin\python.exe
```
you can run this file to see its version
```
c:
cd "C:\Program Files\Blender Foundation\Blender 4.3\4.3\python\bin\"

.\python.exe -V
Python 3.11.9

.\python.exe -m pip list
[... shows package list ...]
```

(this will show the packages installed within the python embedded in blender)

The python version number is important. We will need to create a separate 
python installation and a specific python environment with the same 
or close-enough version

For our case, a close enogh version should be python 3.11


## Installing a separate python version matching the blender python

Install the correct python interpreter version from python.org.
https://www.python.org/downloads/windows/ 
On windows, be sure to install the py launcher, so that we can create 
version-specific python environments.
Once installation is done, you should be able to execute 
(from a powershell prompt)

```
py --list
```

and see the available python versions, among which the 3.11


## Creating a dedicated python environment for my blender

Since I installed Blender 4.3 which uses python 3.11.9 I will create a 
dedicated python 3.11 virtual environment.
open a powershell prompt and go to your home folder, then create a code 
folder and a venv folder 

```
cd ~
mkdir my_blender_4.3
py -3.11 -m venv venv_my_blender_4.3
```

Then you can activate the newly created environment running the activate 
command for your powershell:

```
.\venv_my_blender_4.3\Scripts\Activate.ps1
```

The prompt should change to notify you are in that specific virtual environment

the path to your virtual environment will be something similar to:

```
C:\Users\mgua\venv_my_blender_4.3
```

our naming convention is that the environment folder name is like the 
code folder name prefixed with "venv_"



## my code folder

In the my_blender_4.3 folder we will put and test our python code
this code will run within the dedicated environment we just created.

We create a "packages" subfolders. 

```
cd ~
cd my_blender_4.3
mkdir packages
```

the python code we will write within blender will extend the path 
to include this packages subfolders

```
import sys
sys.path.append(r"c:\Users\mgua\my_blender_4.3\packages")
```


The packages folder is where will will be able to selectively install 
(from within our environment) just the packages that will be needed from
within Blender. We will use a pip install with target option

```
python -m pip install package_name --target=C:\Users\mgua\my_blender_4.3\packages
```

to test the packages in our environment we will install them twice: 
one without --target option, to test within our venv, and one with --target
so to make the packages available to blender (blender will be able to "see" 
our packages subfolder via the sys.path.append statement)


## identifying what to add to the packages folder

Examine your code imports. 
From within blender, in the interactive console, try to import 
the modules and see if you get any error "no module named..." 

The modules for which the import fails are the ones you need to add


## example 01: qrcode generation within blender

Qrcode can be easily generated with python using qrcode package
qrcode package depends on pil

typical package installation is as follows: The [pil] ensures that 
pil dependencies are automatically managed

```
python -m pip install qrcode[pil]
```

the execution of this statement, within our active environment, will perform
the package installation inside the venv_ folder.

once our code has been tested, and we have the full list of packages that will
be needed withing blender, we execute again the pip. adding the target option

```
python -m pip install qrcode[pil] --target=C:\Users\mgua\my_blender_4.3\packages
```

Here is the code 

```python
#! python
# this code generates qrcodes 
# as a test it saves a simple file
#
# install requirements
# python -m pip install qrcode[pip] --target=c:\Users\mgua\my_blender_4.3\packages
#
# for blender integration we rely on a sys.path.append


import sys
sys.path.append(r"c:\Users\mgua\my_blender_4.3\packages")

import qrcode
from io import BytesIO

def generate_qr_bytes(data):
    # Create QR code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    # Add data to the QR code
    qr.add_data(data)
    qr.make(fit=True)

    # Create an image from the QR code
    qr_image = qr.make_image(fill_color="black", back_color="white")
    
    # Create a bytes buffer
    buffer = BytesIO()
    
    # Save the image to the buffer in PNG format
    qr_image.save(buffer, format='PNG')
    
    # Get the bytes from the buffer
    image_bytes = buffer.getvalue()
    
    return image_bytes

# Example usage
if __name__ == "__main__":
    data_to_encode = "https://marco.guardigli.it"
    qr_bytes = generate_qr_bytes(data_to_encode)
    
    # Example: To verify the bytes were created
    print(f"QR code generated! Byte array length: {len(qr_bytes)} bytes")
    
    # Example: If you need to save the bytes to a file later
    output_file=r"C:\Users\mgua\my_blender_4.3\qrcode_blender.png"  # r is to avoid backslash escaping role
    with open(output_file, 'wb') as f:
        f.write(qr_bytes)

```


## Example 02: audio processing from microphone

The test code in audio_blender.py currently crashes blender. 
to be debugged...


