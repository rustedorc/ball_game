import pathlib
from pygame.mixer import Sound


def load_music(mixer) -> dict[str, Sound]:
    music = {}
    music_directory = pathlib.Path(__file__).parent.parent.parent / 'assets' / 'music'
    for path in music_directory.iterdir():
        music[path.stem] = Sound(path)
    print(music)
    return music