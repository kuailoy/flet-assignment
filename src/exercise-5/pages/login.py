import flet as ft
from flet import View, AppBar, Column, TextField, ElevatedButton, Text, SnackBar, MainAxisAlignment, CrossAxisAlignment

def login_view(page) -> View:
    email_field = TextField(label="Email", width=300)
    password_field = TextField(label="Password", password=True, can_reveal_password=True, width=300)

    def login_clicked(_):
        # reset previous errors
        email_field.error_text = None
        password_field.error_text = None

        has_error = False
        if not (email_field.value and email_field.value.strip()):
            email_field.error_text = "Please enter an email"
            has_error = True
        if not (password_field.value and password_field.value.strip()):
            password_field.error_text = "Please enter a password"
            has_error = True

        page.update()
        if has_error:
            return

        page.go("/form")

    return View(
        route="/",
        controls=[
            AppBar(title=Text("Flet app", color="white"), bgcolor="#333333"),
            Column(
                [
                    email_field,
                    password_field,
                    ElevatedButton(text="Log in", on_click=login_clicked),
                ],
                spacing=8,
                alignment="start",
            ),
        ],
        padding=10,
        vertical_alignment=MainAxisAlignment.START,
        horizontal_alignment=CrossAxisAlignment.START,
    )