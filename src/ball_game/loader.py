import pathlib
from pygame.surface import Surface
from pygame.mixer import Sound
from pygame.image import load
from pygame.font import Font

class Loader:
    def __init__(self) -> None:
        self.assets_path = pathlib.Path(__file__).parent.parent.parent / 'assets'
        self.music = {}
        self.images = {}
        self.fonts = {}

    def load_music(self) -> dict[str, Sound]:
        music_directory = self.assets_path / 'music'
        for path in music_directory.iterdir():
            self.music[path.stem] = Sound(path)
        return self.music

    def load_images(self) -> dict[str, Surface]:
        image_directory = self.assets_path / 'images'
        for path in image_directory.iterdir():
            self.images[path.stem] = load(path)
        return self.images
    
    def load_fonts(self) -> dict[str, Font]:
        font_directory = self.assets_path / 'fonts'
        for path in font_directory.iterdir():
            self.fonts[path.stem] = Font(path)