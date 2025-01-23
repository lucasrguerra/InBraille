import trimesh

def createSphere(radius=1, subdivisions=3):
    sphere = trimesh.creation.icosphere(subdivisions=subdivisions, radius=radius)
    return sphere

def createSurface(width, height, depth):
    surface = trimesh.creation.box([width, height, depth])
    return surface

def createBrailleCharacter(
        point_1 = 0,
        point_2 = 0,
        point_3 = 0,
        point_4 = 0,
        point_5 = 0,
        point_6 = 0,
        spacing = 3,
        subdivisions = 3,
    ):

    chacter = trimesh.Scene()

    if point_1:
        chacter.add_geometry(createSphere(point_1, subdivisions).apply_translation([0, 0, 0]))
    if point_2:
        chacter.add_geometry(createSphere(point_2, subdivisions).apply_translation([spacing, 0, 0]))
    if point_3:
        chacter.add_geometry(createSphere(point_3, subdivisions).apply_translation([0, -spacing, 0]))
    if point_4:
        chacter.add_geometry(createSphere(point_4, subdivisions).apply_translation([spacing, -spacing, 0]))
    if point_5:
        chacter.add_geometry(createSphere(point_5, subdivisions).apply_translation([0, (2 * -spacing), 0]))
    if point_6:
        chacter.add_geometry(createSphere(point_6, subdivisions).apply_translation([spacing, (2 * -spacing), 0]))

    return chacter
