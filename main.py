import flet as ft
import os, re
from views.home import Home
from views.signin import Signin

SIGNIN_ROUTE = "/"
HOME_ROUTE = '/home'

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    page.title = "Pay 1.0 - 2025"
    page.fonts = {
        "PPL": "assets/fonts/Poppins-light.ttf",
        "PPM": "assets/fonts/Poppins-Medium.ttf",
        "PPI": "assets/fonts/Poppins-Italic.ttf",
        "PPB": "assets/fonts/Poppins-Bold.ttf",
        "PSB": "assets/fonts/Poppins-SemiBold.ttf",
        "PBL": "assets/fonts/Poppins-Black.ttf",
        "PPR": "assets/fonts/Poppins-Regular.ttf",
        "PEB": "assets/fonts/Poppins-ExtraBold.ttf",
    }

    # Routes
    route_views = {
        SIGNIN_ROUTE: Signin,
        HOME_ROUTE: Home,
    }

    # manage routes changes
    def route_change(event: ft.RouteChangeEvent):
        page.views.clear()
        current_route = event.route
        # Si on est sur la route "/home/<uid>"
        match = re.match(r"^/home/(.+)", current_route)

        if match:
            uid = match.group(1)
            page.views.append(Home(page, uid))  # Afficher la vue

        elif current_route in route_views:
            page.views.append(route_views[current_route](page))
        else:
            page.views.append(Signin(page))

        page.update()

    # Manage return
    def view_pop(view):
        top_view = page.views[-1]
        page.go(top_view.route)

    # Assignation des call backs
    page.on_route_change = route_change
    page.on_view_pop = view_pop

    # go to initial route
    page.go(page.route)

if __name__ == '__main__':
    port = int(os.getenv("PORT", 8080))
    ft.app(
        main, assets_dir="assets", route_url_strategy="default", port=port,
        view=ft.AppView.WEB_BROWSER
    )

