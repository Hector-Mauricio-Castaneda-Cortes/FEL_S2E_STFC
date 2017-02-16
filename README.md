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
