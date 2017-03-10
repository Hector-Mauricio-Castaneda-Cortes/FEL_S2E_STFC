# FEL_S2E_STFC
Modified routines in order to implement a S2E (STFC)
# 16/02/17

This repository includes a modified version of OCELOT, allowing the simulations in GENESIS to be run in our local servers, 
and a ascript that allows us to run GENESIS v2 and v3  (noise realisations, scans).

 The script needs to be run in the path where the input file is located.
 
 The input file contains the main parameters that are usually changed by us before a GENESIS simulation, plus 
 some additional features which are required by the script:
 
  - genesis_launcher: which could be 'genesis2.0' or 'genesis3.2.1'
  - exp_dir: root directory where the results are going to be exported.
  
  At the moment, the lattice design needs to be hardcoded (by setting the undulator parameters that define the lattice
  file in the input file). Also, the beam parameters need to be hardcoded as well (the idea will be to import a beam/dist file).
  
  Features to be added:
   - Possibility to read from existent input file (suggestion by Dave).
   - Matching via BetaMatch (suggestion by Neil).
   - Post-processing (in progress).
   - Wakefields (using GenWake or the functions already implemented by the OCELOT developing team).
   
   HMCC
   
   # 10/03/17
   
   Several features have been added to the Script: 
    - Single runs
    - Statistical runs (reading the input_file.in)
    - Possibility to do quad scans in steady state (scan over quadd, quadf, fl, drl) and using betamatch for the rematching.
    - Support for steady state runs
     - Reading from an external input file (still in progress. The function to read  the file has been implemented and used for the rematching in betamatch. However, I haven't tried to use an existent GENESIS input file for simulation purposes yet).
     
     - Postprocessing:
         -- Use of the function gen_outplot_statistics (implemented within OCELOT and modified) for the plotting of statistical runs. So far, the generated plots show the slice properties at the end of the undulator (power curve,bunching parameter,  phase of the on-axis electric field,on axis spectral density,  as a function of s) and peak power and pulse energy curves as a function of z. As outlook, average power over s, bunching parameter over s as a function of z need to be implemented in the script. It generates 6 png plots in a separate folder called 'results'.
         -- Implementation of the gen_outplot_single within the script (similar to the implementation in OCELOT): This function is called when the simulations are not set to be in statistical mode (number of noise realisations =1). The function supports the plotting of a single run (slice properties at the end of the undulator and mean and peak power and energy as a function of z), scan over quads (quadf). When I did the scan over wavelengths, the routine stops working (work in progress). it generates 9 png plots in a separate folder called 'results'
         
  Before the script is used, you need to replace the following scripts within ocelot:
     - /ocelot/adaptors/genesis.py
     - /ocelot/utils/xfel_utils.py
     - /ocelot/gui/genesis_plot.py
  by the versions that have been updated within this repository
   Delete the files
   - /ocelot/adaptors/genesis.pyc     - /ocelot/utils/xfel_utils.pyc     - /ocelot/gui/genesis_plot.pyc
   The script requires the input_file.in to be located within the same folder where the script is being run. The betamatch executable is copied from /scratch2b/qfi29231/
   
