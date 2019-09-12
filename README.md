# TMT Astrometry
TMT astrometry tool in python 
- Install dash libraries,
- pip install dash==0.42.0  # The core dash backend
- https://plot.ly/products/dash/
- Run IRIS_Astrometry file
- python ./IRIS_Astrometry.py
- See output in browser http://127.0.0.1:8050/
- While using Mac OS setup your system for python 3 and use commands, pip3 install dash==0.42.0,  python3 ./IRIS_Astrometry.py
# Tasks remaining
- Need a better looking UI
- Need units every where
- avoid div by zero
- Put limits on inputs
- some field types need to be int (number of stars) fix that
- rearrange code to make it more readable?

# UI options discuss with Jessica
- show error for each category in UI? FP, OPT-mech etc
- show default (constant values) in UI?
- store results in a file?
- Automate to read multiple cases from a file and store results in a file?
- Things to plot?
- Integrate it with a catalog or observation field simulation. This will automatically generate input for the calculator.

# Issues
- Excel never uses formula DR1 from the .pdf. We need to work on its use case?
- possible error in excel for absolute astrometry PS-2 formulae?
- How and when is Nmodes used?
- Case with Nref >6





