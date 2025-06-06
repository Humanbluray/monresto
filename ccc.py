import flet as ft

def main(page: ft.Page):
    page.title = "Menus contextuels avec PopupMenu"
    page.horizontal_alignment = "start"

    # Menu 1
    menu1 = ft.PopupMenuButton(
        content=ft.Text("Menu 1"),
        items=[
            ft.PopupMenuItem(text="Option A1"),
            ft.PopupMenuItem(text="Option A2"),
        ]
    )

    # Menu 2
    menu2 = ft.PopupMenuButton(
        content=ft.Text("Menu 2"),
        items=[
            ft.PopupMenuItem(text="Option B1"),
            ft.PopupMenuItem(text="Option B2"),
        ]
    )

    # Menu 3
    menu3 = ft.PopupMenuButton(
        content=ft.Text("Menu 3"),
        items=[
            ft.PopupMenuItem(text="Option C1"),
            ft.PopupMenuItem(text="Option C2"),
        ]
    )

    # Les menus côte à côte
    page.add(
        ft.Row(
            [menu1, menu2, menu3],
            spacing=20,
        )
    )

ft.app(target=main)
