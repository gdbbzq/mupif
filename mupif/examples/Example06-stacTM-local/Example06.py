import sys
sys.path.append('../../..')
import demoapp
from mupif import *
import mupif.Physics.PhysicalQuantities as PQ
import time
import logging

log = logging.getLogger()


class Example06(Workflow.Workflow):

    def __init__(self, targetTime=PQ.PhysicalQuantity('0 s'), metaData={}):
        """
        Initializes the workflow.
        """
        MD = {
            'Name': 'Thermo-mechanical stationary problem',
            'ID': 'Thermo-mechanical-1',
            'Description': 'stationary thermo-mechanical problem using finite elements on rectangular domain',
            'Model_refs_ID': ['NonStatThermo-1', 'Mechanical-1'],
            'Inputs': [],
            'Outputs': [
                {'Type': 'mupif.Field', 'Type_ID': 'mupif.FieldID.FID_Temperature', 'Name': 'Temperature field',
                 'Description': 'Temperature field on 2D domain', 'Units': 'degC'},
                {'Type': 'mupif.Field', 'Type_ID': 'mupif.FieldID.FID_Displacement', 'Name': 'Displacement field',
                 'Description': 'Displacement field on 2D domain', 'Units': 'm'}
            ]
        }
        super(Example06, self).__init__(targetTime=targetTime, metaData=MD)
        self.updateMetadata(metaData)

        self.thermalSolver = demoapp.thermal()
        self.mechanicalSolver = demoapp.mechanical()

    def initialize(self, file='', workdir='', metaData={}, validateMetaData=True, **kwargs):
        super(Example06, self).initialize(file, workdir, metaData, validateMetaData, **kwargs)

        passingMD = {
            'Execution': {
                'ID': self.getMetadata('Execution.ID'),
                'Use_case_ID': self.getMetadata('Execution.Use_case_ID'),
                'Task_ID': self.getMetadata('Execution.Task_ID')
            }
        }

        self.thermalSolver.initialize('inputT10.in', '.', metaData=passingMD)
        self.mechanicalSolver.initialize('inputM10.in', '.', metaData=passingMD)

    def solveStep(self, istep, stageID=0, runInBackground=False):
        self.thermalSolver.solveStep(istep, stageID, runInBackground)
        self.mechanicalSolver.setField(self.thermalSolver.getField(FieldID.FID_Temperature, istep.getTime()))
        self.mechanicalSolver.solveStep(istep, stageID, runInBackground)

    def getField(self, fieldID, time, objectID=0):
        if fieldID == FieldID.FID_Temperature:
            return self.thermalSolver.getField(fieldID, time, objectID)
        elif fieldID == FieldID.FID_Displacement:
            return self.mechanicalSolver.getField(fieldID, time, objectID)
        else:
            raise APIError.APIError('Unknown field ID')

    def getCriticalTimeStep(self):
        return PQ.PhysicalQuantity(1.0, 's')

    def terminate(self):
        self.thermalSolver.terminate()
        self.mechanicalSolver.terminate()
        super(Example06, self).terminate()

    def getApplicationSignature(self):
        return "Example06 workflow 1.0"

    def getAPIVersion(self):
        return "1.0"


md = {
    'Execution': {
        'ID': '1',
        'Use_case_ID': '1_1',
        'Task_ID': '1'
    }
}

demo = Example06(targetTime=PQ.PhysicalQuantity('1 s'))
demo.initialize(metaData=md)

tstep = TimeStep.TimeStep(
    PQ.PhysicalQuantity('1 s'),
    PQ.PhysicalQuantity('1 s'),
    PQ.PhysicalQuantity('10 s')
)

demo.solveStep(tstep)

tf = demo.getField(FieldID.FID_Temperature, tstep.getTime())
# tf.field2VTKData().tofile('thermal10')
# tf.field2Image2D(title='Thermal', fileName='thermal.png')
# time.sleep(1)
t_val = tf.evaluate((4.1, 0.9, 0.0))

mf = demo.getField(FieldID.FID_Displacement, tstep.getTime())
# mf.field2VTKData().tofile('mechanical10')
# mf.field2Image2D(fieldComponent=1, title='Mechanical', fileName='mechanical.png')
# time.sleep(1)
m_val = mf.evaluate((4.1, 0.9, 0.0))

demo.terminate()

if ((abs(t_val.getValue()[0]-5.1996464044328956) <= 1.e-8) and
        (abs(m_val.getValue()[1]-(-1.2033973431029044e-05)) <= 1.e-8)):
    log.info("Test OK")
else:
    log.error("Test FAILED")
    print(t_val.getValue()[0], m_val.getValue()[1])
    sys.exit(1)