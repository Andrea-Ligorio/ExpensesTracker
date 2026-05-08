import flet as ft
import datetime
import Spesa
import expensesDatabase

def main(page: ft.Page):
    page.title = "Lista Pagamenti"
    page.theme_mode = ft.ThemeMode.SYSTEM
    page.window.width = 480
    page.window.height = 854
    page.padding = 15

    expensesDatabase.creaDb()
    budget = 500 

    def remainingBudget():
        CurrentMonth = datetime.datetime.now().month
        spese = expensesDatabase.getSpese()
        speso = 0
        for s in spese:
            if(datetime.datetime.strptime(s.data, "%d/%m/%Y").month == CurrentMonth):
                speso+=float(s.prezzo)
        budgetResiduo = budget - speso

        return ft.Column(
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

    def addPayment():
        def saveDb():
            nome = nameTextField.value.strip()
            if nome == "":
                print("manca qualcosa")
                return
            prezzo = priceTextField.value
            if prezzo == "":
                prezzo = "0"
            spesa = Spesa.Spesa(nome, prezzo, dateTextField.value, noteTextField.value, tagTextField.value)
            expensesDatabase.insertSpesa(spesa)
            pagina.content = home()
            page.update()
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
            on_click=saveDb,
        )

        return ft.Container(
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
    
    def toolBar():
        def apriAdd(e):
            pagina.content = addPayment()
            page.update()
        return ft.Row(
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

    def lista_pagamenti():
        #def spesaView:
            
        speseView = ft.ListView(expand=1, spacing=12, padding=5, auto_scroll=True)

        spese = expensesDatabase.getSpese()

        for p in spese:
            speseView.controls.append(
                ft.ListTile(
                    title=ft.Text(p.nome, weight=ft.FontWeight.BOLD),
                    subtitle=ft.Text(f"Data: {p.data}"),
                    trailing=ft.Text(f"€ {p.prezzo:.2f}", weight=ft.FontWeight.BOLD, size=15),
                    #on_click= apri spesa
                ) 
            )
            speseView.controls.append(ft.Divider(height=1))

        return speseView

    
        
    def home():
        return ft.Container(
            ft.Column(
                [
                    remainingBudget(),
                    ft.Divider(height=1),
                    toolBar(),
                    ft.Divider(height=1),
                    lista_pagamenti(),
                ],
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            expand=True,
        )
    
    pagina = ft.Container(expand=True)
    pagina.content = home()


    def cambiaPagina(e):
        i=e.control.selected_index
        if i==0:
            pagina.content = home()
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