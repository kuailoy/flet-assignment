import flet as ft
from flet import Page, RouteChangeEvent, ViewPopEvent

from pages.login import login_view
from pages.form import form_view
from pages.details import details_view

def main(page: Page) -> None:
    page.title = "My store (3 pages)"
    last_form_data: dict = {}

    def route_change(e: RouteChangeEvent) -> None:
        page.views.clear()
        if page.route == "/":
            page.views.append(login_view(page))
        elif page.route == "/form":
            page.views.append(form_view(page, last_form_data))
        elif page.route == "/details":
            page.views.append(details_view(page, last_form_data))
        page.update()

    def view_pop(e: ViewPopEvent) -> None:
        if page.views:
            page.views.pop()
            if page.views:
                page.go(page.views[-1].route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

if __name__ == "__main__":
    ft.app(target=main)