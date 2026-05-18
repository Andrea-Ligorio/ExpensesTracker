import flet as ft
import datetime
import Spesa
import expensesDatabase

def main(page: ft.Page):
    page.title = "ExpensesTracker"
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width = 480
    page.window.height = 854
    page.padding = 15

    expensesDatabase.creaDb()
    budget = 0
    settingsFilePath = "settingsExpensesTracker.txt"

    searchKey = ""
    speseSorted = expensesDatabase.getSpese()

    try:
        with open(settingsFilePath, "r") as f:
            budget = float(f.read().strip())
    except:
        print("file non trovato")

    oggi = datetime.datetime.now()
    def apriAdd(e, payment, rdOy):
        pagina.content = addPayment(payment, rdOy)
        page.update()
    def addPayment(payment, rdOy):
        def saveDb(edit):
            nome = nameTextField.value.strip()
            if nome == "":
                print("manca qualcosa")
                return
            prezzo = priceTextField.value
            if prezzo == "":
                prezzo = "0"
            spesa = Spesa.Spesa(nome, prezzo, dateTextField.value, noteTextField.value, tagTextField.value, payment.id if edit else None)
            if edit:
                expensesDatabase.editSpesa(spesa)
            else:
                expensesDatabase.insertSpesa(spesa)
            
            updateList()
        def deleteDb():
            expensesDatabase.deleteSpesa(payment.id)
            updateList()
        def aggiornaDataText(e):
            print(calendar.value)
            dateTextField.value = (calendar.value + datetime.timedelta(hours=9)).strftime("%d/%m/%Y")
            page.update()
        calendar = ft.DatePicker(
            value= oggi if payment == None else datetime.datetime.strptime(payment.data, "%d/%m/%Y"),
            first_date=oggi - datetime.timedelta(days=365*50),
            last_date=oggi + datetime.timedelta(days=365*50),
            on_change=aggiornaDataText,
        )
        dateTextField = ft.TextField(
            label="Date",
            value=calendar.value.strftime("%d/%m/%Y"),
            read_only=rdOy,
            on_click=lambda e: page.show_dialog(calendar) if not rdOy else None,
        )
        nameTextField = ft.TextField(
            label="Name",
            value="" if payment == None else payment.nome,
            max_lines=1,
            read_only=rdOy
        )
        priceTextField = ft.TextField(
            label="Price",
            max_lines=1,
            read_only=rdOy,
            value="" if payment == None else payment.prezzo,
            prefix="€ ",
            keyboard_type=ft.KeyboardType.NUMBER,
            input_filter=ft.InputFilter(
                allow=True, 
                regex_string=r"^[0-9]*[.]?[0-9]{0,2}$", 
                replacement_string=""
            ),
        )
        tagTextField = ft.TextField(
            label="Tags (separati da [,])",
            multiline=True,
            value="" if payment == None else ", ".join(payment.tag),
            read_only=rdOy,
        )
        noteTextField = ft.TextField(
            label="Note",
            read_only=rdOy,
            value="" if payment == None else payment.note,
            multiline=True
        )
        confirmButton = ft.IconButton(
            icon=ft.icons.Icons.EDIT if rdOy else ft.icons.Icons.ADD if payment == None else ft.icons.Icons.CHECK,
            width=200,
            bgcolor=ft.Colors.GREY_800,
            on_click=lambda e: saveDb(False) if payment == None else apriAdd(e, payment, False) if rdOy else saveDb(True),
        )
        deleteButton = ft.IconButton(
            icon=ft.icons.Icons.DELETE,
            width=200,
            bgcolor=ft.Colors.GREY_800,
            on_click=deleteDb,
            disabled= not rdOy,
            visible= rdOy,
        )

        return ft.Container(
            ft.Column(
                [
                    ft.Text("Nuovo elemento" if payment == None else "Visualizza elemento" if rdOy else "Modifica elemento", size=30, weight=ft.FontWeight.BOLD),
                    ft.ListView(
                        [
                            nameTextField,
                            priceTextField,
                            dateTextField,
                            tagTextField,
                            noteTextField,
                            confirmButton,
                            deleteButton
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

    def settings():
        def updateBudget(e):
            nonlocal budget
            budget = float(budgetTextField.value) if budgetTextField.value != "" else 0
            with open(settingsFilePath, "w") as f:
                f.write(str(budget))

        budgetTextField = ft.TextField(
            value=budget,
            label="Budget mensile",
            prefix="€ ",
            keyboard_type=ft.KeyboardType.NUMBER,
            input_filter=ft.InputFilter(
                allow=True, 
                regex_string=r"^[0-9]*[.]?[0-9]{0,2}$", 
                replacement_string=""
            ),
            max_lines=1,
            on_submit= lambda e: updateBudget(e)
        )
        return ft.Container(
            ft.Column(
                [
                    ft.Text("Impostazioni", size=30, weight=ft.FontWeight.BOLD),
                    budgetTextField,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            alignment=ft.Alignment.CENTER,
            expand=True,
            padding=5,
        )

    def filter():
        return ft.BottomSheet(
            content=ft.Column(
                [

                ],
            )
        )


    def updateList():
        speseDb = expensesDatabase.getSpese()

        if searchKey != "":
            searchedSpese = [s for s in speseDb if searchKey in s.nome.lower() or searchKey in s.note.lower() or any(searchKey in t.lower() for t in s.tag)]
        else:
            searchedSpese = speseDb
            nonlocal speseSorted
        speseSorted = searchedSpese
        pagina.content = home()
        page.update()

    def home():
        def remainingBudget():
            CurrentMonth = datetime.datetime.now().month
            speseDb = expensesDatabase.getSpese()
            speso = 0
            for s in speseDb:
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
        def toolBar():
            def updateKey(e):
                nonlocal searchKey
                searchKey = ricerca.value.strip().lower()
                updateList()

            ricerca = ft.SearchBar(
                value=searchKey,
                height=40,
                expand=True,
                on_submit=updateKey,
            )

            return ft.Row(
                [
                    ricerca,
                    ft.IconButton(
                        icon=ft.icons.Icons.FILTER_ALT,
                        bgcolor=ft.Colors.GREY_800,
                        on_click=lambda e: page.show_dialog(filter()),
                        aspect_ratio=1,
                        disabled=True,
                        visible=False
                    ),
                    ft.IconButton(
                        icon=ft.icons.Icons.ADD_CIRCLE_OUTLINE,
                        bgcolor=ft.Colors.GREY_800,
                        aspect_ratio=1,
                        on_click=lambda e: apriAdd(e, None, False)
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10,
                height=40,
            )
        def lista_pagamenti():
            speseView = ft.ListView(expand=1, spacing=12, padding=5, auto_scroll=True)

            for p in speseSorted:
                speseView.controls.append(
                    ft.ListTile(
                        title=ft.Text(p.nome, weight=ft.FontWeight.BOLD),
                        subtitle=ft.Text(f"Data: {p.data}"),
                        trailing=ft.Text(f"€ {p.prezzo:.2f}", weight=ft.FontWeight.BOLD, size=15),
                        data=p,
                        on_click=lambda e: apriAdd(e, e.control.data, True),
                    ) 
                )
                speseView.controls.append(ft.Divider(height=1))

            return speseView

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
            pagina.content = settings()
        page.update()

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.icons.Icons.HOUSE, label="Home",),
            ft.NavigationBarDestination(icon=ft.icons.Icons.SETTINGS, label="impostazioni"),
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
    ft.run(main, assets_dir="assets")