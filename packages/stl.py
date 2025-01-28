from io import BytesIO
import vtk



def createScene():
    return vtk.vtkAppendPolyData()



def makeTranslation(object, x, y, z, rotate_x=0.0, rotate_y=0.0, rotate_z=0.0):
    transform = vtk.vtkTransform()
    transform.Translate(x, y, z)
    transform.RotateX(rotate_x)
    transform.RotateY(rotate_y)
    transform.RotateZ(rotate_z)
    transform_filter = vtk.vtkTransformPolyDataFilter()
    transform_filter.SetTransform(transform)
    transform_filter.SetInputData(object)
    transform_filter.Update()
    return transform_filter.GetOutput()


def createSphere(radius=1, resolution=20):
    sphere = vtk.vtkSphereSource()
    sphere.SetRadius(radius)
    sphere.SetThetaResolution(resolution)
    sphere.SetPhiResolution(resolution)
    sphere.SetCenter(0, 0, 0)
    sphere.Update()
    return sphere.GetOutput()



def createPlate(width=1, height=1, depth=1):
    plate = vtk.vtkCubeSource()
    plate.SetXLength(width)
    plate.SetYLength(height)
    plate.SetZLength(depth)
    plate.SetCenter(0, 0, 0)
    plate.Update()
    return plate.GetOutput()



def createCylinder(radius=1, width=1, resolution=20):
    cylinder = vtk.vtkCylinderSource()
    cylinder.SetRadius(radius)
    cylinder.SetHeight(width)
    cylinder.SetResolution(resolution)
    cylinder.SetCenter(0, 0, 0)
    cylinder.Update()
    return makeTranslation(cylinder.GetOutput(), (-width / 2), 0, 0, rotate_x=90)



def createBraillePoints(
        points_code,
        radius = 1,
        spacing = 2.7,
        resolution = 20,
    ):
    character = createScene()

    if points_code[0] == "1":
        character.AddInputData(makeTranslation(createSphere(radius, resolution), 0, (2 * spacing), 0))
    if points_code[1] == "1":
        character.AddInputData(makeTranslation(createSphere(radius, resolution), 0, spacing, 0))
    if points_code[2] == "1":
        character.AddInputData(makeTranslation(createSphere(radius, resolution), 0, 0, 0))
    if points_code[3] == "1":
        character.AddInputData(makeTranslation(createSphere(radius, resolution), spacing, (2 * spacing), 0))
    if points_code[4] == "1":
        character.AddInputData(makeTranslation(createSphere(radius, resolution), spacing, spacing, 0))
    if points_code[5] == "1":
        character.AddInputData(makeTranslation(createSphere(radius, resolution), spacing, 0, 0))

    character.Update()
    return character.GetOutput()



def sceneToSTL(scene):
    writer = vtk.vtkSTLWriter()
    writer.SetInputData(scene)
    writer.SetFileTypeToBinary()
    writer.SetFileName("output.stl")
    writer.Write()
    
    with open("output.stl", 'rb') as f:
        stl_data = f.read()
    
    output = BytesIO()
    output.write(stl_data)
    output.seek(0)
    return output
