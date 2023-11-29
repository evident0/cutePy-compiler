# cutePy-compiler
# Description

A python compiler for cutePy, a python-like programming language. This project compiles cutePy code to risc-V assembly with multiple intermediate steps to ensure it can be altered in the future to support more assemblers as well.
   
## Installing

Clone this project and name it accordingly:

``git clone https://github.com/BillyA15/OrderFiles/tree/alpha`` 

Create a virtual enviroment (Optional):

Windows: ``python -m venv .venv`` 

Linux: ``python3 -m venv .venv`` 

Activate virtual enviroment:

Windows CMD: ``path\to\venv\Scripts\activate.bat`` 

Windows PowerShell: ``path\to\venv\Scripts\Activate.ps1`` 

Linux: ``source /path/to/venv/bin/activate`` 

# Getting Started

1. Run the ``main.py`` using python 3.10 and above is recommended:
``python3 main.py path_to_test_program\test_program_name.cpy``
2. The result can be found inside final_code_output. Additionally the intermidiate code is saved in a file on the same path as the cutePy file 

