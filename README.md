# TMT Astrometry
TMT astrometry tool in python 
- Install dash libraries,
- pip install dash==0.42.0  # The core dash backend
- https://plot.ly/products/dash/
# Run GUI
- Run IRIS_Astrometry file using following command
- >> python ./IRIS_Astrometry.py
- See output in browser http://127.0.0.1:8050/
- While using Mac OS setup your system for python 3 and use commands, pip3 install dash==0.42.0,  python3 ./IRIS_Astrometry.py
# Run files directly from python 
- Edit inputs in file inputs.py
- Start python and use the following commands
- >> from inputs import *
- >> from error_calculator import Error_calculator
- >> error_all = Error_calculator(global_inputs,field,sigma_sci,sigma_NGS,RefObjNCatErr,'Absolute Astrometry')
# Tasks remaining
- Add a input file upload, output download feature
# Issues
- Use data set for a wider range to got from magnitude/ exposure time to SNR.








