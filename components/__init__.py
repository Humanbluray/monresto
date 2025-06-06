from utils.couleurs import *
from utils.useful_functions import *
import time
from utils.styles import *

default_image_url = 'https://byggqnusosovxulbchup.supabase.co/storage/v1/object/public/drink-bucket//not-available.webp'


class MyButton(ft.Container):
    def __init__(self, title: str, my_icon, my_width, click):
        super().__init__(
            padding=10,
            bgcolor=SECOND_COLOR,
            height=50, width=my_width, border_radius=24,
            on_click=click, on_hover=self.hover_effect,
            scale=ft.Scale(1),
            animate_scale=ft.Animation(300, ft.AnimationCurve.FAST_OUT_SLOWIN)
        )
        self.title = title
        self.my_width = my_width
        self.click = click
        self.my_icon = my_icon
        visible = False if my_icon is None else True

        self.content = ft.Row(
            controls=[
                ft.Icon(my_icon, size=18, color="white", visible=visible),
                ft.Text(title.lower().capitalize(), size=14, font_family="PPM", color="white"),
            ], alignment=ft.MainAxisAlignment.CENTER,
        )

    def hover_effect(self, e):
        if e.data == 'true':
            self.scale = 1.04
            self.update()
        else:
            self.scale = 1
            self.update()


class ItemBill(ft.ListTile):
    def __init__(self, cp: object, infos: dict):
        super().__init__(
            title=ft.Text(infos['designation'], size=12, font_family="PPM"),
            subtitle=ft.Text(f"{infos['prix']} * {infos['qty']}", size=12, font_family='PPM', color='grey'),
            trailing=ft.IconButton(
                ft.Icons.DELETE_OUTLINED, icon_color=SECOND_COLOR, icon_size=22, bgcolor="white",
                on_click=self.remove
            )
        )
        self.infos = infos
        self.cp = cp

        self.leading = ft.Image(src=self.infos['image'], width=40, height=40)

    def remove(self, e):
        self.cp.mini_items_ct.controls.remove(self)
        self.cp.mini_items_ct.update()

        total = 0
        for widget in self.cp.mini_items_ct.controls[:]:
            total += (widget.infos['prix'] * widget.infos['qty'])

        self.cp.bill_amount.value = f"{add_separator(total)} XAF"

        self.cp.mini_items_ct.update()
        self.cp.bill_amount.update()

        self.cp.nb_items.value = f"{len(self.cp.mini_items_ct.controls)} items" if len(
            self.cp.mini_items_ct.controls) > 1 else f"{len(self.cp.mini_items_ct.controls)} item"
        self.cp.nb_items.update()


class SaleCard(ft.Card):
    def __init__(self, cp: object, infos: dict):
        super().__init__(
            elevation=10, surface_tint_color='white', width=180,
        )
        self.cp = cp
        self.infos = infos

        if self.infos['is_in_promo']:
            promo_icon = ft.Icons.KEYBOARD_DOUBLE_ARROW_DOWN_OUTLINED
        else:
            promo_icon = None

        if self.infos['image_url'] is not None:
            picture_src = infos['image_url']
        else:
            picture_src = default_image_url

        self.qty = ft.Text("0", size=16, font_family="PPB")
        self.container_qty = ft.Container(
            bgcolor=ft.Colors.GREY_200, width=60, height=40, border_radius=8,
            content=ft.Row([self.qty], alignment=ft.MainAxisAlignment.CENTER),
            on_click=self.ajouter_item
        )

        self.content = ft.Container(
            padding=ft.padding.only(10, 15, 10, 15), height=160,
            border_radius=12, bgcolor='white',
            content=ft.Column(
                controls=[
                    ft.Container(
                        height=100, width=180,
                        content=ft.Image(src=picture_src, fit=ft.ImageFit.COVER)
                    ),
                    ft.Column(
                        controls=[
                           ft.Container(
                               width=200, content= ft.Text(
                                    self.infos['designation'], size=12, font_family="PPR",
                                    overflow=ft.TextOverflow.ELLIPSIS, max_lines=1, width=170,
                                   text_align=ft.TextAlign.CENTER
                                ),
                           ),
                            ft.Row(
                                [
                                    ft.Text(
                                        add_separator(self.infos['price']), size=14, font_family="PPM",
                                        color=ft.Colors.BLACK
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.CENTER
                            ),
                        ], spacing=0
                    ),
                    ft.Row(
                        controls=[
                            MyCtButton(ft.Icons.REMOVE, 'red', self.quantity_down),
                            self.container_qty,
                            MyCtButton('add', 'red', self.quantity_up),
                        ], spacing=1, alignment=ft.MainAxisAlignment.CENTER
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )

    def quantity_up(self, e):
        qty = int(self.qty.value)
        new_qty = qty + 1
        self.qty.value = str(new_qty)
        self.qty.update()
        self.infos['qty'] = new_qty

    def quantity_down(self, e):
        qty = int(self.qty.value)

        if qty == 0:
            pass
        else:
            new_qty = qty - 1
            self.qty.value = str(new_qty)
            self.qty.update()
            self.infos['qty'] = new_qty

    def ajouter_item(self, e):

        if self.qty.value == "0":
            self.cp.cp.box.title.value = "Erreur"
            self.cp.cp.box.content.value = "Quantité nulle"
            self.cp.cp.box.open = True
            self.cp.cp.box.update()

        else:
            if self.infos['type'] == 'BOISSON':
                if self.infos['stock'] < int(self.qty.value):
                    self.cp.cp.box.title.value = "Erreur"
                    self.cp.cp.box.content.value = "Pas assez de stock"
                    self.cp.cp.box.open = True
                    self.cp.cp.box.update()
                else:
                    if self.infos['is_in_promo']:
                        prix = self.infos['promo price']
                    else:
                        prix = self.infos['price']

                    self.cp.mini_items_ct.controls.append(
                        ItemBill(
                            self.cp, {
                                'designation': self.infos['designation'], 'id': self.infos['id'],
                                'prix': prix, 'qty': self.infos['qty'], 'image': self.infos['image_url'],
                                'stock': self.infos['stock'], 'type': self.infos['type']
                            }
                        )
                    )

                    total = 0
                    for widget in self.cp.mini_items_ct.controls[:]:
                        total += (widget.infos['prix'] * widget.infos['qty'])

                    self.cp.bill_amount.value = f"{add_separator(total)} XAF"

                    self.cp.mini_items_ct.update()
                    self.cp.bill_amount.update()

                    self.qty.value = "0"
                    self.qty.update()
                    self.cp.cp.snack.open = True
                    self.cp.cp.snack.update()
                    time.sleep(0.5)
                    self.cp.cp.snack.open = False
                    self.cp.cp.snack.update()


            elif self.infos['type'] == "NOURRITURE":
                self.cp.mini_items_ct.controls.append(
                    ItemBill(
                        self.cp, {
                            'designation': self.infos['designation'], 'id': self.infos['id'],
                            'prix': self.infos['price'], 'qty': self.infos['qty'], 'image': self.infos['image_url'],
                            'stock': self.infos['stock'], 'type': self.infos['type']
                        }
                    )
                )

                total = 0
                for widget in self.cp.mini_items_ct.controls[:]:
                    total += (widget.infos['prix'] * widget.infos['qty'])

                self.cp.bill_amount.value = f"{add_separator(total)} XAF"

                self.cp.mini_items_ct.update()
                self.cp.bill_amount.update()

                self.qty.value = "0"
                self.qty.update()

                self.cp.cp.snack.open = True
                self.cp.cp.snack.update()
                time.sleep(0.5)
                self.cp.cp.snack.open = False
                self.cp.cp.snack.update()

            else:
                if self.infos['stock'] < int(self.qty.value):
                    self.cp.cp.box.title.value = "Erreur"
                    self.cp.cp.box.content.value = "Pas assez de stock"
                    self.cp.cp.box.open = True
                    self.cp.cp.box.update()
                else:
                    self.cp.mini_items_ct.controls.append(
                        ItemBill(
                            self.cp, {
                                'designation': self.infos['designation'], 'id': self.infos['id'],
                                'prix': self.infos['price'], 'qty': self.infos['qty'], 'image': self.infos['image_url'],
                                'stock': self.infos['stock'], 'type': self.infos['type']
                            }
                        )
                    )

                    total = 0
                    for widget in self.cp.mini_items_ct.controls[:]:
                        total += (widget.infos['prix'] * widget.infos['qty'])

                    self.cp.bill_amount.value = f"{add_separator(total)} XAF"

                    self.cp.mini_items_ct.update()
                    self.cp.bill_amount.update()

                    self.qty.value = "0"
                    self.qty.update()

                    self.cp.cp.snack.open = True
                    self.cp.cp.snack.update()
                    time.sleep(0.5)
                    self.cp.cp.snack.open = False
                    self.cp.cp.snack.update()


            self.cp.nb_items.value = f"{len(self.cp.mini_items_ct.controls)} items" if len(
                self.cp.mini_items_ct.controls) > 1 else f"{len(self.cp.mini_items_ct.controls)} item"
            self.cp.nb_items.update()


class MyCtButton(ft.Container):
    def __init__(self, title: str, couleur: str, click):
        super().__init__(
            border_radius=8, padding=ft.padding.only(5, 5, 5, 5),
            on_click=click, on_hover=self.hover_effect,
            border=ft.border.all(1, ft.Colors.GREY),
            bgcolor=ft.Colors.GREY_50
        )
        self.couleur = couleur
        self.my_icon = ft.Icon(name=title, color=self.couleur, size=20)
        self.content = ft.Row(
            controls=[
                self.my_icon,
            ], alignment=ft.MainAxisAlignment.CENTER
        )

    def hover_effect(self, e):
        if e.data == "true":
            self.my_icon.color = "black"
            self.my_icon.update()
        else:
            self.my_icon.color = self.couleur
            self.my_icon.update()


class DateSelection(ft.Row):
    def __init__(self, ):
        super().__init__()
        self.day = ft.Dropdown(
            **drop_style, width=85, text_align=ft.TextAlign.RIGHT,
            options=[ft.dropdown.Option(f"{i}") for i in range(1, 32)], hint_text='JJ'
        )
        self.month = ft.Dropdown(
            **drop_style, width=85, text_align=ft.TextAlign.RIGHT, hint_text='MM',
            options=[ft.dropdown.Option(f"{i}") for i in range(1, 13)]
        )
        self.year = ft.TextField(
            height=50,
            focused_border_width=2, focused_border_color=MAIN_COLOR,
            label_style=ft.TextStyle(size=12, font_family="PPM", color="black"),
            hint_style=ft.TextStyle(size=12, font_family="PPM"),
            text_style=ft.TextStyle(size=12, font_family="PPM"),
            border_radius=12, border_width=1, cursor_color=SECOND_COLOR,
            capitalization=ft.TextCapitalization.CHARACTERS,
            input_filter=ft.NumbersOnlyInputFilter(), width=80,
            text_align=ft.TextAlign.RIGHT, hint_text='AAAA'
        )
        self.controls=[
            ft.Row(
                controls=[
                    self.day, self.month, self.year
                ], spacing=2
            )
        ]


