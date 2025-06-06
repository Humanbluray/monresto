from utils.couleurs import *
from components.navbar import NavBar
from components import MyButton, MyCtButton
from services.supabase_client import supabase_client
from utils.useful_functions import convert_date

logo_url = 'https://byggqnusosovxulbchup.supabase.co/storage/v1/object/public/drink-bucket//paytable.png'


class Home(ft.View):
    def __init__(self, page: ft.Page, user_id: str):
        super().__init__(
            route=f'/home/{user_id}', horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.CENTER, bgcolor=PAGE_BG_COLOR,
            padding=10
        )
        self.user_id = user_id
        self.page = page
        self.user_infos = {'restaurant id': '', 'username': ''}
        self.shop_name = ft.Text("", size=13, font_family="PPR", color=ft.Colors.BLACK87)
        self.role = ft.Text("")
        self.user_account = ft.Text('', size=13, font_family="PPM", color=ft.Colors.BLACK87)
        self.fin_abonnement = ft.Text(size=12, font_family="PPR", color=ft.Colors.BLACK87)

        self.top_part = ft.Container(
            padding=ft.padding.only(10, 10, 10,10), bgcolor='white', border_radius=10,
            content=ft.Row(
                controls=[
                    ft.Image(src=logo_url, width=50, height=50),
                    ft.Row(
                        controls=[
                            ft.Container(
                                padding=10, border_radius=12, bgcolor='#f0f0f6',
                                content=ft.Row(
                                    controls=[
                                        ft.Row(
                                            controls=[
                                                ft.Icon(ft.Icons.FOOD_BANK_OUTLINED, size=24,
                                                        color=ft.Colors.BLACK38),
                                                self.shop_name,
                                            ], alignment=ft.MainAxisAlignment.CENTER
                                        ),
                                        ft.Container(
                                            bgcolor=ft.Colors.GREEN_50, border=ft.border.all(1, 'green'),
                                            border_radius=16,
                                            padding=ft.padding.only(10, 3, 10, 3),
                                            content=ft.Row(
                                                controls=[
                                                    ft.Icon(ft.Icons.CHECK_CIRCLE, size=16, color='green'),
                                                    ft.Text('Actif', size=12, font_family='PPM', color='green')
                                                ], alignment=ft.MainAxisAlignment.CENTER
                                            )
                                        ),
                                        # ft.Row(
                                        #     controls=[
                                        #         ft.Icon(ft.Icons.CALENDAR_MONTH_OUTLINED, color=ft.Colors.BLACK45),
                                        #         ft.Text("Fin abonnement", size=12, color=ft.Colors.BLACK45),
                                        #         self.fin_abonnement
                                        #     ]
                                        # )
                                    ]
                                )
                            ),

                        ]
                    ),
                    ft.Row(
                        controls=[
                            ft.Container(
                                padding=10, border_radius=16, bgcolor=PAGE_BG_COLOR,
                                # border=ft.border.all(1, "grey"),
                                content=ft.Row(
                                    [
                                        ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=24, color=ft.Colors.BLACK87),
                                        self.user_account,
                                     ], alignment=ft.MainAxisAlignment.CENTER, spacing=5
                                ),

                            ),

                            ft.VerticalDivider(width=10, color=ft.Colors.TRANSPARENT),
                            MyCtButton(ft.Icons.LOGOUT, 'grey', None)
                        ]
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )
        )
        self.left_part = ft.Container(
            padding=10, bgcolor="white", border_radius=10,
            content=NavBar(self)
        )
        self.my_content = ft.Column(
            expand=True
        )
        self.box = ft.AlertDialog(
            title=ft.Text(size=16, font_family="PPM"),
            content=ft.Text(size=12, font_family="PPM"),
            actions=[MyButton("Quitter", "red", 120, self.close_box)]
        )
        self.snack = ft.SnackBar(
            show_close_icon=True, elevation=10,
            content=ft.Row([ft.Text("Article ajouté", size=12, font_family="PPM")]),
            bgcolor=ft.Colors.BLACK87, behavior=ft.SnackBarBehavior.FLOATING
        )
        self.fp_new_image = ft.FilePicker()
        self.fp_edit_image = ft.FilePicker()

        for widget in (self.fp_new_image, self.fp_edit_image, self.box, self.snack):
            self.page.overlay.append(widget)

        self.controls = [
            ft.Column(
                expand=True,
                controls=[
                    self.top_part,
                    ft.Row(
                        expand=True,
                        controls=[
                            self.left_part,
                            ft.Container(
                                expand=True, padding=0,
                                content=self.my_content,
                            )
                        ]
                    )
                ]
            )
        ]
        self.set_infos()

    def close_box(self, e):
        self.box.open = False
        self.box.update()

    def set_infos(self):
        resp = supabase_client.table('users').select('*').eq("uid", self.user_id).single().execute()
        self.role.value = resp.data["role"]
        self.user_account.value = f"{resp.data['prenom']} {resp.data['nom']}"
        self.user_infos['username'] = f"{resp.data['prenom']} {resp.data['nom']}"

        resp = supabase_client.table('users').select('restaurant_id').eq('uid', self.user_id).single().execute()
        id_resto = resp.data['restaurant_id']
        resto = supabase_client.table("restaurants").select("nom").eq('id', id_resto).single().execute()
        self.shop_name.value = resto.data['nom']
        self.user_infos['restaurant id'] = id_resto

        resp_abo = supabase_client.table('abonnements').select('date_debut', 'date_fin',).single().execute()
        self.fin_abonnement.value = convert_date(str(resp_abo.data['date_fin']))


