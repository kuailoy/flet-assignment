import flet as ft
from datetime import datetime
from typing import List, Dict

CATEGORIES = ["Food", "Transport", "Utilities", "Entertainment"]


def main(page: ft.Page):
    page.title = "Daily Expenses"
    page.padding = 16
    page.window_width = 900
    page.vertical_alignment = ft.MainAxisAlignment.START

    # State
    expenses: List[Dict] = []  # list of dicts: {ts, category, desc, amount}

    # --- UI controls: form ---
    # Some Flet versions don't have Autocomplete or use a different signature.
    # To avoid compatibility issues, use Dropdown which works reliably across versions.
    category_dd = ft.Dropdown(
        width=240,
        hint_text="Category",
        options=[ft.dropdown.Option(c) for c in CATEGORIES],
    )

    desc_tf = ft.TextField(hint_text="Description (optional)", width=320)

    amount_tf = ft.TextField(
        hint_text="Amount",
        width=140,
        keyboard_type=ft.KeyboardType.NUMBER,
    )

    add_btn = ft.ElevatedButton("Add", icon=ft.Icons.ADD)

    status_txt = ft.Text("", color=ft.Colors.RED)

    # --- DataTable (entries) ---
    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Time")),
            ft.DataColumn(ft.Text("Category")),
            ft.DataColumn(ft.Text("Description")),
            ft.DataColumn(ft.Text("Amount")),
        ],
        rows=[],
        heading_row_color=ft.Colors.BLUE_50,
        data_row_min_height=36,
        column_spacing=20,
    )

    table_container = ft.Container(
        content=table,
        height=320,
        padding=ft.padding.all(8),
        bgcolor=ft.Colors.with_opacity(0.03, ft.Colors.BLUE_GREY),
        border_radius=8,
        expand=True,
    )

    # --- Pie chart initialization ---
    def make_pie_segments(totals: Dict[str, float]):
        colors = {
            "Food": ft.Colors.GREEN,
            "Transport": ft.Colors.BLUE,
            "Utilities": ft.Colors.ORANGE,
            "Entertainment": ft.Colors.PINK,
        }
        segs = []
        for c in CATEGORIES:
            segs.append(
                ft.PieChartSection(
                    value=totals.get(c, 0.0),
                    title=f"{c}\n${totals.get(c,0):.2f}",
                    color=colors.get(c, ft.Colors.GREY),
                    radius=100,
                )
            )
        return segs

    totals = {c: 0.0 for c in CATEGORIES}

    pie = ft.PieChart(
        sections=make_pie_segments(totals),
        expand=True,
    )

    totals_text = ft.Text(value="Total: $0.00", weight=ft.FontWeight.BOLD)

    # --- update functions ---
    def update_totals_and_pie():
        nonlocal totals
        totals = {c: 0.0 for c in CATEGORIES}
        for e in expenses:
            totals[e["category"]] += e["amount"]
        pie.sections = make_pie_segments(totals)
        totals_text.value = f"Total: ${sum(totals.values()):.2f}"
        pie.update()
        totals_text.update()

    def add_row_to_table(entry):
        # Insert newest at top
        table.rows.insert(
            0,
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(entry["ts"])),
                    ft.DataCell(ft.Text(entry["category"])),
                    ft.DataCell(ft.Text(entry["desc"])),
                    ft.DataCell(ft.Text(f"${entry['amount']:.2f}")),
                ]
            )
        )
        # keep table reasonable
        if len(table.rows) > 200:
            table.rows.pop()
        table.update()

    # --- form submit handler ---
    def on_add(e):
        status_txt.value = ""
        cat = category_dd.value if category_dd.value else ""
        desc = desc_tf.value.strip() if desc_tf.value else ""
        amt_raw = amount_tf.value.strip() if amount_tf.value else ""

        # Basic validation
        if not cat:
            status_txt.value = "Please choose a category."
            status_txt.color = ft.Colors.RED
            status_txt.update()
            return
        if cat not in CATEGORIES:
            status_txt.value = f"Unknown category. Choose one of: {', '.join(CATEGORIES)}"
            status_txt.color = ft.Colors.RED
            status_txt.update()
            return
        try:
            amt = float(amt_raw)
            if amt <= 0:
                raise ValueError()
        except Exception:
            status_txt.value = "Please enter a valid positive amount."
            status_txt.color = ft.Colors.RED
            status_txt.update()
            return

        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = {"ts": ts, "category": cat, "desc": desc, "amount": amt}
        expenses.append(entry)

        add_row_to_table(entry)
        update_totals_and_pie()

        # reset form
        category_dd.value = None
        desc_tf.value = ""
        amount_tf.value = ""
        category_dd.update()
        desc_tf.update()
        amount_tf.update()

        status_txt.value = "Added."
        status_txt.color = ft.Colors.GREEN
        status_txt.update()

    add_btn.on_click = on_add

    # Shortcut: press Enter in amount field to submit
    def on_amount_enter(e):
        on_add(e)

    amount_tf.on_submit = on_amount_enter

    # --- layout ---
    form_row = ft.Row(
        controls=[
            category_dd,
            desc_tf,
            amount_tf,
            add_btn,
            status_txt,
        ],
        alignment=ft.MainAxisAlignment.START,
        spacing=12,
        wrap=True,
    )

    left_col = ft.Column(
        [
            ft.Text("Add daily expense", size=18, weight=ft.FontWeight.BOLD),
            form_row,
            ft.Text("Entries", size=16, weight=ft.FontWeight.W_600),
            table_container,
        ],
        spacing=12,
        expand=2,
    )

    right_col = ft.Column(
        [
            ft.Text("Expenses share", size=18, weight=ft.FontWeight.BOLD),
            ft.Container(content=pie, height=360, padding=8),
            totals_text,
        ],
        spacing=12,
        expand=1,
    )

    page.add(ft.Row([left_col, right_col], expand=True, spacing=20))
    page.update()


if __name__ == "__main__":
    ft.app(target=main)