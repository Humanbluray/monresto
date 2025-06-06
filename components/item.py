import flet as ft
from utils.couleurs import MAIN_COLOR, SECOND_COLOR, THIRD_COLOR


class ItemMenu(ft.Container):
    def __init__(self, title: str, my_icon: str, selected_color: str):
        super().__init__(
            shape=ft.BoxShape.RECTANGLE,
            padding=ft.padding.only(10, 12,10,12),
            border_radius=16, scale=ft.Scale(1), width=120, height=80,
            animate_size=ft.Animation(300, ft.AnimationCurve.EASE_IN)
        )
        self.title = title
        self.my_icon = my_icon
        self.selected_color = selected_color
        self.is_clicked = False

        self.visuel = ft.Icon(self.my_icon, size=22, color=self.selected_color)
        self.name = ft.Text(title.lower().capitalize(), font_family="PPM", size=13, color=self.selected_color)
        self.content = ft.Column(
            [self.visuel, self.name], horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER)

    def hover_ct(self, e):
        if e.data == "true":
            e.control.scale = 1.1
            e.control.update()
        else:
            if self.is_clicked:
                self.name.size = 14
                self.name.font_family = "PPM"
                self.visuel.color = SECOND_COLOR
                self.name.color = ft.Colors.BLACK87
                self.bgcolor = THIRD_COLOR
                self.visuel.update()
                self.name.update()
                self.update()
            else:
                self.name.size = 13
                self.name.font_family = "PPM"
                self.visuel.color = self.selected_color
                self.name.color = self.selected_color
                self.bgcolor = None
                self.visuel.update()
                self.name.update()
                self.update()

    def set_is_clicked_true(self):
        self.name.size = 14
        self.name.font_family = "PPM"
        self.visuel.color = SECOND_COLOR
        self.name.color = ft.Colors.BLACK87
        self.bgcolor = THIRD_COLOR
        self.visuel.update()
        self.name.update()
        self.update()

    def set_is_clicked_false(self):
        self.name.size = 13
        self.name.font_family = "PPM"
        self.visuel.color = self.selected_color
        self.name.color = self.selected_color
        self.bgcolor = None
        self.visuel.update()
        self.name.update()
        self.update()

