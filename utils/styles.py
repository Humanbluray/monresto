import flet as ft
from utils.couleurs import *

login_style: dict = dict(
    text_style=ft.TextStyle(size=13, font_family="PPM", color="black"), label_style=ft.TextStyle(size=12, font_family="PPM", color="black"),
    hint_style=ft.TextStyle(size=13, font_family="PPM"), border_radius=12, content_padding=12, height=45,
    cursor_height=24, cursor_color=SECOND_COLOR, border_width=1, focused_border_width=2, focused_border_color=MAIN_COLOR,
)
field_style: dict = dict(
    height=50,
    border_color="#f0f0f6", bgcolor="#f0f0f6",
    content_padding=12, cursor_height=24,
    label_style=ft.TextStyle(size=12, font_family="PPM", color="black"),
    hint_style=ft.TextStyle(size=12, font_family="PPM"),
    text_style=ft.TextStyle(size=13, font_family="PPM"),
    border_radius=12, border_width=1, cursor_color=SECOND_COLOR,
    capitalization=ft.TextCapitalization.CHARACTERS
)
radio_style = dict(
    label_style=ft.TextStyle(size=12, font_family="PPM"),
    fill_color=SECOND_COLOR
)
datatable_style: dict = dict(
    data_text_style=ft.TextStyle(size=12, font_family="PPM"),
    heading_text_style=ft.TextStyle(size=12, font_family="PPM", color='grey')
)
field_style_2: dict = dict(
    height=50,
    focused_border_color=MAIN_COLOR,
    content_padding=12, cursor_height=24,
    label_style=ft.TextStyle(size=12, font_family="PPM", color="black"),
    hint_style=ft.TextStyle(size=12, font_family="PPM"),
    text_style=ft.TextStyle(size=13, font_family="PPM"),
    border_radius=12, border_width=1, cursor_color=SECOND_COLOR,
    focused_border_width=1,
    capitalization=ft.TextCapitalization.CHARACTERS
)
drop_style: dict = dict(
    dense=True, border_radius=9,
    label_style=ft.TextStyle(font_family="PPM", size=11),
    text_style=ft.TextStyle(font_family="PPM", size=13),
    hint_style=ft.TextStyle(font_family="PPM", size=11),
    border_width=1, focused_border_width=2
)