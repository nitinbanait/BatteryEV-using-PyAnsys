'''

note:
    when running inside mechanical (remote, ansys-mechanical CLI, and paste into script editor), the full path is needed.
    when running with embedding, the full path is not needed.

    when running the remote interface, the print statements are ignored. Instead, the values can be accessed by running
    code like this:

    import ansys.mechanical.core as mech
    mechanical = mech.launch_mechanical(batch=True, loglevel="DEBUG")
    mechanical.run_python_script_from_file("path\\to\\script.py")
    mechanical.run_python_script("buck_deformation_1.LoadMultiplier")
    mechanical.exit()
'''


# embedding import block. If running in IronPython, this will do nothing.
# try:
#     import ansys.mechanical.core as mech
#     app = mech.App(version=241)
#     globals().update(mech.global_variables(app, True))
# except ImportError as e:
#     pass


import os

geometry_file = os.path.abspath(os.path.join(os.getcwd(), "Files", "Eng157.x_t"))
if not os.path.isfile(geometry_file):
    geometry_file = r"D:\PreSales Q3 2024\Pyansys\LFP Pack\lfp.stp"

geometry_import = Model.GeometryImportGroup.AddGeometryImport()
geometry_import.Import(geometry_file)

Model.Geometry.ElementControl = ElementControl.Manual

struc = Model.AddStaticStructuralAnalysis()
ExtAPI.Application.ActiveUnitSystem = MechanicalUnitSystem.StandardNMMdat

ns_support = Model.AddNamedSelection()
ns_support.ScopingMethod = GeometryDefineByType.Worksheet
ns_support.Name = "NS_SUPPORT"
ns_support.GenerationCriteria.Add()
criteria = ns_support.GenerationCriteria[0]
criteria.EntityType = SelectionType.GeoFace
criteria.Criterion = SelectionCriterionType.LocationZ
criteria.Operator = SelectionOperatorType.Equal
criteria.Value = Quantity('0 [mm]')
ns_support.Generate()

fixed_support = struc.AddFixedSupport()
fixed_support.Location = ns_support

ns_map = Model.AddNamedSelection()
ns_map.ScopingMethod = GeometryDefineByType.Worksheet
ns_map.Name = "MAP1"
ns_map.GenerationCriteria.Add()
criteria = ns_map.GenerationCriteria[0]
criteria.EntityType = SelectionType.GeoFace
criteria.Criterion = SelectionCriterionType.LocationX
criteria.Operator = SelectionOperatorType.Equal
criteria.Value = Quantity('173 [mm]')
ns_map.Generate()

ns_map = Model.AddNamedSelection()
ns_map.ScopingMethod = GeometryDefineByType.Worksheet
ns_map.Name = "MAP2"
ns_map.GenerationCriteria.Add()
criteria = ns_map.GenerationCriteria[0]
criteria.EntityType = SelectionType.GeoFace
criteria.Criterion = SelectionCriterionType.LocationX
criteria.Operator = SelectionOperatorType.Equal
criteria.Value = Quantity('2.7756e-014 [mm]')
ns_map.Generate()

ns_map = Model.AddNamedSelection()
ns_map.ScopingMethod = GeometryDefineByType.Worksheet
ns_map.Name = "MAP3"
ns_map.GenerationCriteria.Add()
criteria = ns_map.GenerationCriteria[0]
criteria.EntityType = SelectionType.GeoFace
criteria.Criterion = SelectionCriterionType.Size
criteria.Operator = SelectionOperatorType.Largest
ns_map.Generate()

#force = struc.AddForce()
#force.Location = ns_force
#force.DefineBy = LoadDefineBy.Components
#force.ZComponent.Output.SetDiscreteValue(0, Quantity("-5 [N]"))


msh = Model.Mesh
msh.ElementOrder = ElementOrder.Quadratic
msh.ElementSize = Quantity(str(5)+"[mm]")

Model.Solve(True)

