#!/usr/bin/python
'''Script to run the genesis simulation in OCELOT. It calls the different
elements that are required to make instances of objects and run genesis.
 It requires to be run in the directory where the input file is (it looks for a .in file
with the specifications of lattice design, simulation specs and hard coded values of 
Beam parameters.  It is necessary to append the path where OCELOT is being installed.

HMCC: 16-02-17 Initial prototype. Including Scan over parameters (from input file)
                and noise realisations. Things still to be implemented: Postprocessing,
                matching of the beam (via betamatch or using the other methods within the 
                OCELOT framework), tapering, wakefields.


'''
#################################################
### import of all modules that are required.
from __future__ import print_function
from copy import deepcopy,copy
import sys, os

from ocelot import *
from ocelot.utils.xfel_utils import *
from ocelot.gui.accelerator import *
from ocelot.gui.genesis_plot import *
from ocelot.optics.elements import Filter_freq
import ocelot.cpbd.elements
import numpy as np
import matplotlib.pyplot as plt

### Path where OCELOT is being installed
sys.path.append('/home/qfi29231/.local/lib/python2.7/site-packages/Ocelot-16.8rc0-py2.7.egg/ocelot/')
####  Methods #################################

def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir,name))]
#def read_input_file(filename):
#    import ocelot.adaptors.genesis####
#    inp = GenesisInput()
#    other_param = ['shotnoise', 'xlamd','filetype', 'fbess0','itdp']
#    with open(filename,'rt') as f:
#        for line in f:
#            line=line.rstrip('\n').replace(' ','')            
#            splitLine = line.split('=')
#            if(splitLine[-1].find('D+')) or (splitLine[-1].find('D-')):
#                splitLine[-1].replace('D','E')
#            if (splitLine[0] in inp.__dict__.keys()) or (splitLine[0] in other_param):
#                setattr(inp,splitLine[0],splitLine[-1])
#    f.close()
#    return inp

def read_input_file(f_path):
    if (f_path.endswith('/') is not 'True'):
        f_path=f_path+'/'
    else:
        f_path=f_path
    A_dir = [files for files in os.listdir(f_path) if files.endswith('.in')]
    A_arg_int = ['stat_run',',ipseed','nsec','nwig','zsep','fl','dl','drl',
                 'npart','nslice','shotnoise','delz','dmpfld',
                 'itdp', 'delz','ncar','iwityp','nslice','fbess0','gauss_fl',
                 'rmax0','i_scan','n_scan']
    A_arg_float = ['xlamd','xlamds','gamma0','aw0','awd','quadf','quadd',
                   'curlen','curpeak','delgam','rxbeam','rybeam',
                   'emitx','emity','alphax','alphay','prad0','dgrid',
                   'xkx','xky','init','end']
    A_content={}
    with open(f_path+str(A_dir[0]),'r') as f:
        for indx,line in enumerate(f.readlines()):
            splitLine = (line.replace('\n','')).split('\t')
            if splitLine[0].startswith('#'):
                continue
            elif splitLine[0] in A_arg_int:
                splitLine[-1]=int(splitLine[-1])
            elif splitLine[0] in A_arg_float:
                splitLine[-1] = float(splitLine[-1])
            elif splitLine[0].startswith('exp_dir'):
                splitLine[-1]=splitLine[-1][splitLine[-1].find('/')-1:-1]
            A_content[splitLine[0]]=splitLine[-1]
            if splitLine[0].startswith('parameter'):
                A_content['parameter']=str(splitLine[-1][11:].replace(" ",''))
            elif splitLine[0].startswith('genesis_launcher'):
                A_content['genesis_launcher']= str(splitLine[-1])
    f.close()
    return A_content
    
def undulator_design(A_contents):
    from ocelot.cpbd.elements import Drift, Quadrupole, Undulator
    from ocelot.cpbd.magnetic_lattice import MagneticLattice
    from ocelot.common import globals
    from ocelot.common.globals import m_e_GeV, speed_of_light, h_eV_s
    from ocelot.rad.undulator_params import Ephoton2K
    from ocelot.rad.undulator_params import UndulatorParameters
    import numpy as np

    ## Taking it from the Notebook
    xlamd = A_contents['xlamd']
    nwig=A_contents['nwig']
    E_beam=A_contents['gamma0']*m_e_GeV
    E_photon=h_eV_s*speed_of_light/A_contents['xlamds']
    p_beam = np.sqrt(E_beam**2-m_e_GeV**2)
    fl=A_contents['fl']
    dl=A_contents['dl']
    drl=A_contents['drl']
    quadf=A_contents['quadf']
    quadd=A_contents['quadd']
    nsec=A_contents['nsec']
    aw0 = A_contents['aw0']
    drl = int((fl+drl-nwig)/2)-1
   
   # Instance of the Undulator object
    und= Undulator(lperiod=xlamd, nperiods=nwig, Kx=aw0*sqrt(0.5))
   
   # Calculation of the Undulator parameter from the Photon and Beam Energies)
    und.Kx=Ephoton2K(E_photon,und.lperiod,E_beam)
   
   # Drift sections (if they are the same)
    d_rift = Drift(l=drl*und.lperiod)
    d_rift2 = Drift(l=drl*und.lperiod)
   
   # Definition of Quads
 
    qf= Quadrupole(l=fl*und.lperiod,k1=0.3*quadf/p_beam)
    qd = Quadrupole(l=dl*und.lperiod,k1=0.3*quadd/p_beam)
    qdh=deepcopy(qd)
    qdh.l/=2
   
   # Creating the cell
 
    extra_fodo = (und,d_rift,qdh)
    cell_ps = (und, d_rift,qf,d_rift2, und, d_rift, qd, d_rift2)
    l_fodo = MagneticLattice(cell_ps).totalLen/2 ##Length of fodo cell
    sase3= MagneticLattice((und,d_rift, qd,d_rift2)+int(nsec/2)*cell_ps) # Lattice with nsec modules
    up = UndulatorParameters(und,E_beam) # Instance of the Class UndulatorParameters
    print('++++ Undulator Parameters +++')
    up.printParameters()
    return {'Undulator Parameters':up,'Magnetic Lattice':sase3}
    
def BeamDefinition(A_contents):
    from ocelot.common.globals import m_e_GeV, speed_of_light
    from ocelot.cpbd.beam import Beam   
    beamf = Beam()
    A_dict= {'E':A_contents['gamma0']*m_e_GeV,'sigma_E':A_contents['delgam']*m_e_GeV,'beta_x':A_contents['gamma0']*(A_contents['rxbeam']**2)/(A_contents['emitx']), 
        'beta_y':A_contents['gamma0']*(A_contents['rybeam']**2)/A_contents['emity'], 'alpha_x':A_contents['alphax'],'alpha_y':A_contents['alphay'],
        'emit_x':A_contents['emitx']/A_contents['gamma0'],'emit_y' : A_contents['emity']/A_contents['gamma0'],'emit_xn':A_contents['emitx'],'emit_yn':A_contents['emity'],
         'x' :  0.000000e+00,
        'y' : 0.000000e+00,'px':0,'py':0,'I':A_contents['curpeak'],'tpulse':1e15*(A_contents['curlen']/speed_of_light)}
    for item in A_dict:
        setattr(beamf, item,A_dict[item])
    return beamf

##########  MAIN ###############################################      
def main():
    import os,sys
    import numpy as np
    from ocelot.common import globals
    from ocelot.adaptors.genesis import generate_input,generate_lattice
    from ocelot.utils.xfel_utils import get_genesis_launcher,run
    A_input = read_input_file(os.getcwd()+'/')
    A_beam = ['xlamds','gamma0','curlen','curpeak','delgam','rxbeam','rybeam','emitx','emity','alphax','alphay','nslice']
    A_simul = ['zsep','npart','ncar','delz','dmpfld','fbess0','dgrid','rmax0']
    A_td = ['itdp','prad0','shotnoise']
    
    #set simulation parameters by calling the read_input_file function
    exp_dir=A_input['exp_dir'][1:-1]+'/'
    print('++++ Output Path {} ++++++'.format(exp_dir))

    # Setting the number of noise realisations
    run_number=A_input['stat_run']
    run_ids = xrange(0,run_number)
    print('++++ Number of noise realisations {} ++++++'.format(run_number))

    # Setting the case when there is a scan over parameters
    if A_input['i_scan'] ==0:
        s_scan = range(1)
        print('++++++++ No scan ++++++++')
    else:
        s_scan = np.linspace(A_input['init'],A_input['end'],A_input['n_scan'])

    # setting the undulator design( Magnetic Lattice)
    A_undulator = undulator_design(A_input)
    
    # fill in the beam object
    A_beam = BeamDefinition(A_input) 
    
    # Generate input object
    inp = generate_input(A_undulator['Undulator Parameters'],A_beam,itdp=True)

    # Overwrite the simulation attributes of the input object with the ones defined in the input file
    for n_simul in A_simul:
        setattr(inp,str(n_simul),A_input.get(str(n_simul)))

    for n_par in s_scan:
        if A_input['i_scan']==1:
            if (A_input['parameter']) or (A_input['parameter'] in A_und) or (A_input['parameter'] in A_simul):
                setattr(inp,A_input['parameter'][1:-1],n_par)
            print(' ++++++++++ Scan {} of the parameter {}'.format(n_par, A_input['parameter']))
        for run_id in run_ids:
        
   #prepare input, file and specify parameters, creating instance of the input object
            try:
                os.makedirs(exp_dir+'scan'+str(n_par)+'/run_'+str(run_id))
            except OSError as exc:
                if (exc.errno == errno.EEXIST) and os.path.isdir(exp_dir+'scan'+str(n_par)+'/run_'+str(run_id)):
                    pass
                else: 
                    raise

            inp.runid = run_id
            inp.run_dir = exp_dir+'scan'+str(n_par)+'/run_'+str(inp.runid)
            inp.ipseed = 17111*(int(inp.runid)+1)
           
            inp.lattice_str = generate_lattice(A_undulator['Magnetic Lattice'],unit = A_undulator['Undulator Parameters'].lw,energy=A_beam.E)
            
            launcher = get_genesis_launcher(A_input['genesis_launcher'][1:-1])
            
            print('+++++ Starting simulation of noise realisation {}'.format(run_id))
            g = run(inp,launcher)

################## END OF METHODS ############################################
if __name__=="__main__":
    print('++++++ Script to run GENESIS ++++++++')
    main()
    print('+++++++++ End of simulation +++++++++')
