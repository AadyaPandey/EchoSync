import flet as ft
import json

def load_tasks_from_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
            # Try parsing as JSON
            try:
                data = json.loads(content)
                return data.get("tasks", [])
            except json.JSONDecodeError:
                pass
            
            # If not JSON, assume it's a plain text file (one task per line)
            return [line.strip() for line in content.split("\n") if line.strip()]
    except Exception as e:
        print("Error loading file:", e)
        return []

def main(page: ft.Page):
    page.title = "To-Do List (Universal File Support)"
    page.scroll = ft.ScrollMode.AUTO
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    todo_list = ft.Column()
    task_input = ft.TextField(hint_text="Enter a task", expand=True)
    file_picker = ft.FilePicker()

    def add_task(e=None):
        if task_input.value.strip():
            task_text = task_input.value.strip()
            task = create_task_row(task_text)
            todo_list.controls.append(task)
            task_input.value = ""
            page.update()

    def create_task_row(task_text):
        checkbox = ft.Checkbox()
        task_text_display = ft.Text(task_text, expand=True)
        task_text_input = ft.TextField(value=task_text, expand=True, visible=False)

        def enable_edit(e):
            task_text_display.visible = False
            task_text_input.visible = True
            edit_button.visible = False
            save_button.visible = True
            page.update()

        def save_edit(e):
            updated_text = task_text_input.value.strip()
            if updated_text:
                task_text_display.value = updated_text
                task_text_display.visible = True
                task_text_input.visible = False
                edit_button.visible = True
                save_button.visible = False
                page.update()

        def remove_task(e):
            todo_list.controls.remove(task_row)
            page.update()

        edit_button = ft.IconButton(icon=ft.icons.EDIT, on_click=enable_edit)
        save_button = ft.IconButton(icon=ft.icons.SAVE, on_click=save_edit, visible=False)
        delete_button = ft.IconButton(icon=ft.icons.DELETE, on_click=remove_task)

        task_row = ft.Row([
            checkbox,
            task_text_display,
            task_text_input,
            edit_button,
            save_button,
            delete_button
        ])
        return task_row

    def on_file_picked(e: ft.FilePickerResultEvent):
        if e.files:
            file_path = e.files[0].path
            tasks = load_tasks_from_file(file_path)
            todo_list.controls.clear()
            for task_text in tasks:
                todo_list.controls.append(create_task_row(task_text))
            page.update()

    file_picker.on_result = on_file_picked
    load_file_button = ft.ElevatedButton("Load File", on_click=lambda _: file_picker.pick_files())

    page.overlay.append(file_picker)
    page.add(
        ft.Column([
            ft.Row([task_input, ft.ElevatedButton("Add", on_click=add_task)]),
            load_file_button,
            todo_list
        ])
    )

ft.app(target=main)
