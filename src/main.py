import flet as ft
import datetime

def main(page: ft.Page):
    page.title = "Lista Pagamenti"
    page.theme_mode = ft.ThemeMode.SYSTEM
    page.window.width = 480
    page.window.height = 854
    page.padding = 15

    budgetResiduo = 1234.56

    pagamenti = [
    {"id": 1, "destinatario": "Amazon", "importo": "€ 45.99", "data": "12/05/2026", "stato": "Completato"},
    {"id": 2, "destinatario": "Netflix", "importo": "€ 12.99", "data": "10/05/2026", "stato": "Completato"},
    {"id": 3, "destinatario": "Supermercato", "importo": "€ 85.50", "data": "08/05/2026", "stato": "In sospeso"},
    {"id": 4, "destinatario": "Bolletta Luce", "importo": "€ 112.45", "data": "05/05/2026", "stato": "Completato"},
    {"id": 5, "destinatario": "Abbonamento Palestra", "importo": "€ 35.00", "data": "01/05/2026", "stato": "Non riuscito"},
    {"id": 6, "destinatario": "Abbonamento Palestra", "importo": "€ 35.00", "data": "01/05/2026", "stato": "Non riuscito"},
    {"id": 7, "destinatario": "Abbonamento Palestra", "importo": "€ 35.00", "data": "01/05/2026", "stato": "Non riuscito"},
    {"id": 8, "destinatario": "Abbonamento Palestra", "importo": "€ 35.00", "data": "01/05/2026", "stato": "Non riuscito"},
    {"id": 9, "destinatario": "Abbonamento Palestra", "importo": "€ 35.00", "data": "01/05/2026", "stato": "Non riuscito"},
    {"id": 10, "destinatario": "Abbonamento Palestra", "importo": "€ 35.00", "data": "01/05/2026", "stato": "Non riuscito"},
    {"id": 11, "destinatario": "Abbonamento Palestra", "importo": "€ 35.00", "data": "01/05/2026", "stato": "Non riuscito"},
    {"id": 12, "destinatario": "Abbonamento Palestra", "importo": "€ 35.00", "data": "01/05/2026", "stato": "Non riuscito"},
    {"id": 13, "destinatario": "Abbonamento Palestra", "importo": "€ 35.00", "data": "01/05/2026", "stato": "Non riuscito"},
    {"id": 14, "destinatario": "Abbonamento Palestra", "importo": "€ 35.00", "data": "01/05/2026", "stato": "Non riuscito"},
    {"id": 15, "destinatario": "Abbonamento Palestra", "importo": "€ 35.00", "data": "01/05/2026", "stato": "Non riuscito"},
    ]

    remainingBudget = ft.Column(
        [
            ft.Text("Budget residuo:",size=15),
            ft.Text(
                f"€{budgetResiduo:.2f}",
                size=80,
                weight=ft.FontWeight.BOLD
            )
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        tight=True,
    )

    oggi = datetime.datetime.now()

    def aggiornaDataText(e):
        print(calendar.value)
        dateTextField.value = (calendar.value + datetime.timedelta(hours=9)).strftime("%d/%m/%Y")
        page.update()

    calendar = ft.DatePicker(
        value=oggi,
        first_date=oggi - datetime.timedelta(days=365*50),
        last_date=oggi + datetime.timedelta(days=365*50),
        on_change=aggiornaDataText
    )

    dateTextField = ft.TextField(
        label="Date",
        value=calendar.value.strftime("%d/%m/%Y"),
        read_only=True,
        on_click=lambda e: page.show_dialog(calendar)
    )

    def saveDb():
        nome = nameTextField.value.strip()
        prezzo = priceTextField.value
        if nome == 0 or prezzo == 0:
            return
        elemento = {}
        tagsStr = tagTextField.value.strip()
        if tagsStr != "":
            tags = []
            for tag in tagsStr.split(","):
                tag = tag.strip()
                if tag != "":
                    tags.append(tag)
        

        

    nameTextField = ft.TextField(label="Name",max_lines=1,)
    priceTextField = ft.TextField(
        label="Price",
        max_lines=1,
        prefix="€ ",
        keyboard_type=ft.KeyboardType.NUMBER,
        input_filter=ft.InputFilter(
            allow=True, 
            regex_string=r"^[0-9]*[.]?[0-9]{0,2}$", 
            replacement_string=""
        ),
    )
    tagTextField = ft.TextField(label="Tags (separati da [,])",multiline=True)
    noteTextField = ft.TextField(label="Note",multiline=True)
    confirmButton = ft.IconButton(
        icon=ft.icons.Icons.ADD,
        width=200,
        bgcolor=ft.Colors.GREY_800,
        #on_click=saveDb,
    )

        


    addPayment = ft.Container(
        ft.Column(
            [
                ft.Text("Nuovo elemento", size=30, weight=ft.FontWeight.BOLD),
                ft.ListView(
                    [
                        nameTextField,
                        priceTextField,
                        dateTextField,
                        tagTextField,
                        noteTextField,
                        confirmButton
                    ],
                    auto_scroll=True,
                    spacing=20,
                    expand=True,
                    padding=35,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        alignment=ft.Alignment.CENTER,
        expand=True,
        padding=5,
    ) 
    


    def apriAdd(e):
            pagina.content = addPayment
            page.update()


    toolBar = ft.Row(
        [
            ft.IconButton(
                icon=ft.icons.Icons.FILTER_ALT,
                bgcolor=ft.Colors.GREY_800,
                width=100
            ),
            ft.IconButton(
                icon=ft.icons.Icons.ADD_CIRCLE_OUTLINE,
                bgcolor=ft.Colors.GREY_800,
                width=100,
                on_click=apriAdd
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=100,
    )

    lista_pagamenti = ft.ListView(expand=1, spacing=12, padding=5, auto_scroll=True)

    for p in pagamenti:
            
        lista_pagamenti.controls.append(
                ft.ListTile(
                    title=ft.Text(p["destinatario"], weight=ft.FontWeight.BOLD),
                    subtitle=ft.Text(f"Data: {p['data']}"),
                    trailing=ft.Text(p["importo"], weight=ft.FontWeight.BOLD, size=15),
                ) 
        )
        lista_pagamenti.controls.append(ft.Divider(height=1))
        
    home = ft.Container(
        ft.Column(
            [
                remainingBudget,
                ft.Divider(height=1),
                toolBar,
                ft.Divider(height=1),
                lista_pagamenti,
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        expand=True,
    )
    
    pagina = ft.Container(expand=True)
    pagina.content = home


    def cambiaPagina(e):
        i=e.control.selected_index
        if i==0:
            pagina.content = home
        elif i==1:
            #pagina.content = addPayment
            print("apri chart")
        elif i==2:
            #pagina = settings
            print("apri settings")
        page.update()

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.icons.Icons.HOUSE, label="Home",),
            ft.NavigationBarDestination(icon=ft.icons.Icons.STACKED_LINE_CHART, label="Pagamenti"),
            ft.NavigationBarDestination(icon=ft.icons.Icons.SETTINGS, label="negro"),
        ],
        selected_index=0,
        on_change=cambiaPagina,
    )
        
    
    
    


    # Aggiunta degli elementi alla pagina
    page.add(
        ft.Row(
            [
            ft.Text(
                "ExpensesTracker",
                size=20, 
                weight=ft.FontWeight.BOLD
            )
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        ft.Divider(height=1),
        pagina,
    )


    
    

        


if __name__ == "__main__":
    ft.run(main)