import os
from PIL import Image
from customtkinter import CTkImage


DEFAULT_ICONS_THEME_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), # src
    'assets/icons/default'
)


_REQUIRED_ICONS: dict[str, tuple[str, int, int]] = {
    "pause_button":      ("player_interface", 50, 50),
    "play_button":       ("player_interface", 50, 50),
    "left_skip_button":  ("player_interface", 35, 35),
    "right_skip_button": ("player_interface", 35, 35)
}


def build(icons_dir: str) -> dict[str, dict[str, CTkImage]]:
    ipack: dict[str, dict[str, CTkImage]] = {}

    dark_icons_path = os.path.join(icons_dir, "dark")
    light_icons_path = os.path.join(icons_dir, "light")

    for icon in _REQUIRED_ICONS:
        icon_data = _REQUIRED_ICONS[icon]
        owner = icon_data[0]
        width = icon_data[1]
        height = icon_data[2]

        icon_filename = f"{icon}.png"
        light_image = Image.open(os.path.join(light_icons_path, icon_filename))
        dark_image = Image.open(os.path.join(dark_icons_path, icon_filename))

        image = CTkImage(
            light_image=light_image,
            dark_image=dark_image,
            size=(width, height)
        )

        if owner not in ipack:
            ipack[owner] = {icon: image}
        else:
            ipack[owner][icon] = image

    return ipack
