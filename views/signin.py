import flet as ft
from components import MyButton
from utils.styles import login_style
from utils.couleurs import MAIN_COLOR, SECOND_COLOR, PAGE_BG_COLOR
from services.supabase_client import supabase_client
logo_url = 'https://byggqnusosovxulbchup.supabase.co/storage/v1/object/public/drink-bucket//paytable.png'


class Signin(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(
            route='/', horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.CENTER, bgcolor=PAGE_BG_COLOR, padding=0,
        )
        self.page = page
        self.email = ft.TextField(
            **login_style, label="Email", prefix_icon=ft.Icons.MAIL_OUTLINED
        )
        self.password = ft.TextField(
            **login_style, label="Mot de passe", prefix_icon=ft.Icons.KEY_OFF_OUTLINED,
            can_reveal_password=True, password=True
        )
        self.connect_button = MyButton('Se connecter', None, None, self.connecter)
        self.infos_container = ft.Container(
            bgcolor="white", width=300, border_radius=16, padding=20, height=550,
            content=ft.Column(
                controls=[
                    ft.Row(
                        [ft.Image(src=logo_url, width=100, height=100),],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Column(
                        controls=[
                            ft.Text('Bonjour', size=13, font_family="PPR"),
                            ft.Text('Bienvenue', size=24, font_family="PPB")
                        ], spacing=0
                    ),
                    ft.Divider(height=5, color=ft.Colors.TRANSPARENT),
                    self.email,
                    self.password,
                    self.connect_button,
                    # ft.Divider(height=1, color=ft.Colors.TRANSPARENT),
                ],
            )
        )
        self.box = ft.AlertDialog(
            title=ft.Text(size=16, font_family="PPM"),
            content=ft.Text(size=12, font_family="PPM"),
            actions=[MyButton("Quitter", "red", 120, self.close_box)]
        )
        self.page.overlay.append(self.box)

        self.controls = [
            ft.Stack(
                expand=True,
                controls=[
                    ft.Container(
                        expand=True,
                        gradient=ft.LinearGradient(
                            begin=ft.alignment.top_left, end=ft.alignment.bottom_right,
                            colors=['#f0f0f6', ft.Colors.GREY_50],
                        ),
                        alignment=ft.alignment.center,
                        content=ft.Row(
                            controls=[
                                ft.Card(
                                    elevation=10,
                                    shape=ft.RoundedRectangleBorder(radius=16),
                                    content=self.infos_container
                                )
                            ], alignment=ft.MainAxisAlignment.CENTER,
                        )
                    )

                ], alignment=ft.alignment.center
            )
        ]

    def connecter(self, e):
        email = self.email.value
        password = self.password.value

        if not email or not password:
            self.box.title.value = 'Erreur de connexion'
            self.box.content.value = 'Tous les champs sont obligatoires'
            self.box.open = True
            self.box.update()

        else:
            try:
                res = supabase_client.auth.sign_in_with_password({"email": email, "password": password})
                session = res.session
                user_id = res.user.id
                # print(f"id: {res.user.id}")

                if session:
                    self.page.client_storage.set("token", session.access_token)
                    self.page.client_storage.set("user_id", res.user.id)

                    resp = supabase_client.table("users").select("role").eq("uid", user_id).single().execute()
                    role = resp.data["role"]

                    if role == "admin":
                        pass
                    else:
                        response_id_resto = supabase_client.table('users').select('restaurant_id').eq('uid', user_id).single().execute()
                        id_resto = response_id_resto.data['restaurant_id']
                        resp_statut = supabase_client.table('abonnements').select('date_debut', 'date_fin', 'actif').single().execute()

                        if resp_statut.data['actif']:
                            self.page.go(f'/home/{user_id}')
                        else:
                            self.box.title.value = 'Erreur'
                            self.box.content.value = 'Votre abonnement est inactif'
                            self.box.open = True
                            self.box.update()

                else:
                    self.box.title.value = 'Erreur'
                    self.box.content.value ='Identifiants incorrects'
                    self.box.open = True
                    self.box.update()

            except Exception as ex:
                self.box.title.value = 'Erreur'
                self.box.content.value = f"Erreur : {str(ex)}"
                self.box.open = True
                self.box.update()

            self.update()

    def close_box(self, e):
        self.box.open = False
        self.box.update()