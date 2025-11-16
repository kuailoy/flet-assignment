import flet as ft
from encryption import encrypt_message, decrypt_message

def main(page: ft.Page):
    page.title = "Encrypted Chat"

    def on_message(msg):
        parts = msg.split(":", 1)
        if len(parts) == 2:
            topic, encrypted_msg = parts
            if topic == current_topic.value:
                decrypted_msg = decrypt_message(encrypted_msg, passphrase.value)

                if decrypted_msg.startswith("[Unable to decrypt"):
                    messages.controls.append(ft.Text(f"[Encrypted message - wrong passphrase?]", color=ft.Colors.RED))
                else:
                    messages.controls.append(ft.Text(decrypted_msg))

                page.update()

    page.pubsub.subscribe(on_message)

    def send_click(e):
        if passphrase.value and message.value:
            encrypted_msg = encrypt_message(f"{user.value}: {message.value}", passphrase.value)
            page.pubsub.send_all(f"{current_topic.value}:{encrypted_msg}")
            message.value = ""
            page.update()

    # UI components
    user = ft.TextField(hint_text="Your name", width=150)
    passphrase = ft.TextField(hint_text="Passphrase", width=200)

    current_topic = ft.Dropdown(
        width=150,
        options=[
            ft.dropdown.Option("general"),
            ft.dropdown.Option("private"),
            ft.dropdown.Option("work"),
        ],
        value="general"
    )

    message = ft.TextField(hint_text="Your message...", expand=True)
    send = ft.ElevatedButton("Send", on_click=send_click)

    messages = ft.Column()

    page.add(
        ft.Row([user, passphrase, current_topic]),
        messages,
        ft.Row([message, send])
    )

ft.app(main, view=ft.AppView.WEB_BROWSER)