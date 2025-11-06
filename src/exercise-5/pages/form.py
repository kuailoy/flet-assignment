import datetime
import flet as ft
from flet import View, AppBar, Column, TextField, RadioGroup, Radio, Dropdown, IconButton, Icons, ElevatedButton, Text, MainAxisAlignment, CrossAxisAlignment

def form_view(page, last_form_data: dict) -> View:
    name_field = TextField(label="Name", width=500)
    # use modal DatePicker (opened with page.open) instead of inline DatePicker
    selected_dob = {"value": None}
    dob_display = Text(selectable=False)

    def on_date_change(e):
        selected_dob["value"] = e.control.value
        dob_display.value = "Date of Birth: " + selected_dob["value"].strftime("%Y-%m-%d")
        page.update()

    def on_date_dismiss(e):
        # optional: show nothing or a message; keep simple no-op
        pass

    def open_date_picker(e):
        page.open(
            ft.DatePicker(
                first_date=datetime.date(1900, 1, 1),
                last_date=datetime.date(2100, 12, 31),
                value=selected_dob["value"],
                on_change=on_date_change,
                on_dismiss=on_date_dismiss,
            )
        )

    gender_group = RadioGroup(
        content=Column([Radio(value="Male", label="Male"),
                        Radio(value="Female", label="Female"),
                        Radio(value="Other", label="Other")])
    )
    address_field = TextField(label="Address", width=500)
    country_dropdown = Dropdown(
        width=200,
        options=[
            ft.dropdown.Option("Country"),  # placeholder option
            ft.dropdown.Option("Finland"),
            ft.dropdown.Option("Sweden"),
            ft.dropdown.Option("Estonia"),
            ft.dropdown.Option("Other"),
        ],
        value="Country",  # show placeholder initially
    )

    def create_clicked(_):
        last_form_data.clear()
        last_form_data.update(
            {
                "name": name_field.value or "",
                "dob": selected_dob["value"].strftime("%Y-%m-%d") if selected_dob["value"] else "",
                "gender": getattr(gender_group, "value", "") or "",
                "address": address_field.value or "",
                "country": (country_dropdown.value if country_dropdown.value != "Select country" else ""),
            }
        )
        page.go("/details")

    return View(
        route="/form",
        controls=[
            AppBar(title=Text("Form Page", color="white"), bgcolor="#333333",
                   leading=IconButton(icon=Icons.ARROW_BACK, icon_color="white", on_click=lambda _: page.go("/"))),
            Column(
                [
                    name_field,
                    ft.Row([dob_display, ft.ElevatedButton("Date of Birth", icon=Icons.CALENDAR_MONTH, on_click=open_date_picker)], alignment="start"),
                    Text("Gender:"),
                    gender_group,
                    address_field,
                    country_dropdown,
                    ElevatedButton(text="Create", on_click=create_clicked),
                ],
                spacing=12,
                alignment="start",
            ),
        ],
        vertical_alignment=MainAxisAlignment.START,
        horizontal_alignment=CrossAxisAlignment.START,
        padding=20,
    )