import pygame as pg

# File related tools
def get_image(directory: str, image_name: str) -> pg.Surface:
    path = f"{directory}/{image_name}"
    return pg.image.load(path)

def get_font(directory: str, font_name: str, size: int) -> pg.font.Font:
    path = f"{directory}/{font_name}"
    return pg.font.Font(path, size)
