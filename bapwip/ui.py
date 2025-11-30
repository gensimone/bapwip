from customtkinter import CTk
from customtkinter import CTkButton as Button
from customtkinter import CTkFrame as Frame
from customtkinter import CTkFrame as Frame
from customtkinter import CTkSlider as Slider
from mpv import MPV
from tkinter import Event
import logging


logger = logging.getLogger(__name__)


class Root(CTk):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.grid_rowconfigure(index=0, weight=1)
        self.grid_columnconfigure(index=0, weight=1)

        self.main_frame = Frame(master=self, bg_color="transparent", fg_color="transparent")
        self.main_frame.grid_columnconfigure(index=(0, 2), weight=1)
        self.main_frame.grid_rowconfigure(index=(0, 2), weight=1)
        self.main_frame.grid_columnconfigure(index=1, weight=1)
        self.main_frame.grid_rowconfigure(index=1, weight=1)
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        self.player_main_frame = Frame(master=self.main_frame, fg_color="transparent")
        self.player_main_frame.grid_rowconfigure(index=0, weight=1)
        self.player_main_frame.grid_rowconfigure(index=(1, 2, 3), weight=0)
        self.player_main_frame.grid_columnconfigure(index=0, weight=1)
        self.player_main_frame.grid(row=1, column=1, sticky="nsew")

        self.player_video_frame = PlayerVideoFrame(master=self.player_main_frame)
        self.player_video_frame.grid(row=0, column=0, sticky="nsew")

        self.top_glue = Frame(master=self.player_main_frame, height=10, fg_color="transparent")
        self.top_glue.grid(row=1, column=0)

        self.player_interface = PlayerInterface(master=self.player_main_frame)
        self.player_interface.grid(row=2, column=0, sticky="nsew")


    def set_icons(self, data: dict) -> None:
        self.player_interface.set_icons(data["player_interface"])


class PlayerVideoFrame(Frame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


class PlayerInterface(Frame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.configure(fg_color="transparent", bg_color="transparent")
        self.grid_rowconfigure(index=(0, 1, 2), weight=0)
        self.grid_columnconfigure(index=0, weight=1)

        self.button_interface = Frame(master=self, fg_color="transparent")
        self.button_interface.grid_rowconfigure(index=0, weight=1)
        self.button_interface.grid_columnconfigure(index=(0, 6), weight=1)
        self.button_interface.grid_columnconfigure(index=(1, 2, 3, 4, 5), weight=0)
        self.button_interface.grid(row=2, column=0, sticky="nsew")

        self.play_button = Button(
            master=self.button_interface,
            width=20,
            text="",
            hover=False,
            border_width=0,
            fg_color="transparent",
        )
        self.play_button.grid_rowconfigure(index=0, weight=1)
        self.play_button.grid_columnconfigure(index=0, weight=1)
        self.play_button.grid(row=0, column=3)
        self.play_button.configure(command=self._play_button_command)

        self.pause_button = Button(
            master=self.button_interface,
            width=20,
            text="",
            hover=False,
            border_width=0,
            fg_color="transparent",
        )
        self.pause_button.grid_rowconfigure(index=0, weight=1)
        self.pause_button.grid_columnconfigure(index=0, weight=1)
        self.pause_button.grid(row=0, column=3)
        self.pause_button.configure(command=self._pause_button_command)

        self.left_skip_button = Button(
            master=self.button_interface,
            width=20,
            text="",
            hover=False,
            border_width=0,
            fg_color="transparent"
        )
        self.left_skip_button.grid_rowconfigure(index=0, weight=1)
        self.left_skip_button.grid_columnconfigure(index=0, weight=1)
        self.left_skip_button.grid(row=0, column=1)
        self.left_skip_button.configure(command=self._left_skip_button_command)

        self.right_skip_button = Button(
            master=self.button_interface,
            width=20,
            text="",
            hover=False,
            border_width=0,
            fg_color="transparent"
        )
        self.right_skip_button.grid_rowconfigure(index=0, weight=1)
        self.right_skip_button.grid_columnconfigure(index=0, weight=1)
        self.right_skip_button.grid(row=0, column=5)
        self.right_skip_button.configure(command=self._right_skip_button_command)

        self.left_glue = Frame(
            master=self.button_interface,
            width=40,
            height=10,
            fg_color="transparent"
        )
        self.left_glue.grid(row=0, column=2)

        self.right_glue = Frame(
            master=self.button_interface,
            width=40,
            height=10,
            fg_color="transparent"
        )
        self.right_glue.grid(row=0, column=4)

        self.glue = Frame(master=self, height=10, fg_color="transparent")
        self.glue.grid(row=1, column=0)

        self.player_slider = PlayerSlider(master=self, from_=0, to=10)
        self.player_slider.grid(row=0, column=0, sticky="nsew")

    def set_icons(self, data: dict) -> None:
        self.play_button.configure(image=data["play_button"], require_redraw=True)
        self.pause_button.configure(image=data["pause_button"], require_redraw=True)
        self.left_skip_button.configure(image=data["left_skip_button"], require_redraw=True)
        self.right_skip_button.configure(image=data["right_skip_button"], require_redraw=True)

    def set_player(self, player: MPV) -> None:
        self.player = player
        self.player_slider.set_player(player)

    def _play_button_command(self) -> None:
        self.player.pause = False
        self.pause_button.tkraise()

    def _pause_button_command(self) -> None:
        self.player.pause = True
        self.play_button.tkraise()

    def _right_skip_button_command(self) -> None:
        self.player.playlist_prev()
        self.pause_button.tkraise()

    def _left_skip_button_command(self) -> None:
        self.player.playlist_next()
        self.pause_button.tkraise()


class PlayerSlider(Slider):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.set(0)
        self.bind("<ButtonRelease-1>", self._update_position)
        self.bind("<ButtonPress-1>", lambda _: self.player.unobserve_property(name='time-pos', handler=self._update_slider))
        self.configure(number_of_steps=1000)

    def set_player(self, player: MPV) -> None:
        self.player = player
        self.player.observe_property(name='time-pos', handler=self._update_slider)

    def _update_slider(self, _: str, value: int) -> None:
        self.set((value / self.player.duration) * 10)  # type: ignore

    def _update_position(self, _: Event | None = None) -> None:
        self.player.seek(self.get() * self.player.duration / 10 - self.player.time_pos)  # type: ignore
        self.player.observe_property(name='time-pos', handler=self._update_slider)
