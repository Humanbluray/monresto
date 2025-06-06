import time
from components import MyButton, MyCtButton, SaleCard
import datetime
from utils.useful_functions import *
from utils.styles import *
from services.supabase_client import supabase_client


class Sales(ft.Container):
    def __init__(self, cp: object):
        super().__init__(
            expand=True, padding=0
        )
        self.cp = cp
        self.utilisateur_id = self.cp.user_id
        self.restaurant_id = self.cp.user_infos['restaurant id']
        self.grid = ft.GridView(
            expand=True, runs_count=5, child_aspect_ratio=0.7,
            spacing=10, run_spacing=10, max_extent=180
        )
        self.search = ft.TextField(
            **field_style, expand=True, label="search", prefix_icon="search", on_change=self.filter_datas
        )
        self.items_container = ft.Container(
            padding=20, bgcolor="white", border_radius=10, expand=True,
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            self.search,
                            MyCtButton(ft.Icons.FILTER_ALT_OFF_OUTLINED, "grey", self.supp_filtres)
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    self.grid
                ]
            )
        )
        self.table_number = ft.TextField(**field_style, dense=True, label="Table", width=120, prefix_icon=ft.Icons.TABLE_RESTAURANT_OUTLINED)
        self.cashier = ft.Text(f"{self.cp.user_infos['username']}", size=12, font_family="PPM")
        self.nb_items = ft.Text("0 item", size=12, font_family="PPM")
        self.bill_amount = ft.Text("0 XAF", size=14, font_family="PPB")
        self.mini_items_ct = ft.ListView(expand=True, spacing=10, divider_thickness=1,)
        self.bill_number = ft.Text(f'{find_facture_number()}', size=12, font_family="PPR", color='grey')
        self.pay_mode = ft.RadioGroup(
            content = ft.Row(
                controls=[
                    ft.Radio(
                        **radio_style, label=option['label'], value=option['value']
                    )
                    for option in [
                        {'label': "OM", 'value': 'OM'}, {'label': "MOMO", 'value': 'MOMO'}, {'label': "Espèces", 'value': 'espèces'}
                    ]
                ]
            ), on_change=self.changing_pay_mode
        )
        self.pay_gift = ft.TextField(
            **field_style, input_filter=ft.NumbersOnlyInputFilter(), text_align=ft.TextAlign.RIGHT, width=130,
            value="0", on_blur=self.calculate_rest, suffix_text=" XAF", dense=True, expand=True,
            prefix_icon=ft.Icons.MONETIZATION_ON_OUTLINED, label="versement"
        )
        self.rest = ft.Text("0,00", size=12, font_family='PPM')
        self.bill_container = ft.Container(
            padding=ft.padding.only(20, 10, 20, 10), bgcolor="white", border_radius=10, width=290,  # expand=True,
            content=ft.Column(
                controls=[
                    ft.Column(
                        expand=True,
                        controls=[
                            ft.Column(
                                controls=[
                                    ft.Row(
                                        [
                                            ft.Text("Facture N°", size=14, font_family="PSB"),
                                            self.bill_number,
                                        ], alignment=ft.MainAxisAlignment.CENTER
                                    ),
                                    ft.Divider(height=5, color=ft.Colors.TRANSPARENT),
                                    ft.Column(
                                        spacing=5, controls=[
                                            ft.Row(
                                                controls=[
                                                    self.table_number
                                                ], alignment=ft.MainAxisAlignment.CENTER
                                            ),
                                            ft.Row(
                                                controls=[
                                                    ft.Text("Caissier:", size=12, font_family="PPI", color="grey"),
                                                    self.cashier
                                                ], alignment=ft.MainAxisAlignment.CENTER
                                            ),
                                            ft.Row([self.nb_items], alignment=ft.MainAxisAlignment.CENTER)
                                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER
                                    )

                                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER
                            ),

                            ft.Divider(height=1, thickness=1),
                            self.mini_items_ct
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    ft.Column(
                        controls=[
                            ft.Divider(height=1, thickness=1),
                            ft.Text("Paiement".upper(), size=14, font_family="PSB"),
                            self.pay_mode,
                            ft.Row(
                                controls=[
                                    # ft.Text("Versement", size=12, font_family="PPI", color=ft.Colors.BLACK45),
                                    self.pay_gift,
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text("Reste", size=12, font_family="PPI", color=ft.Colors.BLACK45),
                                    self.rest,
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            ),
                            ft.Row(
                                [
                                    ft.Text('Total Facture', size=12, font_family="PPI", color=ft.Colors.BLACK45),
                                    self.bill_amount
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            ),
                            MyButton("Valider paiement", SECOND_COLOR, None, self.validate_bill)
                        ]
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )
        )
        self.main_window = ft.Container(
            expand=True, padding=0,
            content=ft.Row(
                expand=True,
                controls=[
                    self.items_container,
                    self.bill_container
                ]
            )
        )
        self.content = ft.Stack(
            expand=True,
            controls=[
                self.main_window
            ]
        )
        self.load_datas()

    def load_datas(self):
        self.grid.controls.clear()

        resp = supabase_client.table('users').select('restaurant_id').eq('uid', self.cp.user_id).single().execute()
        response = supabase_client.table("produits").select('*').execute()
        datas = response.data

        for widget in self.grid.controls[:]:
            self.grid.controls.remove(widget)

        for data in datas:
            self.grid.controls.append(
                SaleCard(self, data)
            )

    def filter_datas(self, e):
        search = self.search.value if self.search.value is not None else ""
        resp = supabase_client.table('users').select('restaurant_id').eq('uid', self.cp.user_id).single().execute()
        response = supabase_client.table("produits").select('*').execute()
        datas = response.data

        filtered_datas = list(filter(lambda x: search in x['designation'], datas))
        self.grid.controls.clear()

        for data in filtered_datas:
            self.grid.controls.append(
                SaleCard(self, data)
            )

        self.grid.update()

    def supp_filtres(self, e):
        self.load_datas()
        self.search.value = None
        self.grid.update()
        self.search.update()

    def calculate_rest(self, e):
        t = self.bill_amount.value.replace(", ", "")
        total_amount = t.replace(' XAF', "")

        reste = int(self.pay_gift.value) - int(total_amount)
        self.rest.value = f"{add_separator(reste)} XAF"
        self.rest.update()

    def changing_pay_mode(self, e):
        if self.pay_mode.value == "espèces":
            self.pay_gift.value = "0"
            self.pay_gift.disabled = False
            self.pay_gift.update()
            self.rest.value = None
            self.rest.update()
        else:
            t = self.bill_amount.value.replace(", ", "")
            total_amount = t.replace(' XAF', "")
            self.pay_gift.value = f"{total_amount}"
            self.pay_gift.disabled = True
            self.rest.value = "0 XAF"
            self.rest.update()
            self.pay_gift.update()

    def validate_bill(self, e):

        # Mise à jour des données dans la base de données
        t = self.bill_amount.value.replace(", ", "")
        total_amount = int(t.replace(' XAF', ""))
        montant_verse = int(self.pay_gift.value)
        reste = montant_verse - total_amount

        if self.pay_mode.value is not None:
            numero_facture = find_facture_number()
            # Ajouter une entrée à la table facture
            supabase_client.table('factures').insert(
                {
                    'restaurant_id': self.cp.user_infos['restaurant id'], 'user_id': self.cp.user_id,
                    'montant': total_amount, 'numero': numero_facture, 'numero_table': self.table_number.value
                }
            ).execute()

            # Ajouter les détails de facture
            for widget in self.mini_items_ct.controls[:]:
                supabase_client.table('details_factures').insert(
                    {
                        'facture_numero': numero_facture, 'produit_id': widget.infos['id'],
                        'qte': widget.infos['qty'], 'prix': widget.infos['prix']
                    }
                ).execute()
                new_stock = widget.infos['stock'] - widget.infos['qty']

                # On met à jour le stock des articles
                if widget.infos['type'] != 'nourriture':
                    supabase_client.table('produits').update({'stock': new_stock}).eq('id', widget.infos['id']).execute()
                else:
                    pass

            # impression du ticket de caisse

            # finalisation de la procédure
            self.mini_items_ct.controls.clear()
            self.mini_items_ct.update()

            self.pay_mode.value = None
            self.rest.value = None
            self.table_number.value = None
            self.pay_gift.value = "0"
            self.bill_number.value = find_facture_number()
            self.nb_items.value = "0 item"
            self.bill_amount.value = "0.00 XAF"

            for widget in (self.pay_mode, self.rest, self.pay_gift, self.bill_number, self.nb_items, self.bill_amount, self.table_number):
                widget.update()

            self.cp.box.title.value = "Validé"
            self.cp.box.content.value = 'Ticket imprimé avec succès'
            self.cp.box.open = True
            self.cp.box.update()

        else:
            self.cp.box.title.value = "Erreur"
            self.cp.box.content.value = 'Veuillez choisir le mode de paiement'
            self.cp.box.open = True
            self.cp.box.update()



