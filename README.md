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

by the versions that have been updated within this repository. 

Delete the files
   - /ocelot/adaptors/genesis.pyc     
   - /ocelot/utils/xfel_utils.pyc     
   - /ocelot/gui/genesis_plot.pyc

The script requires the input_file.in to be located within the same folder where the script is being run. The betamatch executable is copied from /scratch2b/qfi29231/betamatch_dir
  
  23-03-17
Description of the input_file.in
 ###### Output path #################################
exp_dir	      '/scratch2b/qfi29231/results_dev_single/'   (Output path where the results and output files are going to be stored)
###### Type of Launcher (Genesis v2 or v3) #########
genesis_launcher	'genesis2.0'                          (GENESIS launcher, could be genesis2.0 or genesis3.2.1)
###### Statistical runs ############################
stat_run	   1                                          (Number of statistical runs, larger than 0) 
###### GENESIS input file ##########################
in_gen 0                                                  (Flag to set if there is a GENESIS input file available to read from, 1, or not, 0).
gen_filename	gen_input.in                              (Name of the GENESIS input file. Even if there is one, noise realisations and scans are controlled via the input_file.in)  
###### Time dependent flags       ##################      (Time dependent flags (controls steady state or time dependent simulations)  
shotnoise   1
itdp	    1
prad0	    1e-12
###### Beam Energy and wavelength ##################      (Beam Energy and wavelength values) (if there is an available GENESIS input file, these values are overwritten)
xlamds	1.35076e-8
gamma0	1.46871e3
###### Undulator design and lattice ################      (Undulator parameters: They are used to fill in the attributes of the Undulator Lattice object. The lattice file is generated automatically from the object in run time)
xlamd	0.036
nsec	23
nwig	58
aw0	0.7852
fl	2
dl	2
drl	78
quadf	16
quadd	-16
iwityp	1
xkx	0.5
xky	0.5
##### Beam parameters #############################         (Beam parameters: hard coded for the moment. Eventually, the idea is to read these parameters from a dist file or a beam file and generate a beam file in run time)
i_profile  1                                                 (i_profile: Flag to determine if the beam is gaussian (1) or flat-top(0)) If it is gaussian, OCELOT calculates the time window as 8 sigma. 
curlen	2.0944e-5
curpeak	430
delgam	1.357
rxbeam	6.491585e-5
rybeam	2.95641e-5
emitx	6.5e-7
emity	6.5e-7
alphax	-2.464459e-2
alphay	-8.971086e-3
nslice	927
ntail	-463
gauss_fl	1
##### Simulation parameters #######################        (Simulation parameters: If there is an available GENESIS input file, these are overwritten)
zsep	10
npart	8192
ncar	151
delz	1
dmpfld	1
fbess0	0
dgrid	0
rmax0	9
##### Scan parameters (flag 0 if there is no scan) #        (Scan parameters)
i_scan	   0                                                (Flag for scan. If it is 0, no scan is considered. If it is 1, then the scan is performed)   
parameter  'aw0'                                             (Name of the parameter to do scan. If it is a quad scan (quadf, quadd, fl,dl,drl, nsec, nwig, aw0), the scan is done in Steady State and rematching is done with betamatch)
init	   12                                                (Initial value of the scan parameter)
end	   25                                                    (End value of the scan parameter_)
n_scan	   10                                                (Number of scans)

 
   HMCC
   
