from flet import View, AppBar, IconButton, Icons, Column, Text, ElevatedButton, MainAxisAlignment, CrossAxisAlignment

def details_view(page, last_form_data: dict) -> View:
    def go_back(_):
        page.go("/")

    return View(
        route="/details",
        controls=[
            AppBar(title=Text("Result", color="white"), bgcolor="#333333",
                   leading=IconButton(icon=Icons.ARROW_BACK, icon_color="white", on_click=go_back)),
            Column(
                [
                    Text(f"{last_form_data.get('name','')}"),
                    Text(f"Date of Birth: {last_form_data.get('dob','')}"),
                    Text(f"Gender: {last_form_data.get('gender','')}"),
                    Text(f"Address: {last_form_data.get('address','')}"),
                    Text(f"Country: {last_form_data.get('country','')}"),
                    ElevatedButton(text="Go back", on_click=go_back, bgcolor="#333333", color="white"),
                ],
                spacing=8,
                alignment="center",
            ),
        ],
        padding=20,
        vertical_alignment=MainAxisAlignment.START,
        horizontal_alignment=CrossAxisAlignment.CENTER,
    )