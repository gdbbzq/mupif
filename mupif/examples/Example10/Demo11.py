from __future__ import print_function
import sys
sys.path.append('../../..')
import demoapp
import meshgen
from mupif import FieldID
from mupif import Field
from mupif import ValueType
from mupif import TimeStep
from mupif import PropertyID
from mupif import Mesh
from mupif import Vertex
from mupif import Cell


if True:
    app = demoapp.thermal('inputT11.in','.')
    print(app.getApplicationSignature())

    sol = app.solveStep(TimeStep.TimeStep(0,1)) 
    f = app.getField(FieldID.FID_Temperature, 0.0)
    f.field2VTKData().tofile('thermal11')

if True:
    app2 = demoapp.mechanical('inputM11.in', '.')
    print(app2.getApplicationSignature())

    app2.setField(f)
    sol = app2.solveStep(TimeStep.TimeStep(0,1)) 
    f = app2.getField(FieldID.FID_Displacement, 0.0)
    f.field2VTKData().tofile('mechanical11')

