import flet as ft
from components.item import ItemMenu
from views.sales import Sales

logo_url = 'https://byggqnusosovxulbchup.supabase.co/storage/v1/object/public/drink-bucket//paytable.png'


class NavBar(ft.Container):
    def __init__(self, cp: object):
        super().__init__(
            padding=ft.padding.only(10, 15, 10, 15),
            border_radius=0, expand=True,
        )
        self.cp = cp # container parent ... Page home
        couleur = ft.Colors.BLACK54
        self.sales = ItemMenu("ventes", ft.Icons.RESTAURANT_OUTLINED, couleur)
        self.stocks = ItemMenu("Stocks", ft.Icons.LOCAL_GROCERY_STORE_OUTLINED, couleur)
        self.factures = ItemMenu("Factures", ft.Icons.NOTES_OUTLINED, couleur)

        self.children = [
            self.sales,  self.stocks, self.factures
        ]

        for child in self.children:
            child.on_click = self.click_on_menu

        self.content = ft.Column(
            controls=[
                ft.Column(
                    controls=[
                        self.sales,  self.stocks, self.factures
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                ft.Column(
                    controls=[
                        ft.Divider(height=1, thickness=1),
                        ft.Row(
                            [ft.Image(src=logo_url, width=70, height=70),],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        ft.Column(
                            controls=[
                                ft.Text('Pay v1.0 2025', size=9, font_family="PPR", color=ft.Colors.BLACK45),
                                ft.Text("VAN TECH SARL", size=9, font_family="PPR", color=ft.Colors.BLACK45),
                                ft.Text("vantech.infos@gmail.com", size=9, font_family="PPR", color=ft.Colors.BLACK45),
                            ], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        )
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )


    def click_on_menu(self, e):
        for child in self.children:
            child.set_is_clicked_false()

        e.control.set_is_clicked_true()
        e.control.update()

        for widget in self.cp.my_content.controls[:]:
            self.cp.my_content.controls.remove(widget)

        self.cp.my_content.update()

        if e.control.name.value.lower() == "ventes":
            self.cp.my_content.controls.append(Sales(self.cp))
        #
        # if e.control.name.value.lower() == "stocks":
        #     self.cp.my_content.controls.append(Stocks(self.cp))
        #
        self.cp.my_content.update()