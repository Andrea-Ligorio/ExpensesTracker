import flet as ft
from datetime import datetime

def main(page: ft.Page):
    page.title = "Gestione Spese Personali"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.width = 450
    page.window.height = 700
    
    # Lista in memoria
    expenses = []
    expense_id_counter = 1

    # Componenti per l'inserimento
    txt_nome = ft.TextField(label="Nome spesa")
    txt_prezzo = ft.TextField(
        label="Prezzo (€)", 
        keyboard_type=ft.KeyboardType.NUMBER
    )
    txt_data = ft.TextField(
        label="Data (YYYY-MM-DD)", 
        value=datetime.now().strftime("%Y-%m-%d")
    )
    txt_note = ft.TextField(label="Note")
    txt_tags = ft.TextField(label="Tag (separati da virgola: es. cibo, svago)")

    # Lista e riepilogo
    lv_spese = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
    lbl_total = ft.Text("Totale: 0.00 €", size=20, weight=ft.FontWeight.BOLD)

    def aggiorna_vista():
        """Aggiorna la lista delle spese e il totale."""
        lv_spese.controls.clear()
        totale = 0.00
        
        for spesa in expenses:
            totale += spesa["prezzo"]
            tags_str = ", ".join(spesa["tags"])
            lv_spese.controls.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            [
                                ft.ListTile(
                                    leading=ft.Icon(ft.icons.monetization_on, color=ft.colors.GREEN),
                                    title=ft.Text(f"[{spesa['id']}] {spesa['nome']}", weight=ft.FontWeight.BOLD),
                                    subtitle=ft.Text(f"Prezzo: {spesa['prezzo']:.2f} € | Data: {spesa['data']}\nTags: {tags_str or 'Nessuno'}"),
                                ),
                                ft.Text(f"Note: {spesa['note']}", size=12, color=ft.colors.GREY, italic=True)
                            ]
                        ),
                        padding=10,
                    ),
                )
            )
        
        lbl_total.value = f"Totale complessivo: {totale:.2f} €"
        page.update()

    def salva_spesa(e):
        nonlocal expense_id_counter # Corretto qui
        try:
            nome = txt_nome.value
            if not nome or not txt_prezzo.value:
                page.show_snack_bar(
                    ft.SnackBar(content=ft.Text("Compila almeno Nome e Prezzo!"))
                )
                return
            
            prezzo = float(txt_prezzo.value)
            data = txt_data.value
            note = txt_note.value
            tags = [t.strip() for t in txt_tags.value.split(',') if t.strip()]

            spesa = {
                "id": expense_id_counter,
                "prezzo": prezzo,
                "data": data,
                "nome": nome,
                "note": note,
                "tags": tags
            }
            expenses.append(spesa)
            expense_id_counter += 1 # E corretto qui

            # Pulizia campi del dialog
            txt_nome.value = ""
            txt_prezzo.value = ""
            txt_data.value = datetime.now().strftime("%Y-%m-%d")
            txt_note.value = ""
            txt_tags.value = ""

            # Chiudi la finestra
            dlg_nuova_spesa.open = False
            aggiorna_vista()
            
            page.show_snack_bar(
                ft.SnackBar(content=ft.Text("Spesa aggiunta con successo!"))
            )
            
        except ValueError:
            page.show_snack_bar(
                ft.SnackBar(content=ft.Text("Inserisci un prezzo numerico valido!"))
            )

    def apri_dialog(e):
        page.dialog = dlg_nuova_spesa
        dlg_nuova_spesa.open = True
        page.update()

    def chiudi_dialog(e):
        dlg_nuova_spesa.open = False
        page.update()

    # Finestra di dialogo (Dialog)
    dlg_nuova_spesa = ft.AlertDialog(
        title=ft.Text("Aggiungi nuova spesa"),
        content=ft.Column(
            [
                txt_nome,
                txt_prezzo,
                txt_data,
                txt_note,
                txt_tags,
            ],
            tight=True,
            width=350,
        ),
        actions=[
            ft.TextButton("Annulla", on_click=chiudi_dialog),
            ft.ElevatedButton("Salva", on_click=salva_spesa),
        ],
    )

    # Bottone Fluttuante
    page.floating_action_button = ft.FloatingActionButton(
        icon="add",
        bgcolor=ft.colors.GREEN_ACCENT,
        on_click=apri_dialog
    )

    aggiorna_vista()

    # Aggiunta alla pagina
    page.add(
        ft.Text("Gestore Spese Personali", size=26, weight=ft.FontWeight.BOLD),
        ft.Divider(),
        lbl_total,
        lv_spese
    )

if __name__ == "__main__":
    ft.app(target=main)