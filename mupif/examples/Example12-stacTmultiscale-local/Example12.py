import sys
sys.path.extend(['../../..', '../Example10-stacTM-local'])
from mupif import *
import demoapp
import logging
log = logging.getLogger()
import mupif.Physics.PhysicalQuantities as PQ

#Read geometry and boundary condition for the microscale
thermalMicro = demoapp.thermal('thermalMicro.in','')
log.info(thermalMicro.getApplicationSignature())
#Solve the microscale problem
tstep = TimeStep.TimeStep(0., 1., 1., 's')
thermalMicro.solveStep(tstep)
#Get effective conductivity from the microscale
effConductivity = thermalMicro.getProperty(PropertyID.PID_effective_conductivity,tstep.getTargetTime())
log.info('Computed effective conductivity from microscale: %f' % effConductivity.value)

#Dump microscale results to VTK files
thermalMicroField = thermalMicro.getField(FieldID.FID_Material_number, tstep.getTargetTime())
thermalMicroField.field2VTKData().tofile('thermalMicroMaterial')
thermalMicroField = thermalMicro.getField(FieldID.FID_Temperature, tstep.getTargetTime())
thermalMicroField.field2VTKData().tofile('thermalMicroT')

#Read geometry and boundary condition for the macroscale
thermalMacro = demoapp.thermal('thermalMacro.in','')
#Assign effective conductivity for the whole macroscale domain
thermalMacro.setProperty(effConductivity)
thermalMacro.solveStep(None)
thermalMacroField = thermalMacro.getField(FieldID.FID_Temperature, tstep.getTargetTime())

#Dump macroscale results to VTK files
thermalMacroField.field2VTKData().tofile('thermalMacroT')

log.info("Test OK")
