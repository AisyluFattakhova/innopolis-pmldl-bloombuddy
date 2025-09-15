import flet as ft


def main(page: ft.Page):
    page.bgcolor = ft.Colors.TRANSPARENT
    page.title = "BloomBuddy"
    page.scroll = "none"
    page.theme = ft.Theme(font_family="Ag Single Line/Body Small Strong")
    TEXT_COLOR = "#103F1E"

    page.decoration = ft.BoxDecoration(
        image=ft.DecorationImage(
            src="img\petals.jpg",
            fit=ft.ImageFit.COVER
        )
    )

    page.update()

    # Panel 1 - BloomBuddy Chat
    messages = ft.ListView(expand=True, spacing=10, auto_scroll=True)

    def send_message(e):
        if user_input.value.strip() != "":
            # User's message
            messages.controls.append(
                ft.Row(
                    [
                        ft.Container(
                            ft.Text(user_input.value, color=TEXT_COLOR),
                            bgcolor="#94e48f",
                            border_radius=10,
                            padding=10,
                            margin=5,
                        )
                    ],
                    alignment=ft.MainAxisAlignment.END,
                )
            )

            # Placeholder bot reply
            messages.controls.append(
                ft.Row(
                    [
                        ft.Container(
                            ft.Text("Message accepted 🌱", color=TEXT_COLOR),
                            bgcolor="#fff59d",
                            border_radius=10,
                            padding=10,
                            margin=5,
                        )
                    ],
                    alignment=ft.MainAxisAlignment.START,
                )
            )

            user_input.value = ""
            page.update()

    user_input = ft.TextField(
        hint_text="Type your message...",
        expand=True,
        bgcolor="white",
        border_radius=10,
        color=TEXT_COLOR,
    )

    chat_tab = ft.Column(
        [
            messages,
            ft.Container(
                content=ft.Row(
                    [
                        user_input,
                        ft.ElevatedButton(
                            "Send",
                            on_click=send_message,
                            style=ft.ButtonStyle(
                                bgcolor="#94e48f", color=TEXT_COLOR)
                        ),
                    ],
                ),
                bgcolor="#b2f085",
                border_radius=10,
                padding=10,
            ),
        ],
        expand=True,
    )

    # Panel 2 - Scan
    def pick_file_result(e: ft.FilePickerResultEvent):
        if e.files:
            scan_output.value = f"You have chosen: {e.files[0].name}"
        else:
            scan_output.value = "File not selected"
        page.update()

    file_picker = ft.FilePicker(on_result=pick_file_result)
    page.overlay.append(file_picker)

    scan_output = ft.Text("The selected file will be here", color=TEXT_COLOR)
    scan_tab = ft.Column(
        [
            ft.Text("Upload a photo of the plant:", size=16, color=TEXT_COLOR),
            ft.Row(
                [
                    ft.ElevatedButton(
                        "Select file",
                        on_click=lambda _: file_picker.pick_files(
                            allow_multiple=False),
                        style=ft.ButtonStyle(
                            bgcolor="#94e48f", color=TEXT_COLOR),
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            scan_output,
        ],
        expand=True,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # Panel 3 - Settings
    theme_switch = ft.Switch(
        label="Dark theme", label_style=ft.TextStyle(color=TEXT_COLOR))

    settings_tab = ft.Column(
        [
            ft.Text("Settings:", size=16, color=TEXT_COLOR),
            theme_switch,
            ft.Text("Font size:", color=TEXT_COLOR),
            ft.Slider(min=10, max=30, divisions=20, label="{value}"),
        ],
        expand=True,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    selected_tab = "chat"

    def change_tab(e):
        nonlocal selected_tab
        selected_tab = e.control.data

        content.controls.clear()
        if selected_tab == "chat":
            content.controls.append(chat_tab)
        elif selected_tab == "scan":
            content.controls.append(scan_tab)
        elif selected_tab == "settings":
            content.controls.append(settings_tab)

        for c in header.content.controls:
            if getattr(c, "data", None) == selected_tab:
                c.bgcolor = "#fff59d"
            else:
                c.bgcolor = None
        page.update()

    def make_tab_box(label: str, icon, data_id: str):
        return ft.Container(
            data=data_id,
            expand=True,
            padding=10,
            border_radius=8,
            content=ft.Row(
                [
                    ft.Icon(icon, size=18, color=TEXT_COLOR),
                    ft.Text(label, color=TEXT_COLOR, size=14),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=8,
            ),
            on_click=change_tab
        )

    header = ft.Container(
        content=ft.Row(
            [
                make_tab_box("BloomBuddy", ft.Icons.CHAT, "chat"),
                make_tab_box("Scan", ft.Icons.CAMERA_ALT, "scan"),
                make_tab_box("Settings", ft.Icons.SETTINGS, "settings"),
            ],
            expand=True,
            spacing=0,
        ),

        padding=0,
    )

    for c in header.content.controls:
        if getattr(c, "data", None) == selected_tab:
            c.bgcolor = "#fff59d"

    # Main content area
    content = ft.Column([chat_tab], expand=True)

    # App container
    app_container = ft.Container(
        content=ft.Column(
            [header, content],
            expand=True,
        ),
        bgcolor="#c7ffa4",
        width=600,
        margin=ft.margin.symmetric(horizontal=20, vertical=20),
        padding=10,
        border_radius=15,
    )

    page.add(
        ft.Row(
            [app_container],
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True,
        )
    )


ft.app(target=main)


