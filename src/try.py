import flet as ft

def main(page: ft.Page):
    
    page.add(ft.ListView(controls=[ft.Text(f"Item {i}") for i in range(1, 60)]))

ft.run(main)