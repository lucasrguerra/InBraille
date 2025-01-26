from io import BytesIO
import trimesh



def createScene():
    return trimesh.Scene()



def createSphere(radius=1, subdivisions=2):
    sphere = trimesh.creation.icosphere(radius=radius, subdivisions=subdivisions)
    return sphere



def createPlate(width=1, height=1, depth=1):
    surface = trimesh.creation.box(extents=(width, height, depth))
    return surface



def createCylinder(radius=1, height=1):
    cylinder = trimesh.creation.cylinder(radius=radius, height=height)
    return cylinder



def createBraillePoints(
        points_code,
        radius = 1,
        spacing = 3,
        subdivisions = 3,
    ):

    character = trimesh.Scene()

    if points_code[0] == "1":
        character.add_geometry(createSphere(radius, subdivisions).apply_translation([0, 0, 0]))
    if points_code[1] == "1":
        character.add_geometry(createSphere(radius, subdivisions).apply_translation([0, -spacing, 0]))
    if points_code[2] == "1":
        character.add_geometry(createSphere(radius, subdivisions).apply_translation([0, (2 * -spacing), 0]))
    if points_code[3] == "1":
        character.add_geometry(createSphere(radius, subdivisions).apply_translation([spacing, 0, 0]))
    if points_code[4] == "1":
        character.add_geometry(createSphere(radius, subdivisions).apply_translation([spacing, -spacing, 0]))
    if points_code[5] == "1":
        character.add_geometry(createSphere(radius, subdivisions).apply_translation([spacing, (2 * -spacing), 0]))

    return character



def sceneToSTL(scene):
    data = scene.export(None, "stl")
    file = BytesIO(data)
    file.seek(0)
    return file