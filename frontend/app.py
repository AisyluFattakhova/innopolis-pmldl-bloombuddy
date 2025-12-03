import flet as ft
import requests
import os
import sys
import logging
logging.basicConfig(level=logging.DEBUG)

if getattr(sys, 'frozen', False):
    os.environ["FLET_FORCE_RESTART"] = "0"


if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

IMG_DIR = os.path.join(BASE_DIR, "frontend", "img")


API_URL = "http://127.0.0.1:8000"
def main(page: ft.Page):
    page.bgcolor = ft.Colors.TRANSPARENT
    page.title = "BloomBuddy"
    page.scroll = "none"
    page.theme = ft.Theme(font_family="Ag Single Line/Body Small Strong")
    TEXT_COLOR = "#103F1E"

    page.decoration = ft.BoxDecoration(
        image=ft.DecorationImage(
            src=os.path.join(IMG_DIR, "white.png"),
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


    # Now assemble scan_tab (logo + upload_box + controls_row + diagnosis_box)
    # Text field for displaying selected file
    scan_file_label = ft.Text("No file selected", color=TEXT_COLOR)

    def pick_file_result(e: ft.FilePickerResultEvent):
        if e.files:
            scan_file_label.value = f"File selected: {e.files[0].name}"

            try:
                # Getting bytes directly (not via path!)
                file_path = e.files[0].path
                with open(file_path, "rb") as f:
                    file_bytes = f.read()


                response = requests.post(
                    f"{API_URL}/scan/analyze",
                    files={"file": ("image.jpg", file_bytes, "image/jpeg")}
                )

                data = response.json()

                if data.get("status") == "error":
                    diagnosis_text.value = "Diagnose: " + data.get("result")
                else:
                    text = data.get("result", "")
                    if data.get("treatment_advice"):
                        text += "\n\n" + data.get("treatment_advice") + "\n"
                    diagnosis_text.value = "Diagnose: " + text

            except Exception as ex:
                diagnosis_text.value = f"Diagnose: Error — {ex}"

        else:
            scan_file_label.value = "No file selected"
            diagnosis_text.value = "Diagnose: \n"

        page.update()


    file_picker = ft.FilePicker(on_result=pick_file_result)
    page.overlay.append(file_picker)

    def clear_scan():
        scan_file_label.value = "No file selected"
        diagnosis_text.value = "Diagnose: \n"
        page.update()

    def copy_diagnosis(e):
        page.set_clipboard(diagnosis_text.value)

    # Container for diagnosis text
    diagnosis_text = ft.Text("Diagnose: \n", color=TEXT_COLOR, selectable=True)

    # The scanner block itself
    scan_tab = ft.Column(
        [
            # Top block file upload with logo in the background
            ft.Container(
                content=ft.Stack(
                    [
                        # Logo in the background
                        ft.Container(
                            ft.Image(src=os.path.join(IMG_DIR, "logo.png"), width=100, height=100, opacity=0.2),
                            expand=True,
                            alignment=ft.alignment.center,
                        ),
                        # File select button and text
                        ft.Column(
                            [
                                ft.Text("Upload a photo of the plant:", color=TEXT_COLOR),
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
                padding=10,
                width=500,
                height=120,
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
                content=ft.Stack(
                    [
                        diagnosis_text,
                        ft.IconButton(
                            icon=ft.Icons.COPY,
                            icon_size=16,
                            tooltip="Copy diagnosis",
                            on_click=copy_diagnosis,
                            style=ft.ButtonStyle(padding=0),
                            right=0,
                            bottom=0,
                        ),
                    ]
                ),
                bgcolor="#fff59d",
                border_radius=10,
                padding=10,
                width=500,
            ),

        ],
        expand=True,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )



    # Callback for Dark mode
    def toggle_theme(e):
        if e.control.value:  # if switch is ON
            # Dark theme
            page.decoration = ft.BoxDecoration(
                image=ft.DecorationImage(
                    src=os.path.join(IMG_DIR, "dark.png"),
                    fit=ft.ImageFit.COVER
                )
            )
        else:
            # Light theme
            page.decoration = ft.BoxDecoration(
                image=ft.DecorationImage(
                    src=os.path.join(IMG_DIR, "white.png"),
                    fit=ft.ImageFit.COVER
                )
            )
        page.update()

    # Callback for Large font
    def toggle_font_size(e):
        if e.control.value:  # Large font ON
            font_size_body = 20
            font_size_label = 19
            font_size_title = 22
            button_font_size = 19
        else:  # Large font OFF
            font_size_body = 16
            font_size_label = 15
            font_size_title = 17
            button_font_size = 15

        page.theme = ft.Theme(
            font_family="Ag Single Line/Body Small Strong",
            text_theme=ft.TextTheme(
                body_large=ft.TextStyle(size=font_size_body),
                body_medium=ft.TextStyle(size=font_size_body),
                body_small=ft.TextStyle(size=font_size_body),
                title_large=ft.TextStyle(size=font_size_title),
                title_medium=ft.TextStyle(size=font_size_title),
                title_small=ft.TextStyle(size=font_size_title),
                label_large=ft.TextStyle(size=font_size_label),
                label_medium=ft.TextStyle(size=font_size_label),
                label_small=ft.TextStyle(size=font_size_label),
            ),
        )

        def update_button_font(control):
            if isinstance(control, ft.ElevatedButton):
                control.style = ft.ButtonStyle(
                    bgcolor=control.style.bgcolor if control.style else None,
                    color=control.style.color if control.style else None,
                    text_style=ft.TextStyle(size=button_font_size)
                )
            if hasattr(control, "content") and isinstance(control.content, (ft.Column, ft.Row)):
                for c in control.content.controls:
                    update_button_font(c)

        
        for tab in [chat_tab, scan_tab, settings_tab]:
            update_button_font(tab)

        page.update()



    # Callback for the button About us
    def open_github(e):
        import webbrowser
        webbrowser.open("https://github.com/AisyluFattakhova/innopolis-pmldl-bloombuddy/tree/main")

    settings_tab = ft.Column(
        [
            ft.Row( 
                [
                    ft.Container(
                        content=ft.Column(
                            [
                                # Dark mode
                                ft.Row(
                                    [
                                        ft.Row(
                                            [
                                                ft.Icon(ft.Icons.DARK_MODE, color=TEXT_COLOR),
                                                ft.Text("Dark mode", color=TEXT_COLOR),
                                            ],
                                            spacing=8,
                                        ),
                                        ft.Switch(
                                            value=False,
                                            on_change=toggle_theme,
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                ),
                                # Large font
                                ft.Row(
                                    [
                                        ft.Row(
                                            [
                                                ft.Icon(ft.Icons.REMOVE_RED_EYE, color=TEXT_COLOR),
                                                ft.Text("Large font", color=TEXT_COLOR),
                                            ],
                                            spacing=8,
                                        ),
                                        ft.Switch(
                                            value=False,
                                            on_change=toggle_font_size,
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                ),
                            ],
                            spacing=15,
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        bgcolor="#fff59d",
                        border_radius=10,
                        padding=20,
                        width=400,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),

            ft.Container(  
                ft.ElevatedButton(
                    "About us",
                    icon=ft.Icons.INFO,
                    on_click=open_github,
                    style=ft.ButtonStyle(
                        bgcolor="#94e48f",
                        color=TEXT_COLOR,
                    ),
                ),
                alignment=ft.alignment.center,
                margin=ft.margin.only(top=10),  
            ),
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
                    ft.Text(label, color=TEXT_COLOR, size=16),
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
