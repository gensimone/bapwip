import os, logging, customtkinter
from mpv import MPV
from bapwip import ui, icons


def main() -> None:
    PROJECT_CODE = os.path.dirname(os.path.abspath(__file__))
    ASSETS = os.path.join(PROJECT_CODE, "assets")
    COLORSCHEMES = os.path.join(ASSETS, "colorschemes")

    logging.basicConfig(level=logging.DEBUG)
    customtkinter.set_default_color_theme(os.path.join(COLORSCHEMES, "Sweetkind.json"))
    customtkinter.set_appearance_mode("light")

    root_ui = ui.Root()

    player_video_frame_id = root_ui.player_video_frame.winfo_id()
    player = MPV(wid=player_video_frame_id)
    player.play("/home/simone/music/Beck/Guero/Girl.mp3")

    # setting up icons
    pack = icons.build(icons.DEFAULT_ICONS_THEME_PATH)
    root_ui.set_icons(pack)
    root_ui.player_interface.set_player(player)

    root_ui.mainloop()


if __name__ == "__main__":
    main()
