import flet as ft
import requests


API_URL = "http://127.0.0.1:8000"
def main(page: ft.Page):
    page.bgcolor = ft.Colors.TRANSPARENT
    page.title = "BloomBuddy"
    page.scroll = "none"
    page.theme = ft.Theme(font_family="Ag Single Line/Body Small Strong")
    TEXT_COLOR = "#103F1E"

    page.decoration = ft.BoxDecoration(
        image=ft.DecorationImage(
            src="img/white.png",
            fit=ft.ImageFit.COVER
        )
    )

    page.update()

    # Panel 1 - BloomBuddy Chat
    messages = ft.ListView(expand=True, spacing=10, auto_scroll=True)

    def send_message(e):
        if user_input.value.strip() != "":
            user_msg = user_input.value.strip()
            # User's message
            messages.controls.append(
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Stack(
                                [
                                    ft.Text(
                                        user_input.value + "\n\n",
                                        color=TEXT_COLOR,
                                        no_wrap=False,
                                        selectable=True,
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.COPY,
                                        icon_color=TEXT_COLOR,
                                        icon_size=12,
                                        tooltip="Copy",
                                        on_click=lambda e, msg=user_input.value: page.set_clipboard(msg),
                                        style=ft.ButtonStyle(padding=0),
                                        right=0, 
                                        bottom=0,  
                                    ),
                                ]
                            ),
                            bgcolor="#94e48f",
                            border_radius=10,
                            padding=10,
                            margin=5,
                            width=450,
                        )

                    ],
                    alignment=ft.MainAxisAlignment.END,
                )
            )
            
            # Send message to backend API
            try:
                response = requests.post(f"{API_URL}/chat/message", json={"message": user_msg})
                reply = response.json().get("reply", "No response")
            except Exception as ex:
                reply = f"Error: {ex}"


            # Placeholder bot reply
            messages.controls.append(
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Stack(
                                [
                                    ft.Text(
                                        reply + "\n\n",
                                        color=TEXT_COLOR,
                                        no_wrap=False,
                                        selectable=True,
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.COPY,
                                        icon_color=TEXT_COLOR,
                                        icon_size=12,
                                        tooltip="Copy",
                                        on_click=lambda e, msg=reply: page.set_clipboard(msg),
                                        style=ft.ButtonStyle(padding=0),
                                        right=2,
                                        bottom=2,
                                    ),
                                ]
                            ),
                            bgcolor="#fff59d",
                            border_radius=10,
                            padding=10,
                            margin=5,
                            width=450,
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
        on_submit=send_message,
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

    # State objects for the Scan panel
    selected_file_path = None  # will store the selected file path
    selected_file_text = ft.Text("No file selected", color=TEXT_COLOR)
    image_preview = ft.Container(content=ft.Text("", color=TEXT_COLOR), width=420, height=240)
    diagnosis_text = ft.Text("Diagnose:", color=TEXT_COLOR, selectable=True)

    def pick_file_result(e: ft.FilePickerResultEvent):
        nonlocal selected_file_path
        if e.files:
            # Take the first file
            f = e.files[0]
            selected_file_path = f.path  # local file path
            selected_file_text.value = f"You have chosen: {f.name}"
            # Show image preview (if it's an image)
            try:
                image_preview.content = ft.Image(src=selected_file_path, width=420, height=240, fit=ft.ImageFit.CONTAIN)
            except Exception:
                image_preview.content = ft.Text("Preview not available", color=TEXT_COLOR)
            # TODO: you can add sending file to backend and getting diagnosis here:
            # response = requests.post(f"{API_URL}/scan", files={"file": open(selected_file_path, "rb")})
            # diagnosis = response.json().get("diagnosis", "No diagnosis")
            # diagnosis_text.value = "Diagnose: " + diagnosis
        else:
            selected_file_path = None
            selected_file_text.value = "File not selected"
            image_preview.content = ft.Text("", color=TEXT_COLOR)
            diagnosis_text.value = "Diagnose:"
        page.update()

    file_picker = ft.FilePicker(on_result=pick_file_result)
    page.overlay.append(file_picker)

    # Clear button (removes selected file and diagnosis)
    def clear_scan(e):
        nonlocal selected_file_path
        selected_file_path = None
        selected_file_text.value = "No file selected"
        image_preview.content = ft.Text("", color=TEXT_COLOR)
        diagnosis_text.value = "Diagnose:"
        page.update()

    # Top window — upload/preview area (styled like a bot message and centered)
    upload_box = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Container(  # the "bubble" of preview
                            content=ft.Stack(
                                [
                                    image_preview,  # preview (if any) or empty text
                                ]
                            ),
                            bgcolor="#94e48f",
                            border_radius=10,
                            padding=10,
                            margin=ft.margin.only(top=5, bottom=5),
                            width=500,
                            alignment=ft.alignment.center,
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [
                        ft.TextButton(
                            "Select file",
                            on_click=lambda _: file_picker.pick_files(allow_multiple=False),
                            style=ft.ButtonStyle(bgcolor="#94e48f", color=TEXT_COLOR),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [
                        selected_file_text
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            spacing=6,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor=None,
    )

    # Buttons between windows: Clear + cross
    controls_row = ft.Row(
        [
            ft.ElevatedButton("Clear", on_click=clear_scan, icon=ft.Icons.CLEAR),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    # Bottom window — diagnosis text with copy button in the corner
    def copy_diagnosis(e):
        # copy the entire string (including 'Diagnose:')
        page.set_clipboard(diagnosis_text.value)
        # can show Snackbar confirmation
        page.snack_bar = ft.SnackBar(ft.Text("Copied"), open=True)
        page.update()

    diagnosis_box = ft.Container(
        content=ft.Row(
            [
                ft.Text(diagnosis_text.value, color=TEXT_COLOR, selectable=True, expand=True),
                ft.IconButton(
                    icon=ft.Icons.COPY,
                    icon_size=16,
                    tooltip="Copy diagnosis",
                    on_click=copy_diagnosis,
                    style=ft.ButtonStyle(padding=0),
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        bgcolor="#fff59d",
        border_radius=10,
        padding=8,
        margin=ft.margin.only(top=8),
        width=500,
    )


    # Now assemble scan_tab (logo + upload_box + controls_row + diagnosis_box)
    # Text field for displaying selected file
    scan_file_label = ft.Text("No file selected", color=TEXT_COLOR)

    def pick_file_result(e: ft.FilePickerResultEvent):
        if e.files:
            scan_file_label.value = f"File selected: {e.files[0].name}"
            # Here you can add code to process the file and display diagnosis
            diagnosis_text.value = "Diagnose: ..."  # example, can update later
        else:
            scan_file_label.value = "No file selected"
            diagnosis_text.value = "Diagnose: "
        page.update()

    file_picker = ft.FilePicker(on_result=pick_file_result)
    page.overlay.append(file_picker)

    def clear_scan():
        scan_file_label.value = "No file selected"
        diagnosis_text.value = "Diagnose: "
        page.update()

    def copy_diagnosis(e):
        page.set_clipboard(diagnosis_text.value)

    # Container for diagnosis text
    diagnosis_text = ft.Text("Diagnose: ", color=TEXT_COLOR, selectable=True)

    # The scanner block itself
    scan_tab = ft.Column(
        [
            # Top block file upload with logo in the background
            ft.Container(
                content=ft.Stack(
                    [
                        # Logo in the background
                        ft.Container(
                            ft.Image(src="img/logo.png", width=150, height=150, opacity=0.2),
                            expand=True,
                            alignment=ft.alignment.center,
                        ),
                        # File select button and text
                        ft.Column(
                            [
                                ft.Text("Upload a photo of the plant:", size=16, color=TEXT_COLOR),
                                ft.Row(
                                    [
                                        ft.ElevatedButton(
                                            "Select file",
                                            on_click=lambda _: file_picker.pick_files(allow_multiple=False),
                                            style=ft.ButtonStyle(bgcolor="#94e48f", color=TEXT_COLOR),
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                    ],
                    expand=True
                ),
                bgcolor="#fff59d",
                border_radius=10,
                padding=20,
                width=500,
                height=180,
                margin=ft.margin.only(bottom=5),
            ),

            # Text with selected file
            scan_file_label,

            # Clear button
            ft.Row(
                [
                    ft.ElevatedButton(
                        "Clear",
                        icon=ft.Icons.CLEAR,
                        on_click=lambda _: clear_scan(),
                        style=ft.ButtonStyle(bgcolor="#f28b82", color="white"),
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10,
            ),

            # Diagnosis block
            ft.Container(
                content=ft.Row(
                    [
                        ft.Text(diagnosis_text.value, color=TEXT_COLOR, selectable=True, expand=True),
                        ft.IconButton(
                            icon=ft.Icons.COPY,
                            icon_size=16,
                            tooltip="Copy diagnosis",
                            on_click=copy_diagnosis,
                            style=ft.ButtonStyle(padding=0),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                bgcolor="#fff59d",
                border_radius=10,
                padding=8,
                width=500,
            ),
        ],
        expand=True,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )



    # Panel 3 - Settings
    def toggle_theme(e):
        if theme_switch.value:
            # Dark theme
            page.decoration = ft.BoxDecoration(
                image=ft.DecorationImage(
                    src="img/dark.png",
                    fit=ft.ImageFit.COVER
                )
            )
        else:
            # Light theme
            page.decoration = ft.BoxDecoration(
                image=ft.DecorationImage(
                    src="img/white.png",
                    fit=ft.ImageFit.COVER
                )
            )
        page.update()

    theme_switch = ft.Switch(
        label="Dark theme",
        label_style=ft.TextStyle(color=TEXT_COLOR),
        on_change=toggle_theme
    )


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
        padding=15,
        border_radius=10,
    )

    page.add(
        ft.Row(
            [app_container],
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True,
        )
    )


ft.app(target=main)
