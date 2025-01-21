from resources import braille
from resources import stl
import trimesh

if __name__ == '__main__':
    phrase = "Hello, World!"
    braille_text = braille.encode(phrase)
    braille_length = len(braille_text)

    surface = stl.createSurface(5, 5, 0.18)
    
    output_scene = trimesh.Scene()
    for i in range(braille_length):
        character = braille_text[i]
        if character != " ":
            character_3d = braille.characterTo3d(character, 0.1, 1, 3)
            print(character_3d)
            output_scene.add_geometry(character_3d.apply_translation([i * 2, 0, 0]))

    output_scene.export("output.stl")