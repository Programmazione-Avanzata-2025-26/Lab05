import flet as ft
from alert import AlertManager
from autonoleggio import Autonoleggio
# Assumo che Autonoleggio importi la classe Automobile
from autonoleggio import Automobile

FILE_AUTO = "automobili.csv"


def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = "center"
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DALL'AUTONOLEGGIO DEL LAB03 ---
    autonoleggio = Autonoleggio("Polito Rent", "Alessandro Visconti")
    try:
        autonoleggio.carica_file_automobili(FILE_AUTO)  # Carica il file
    except Exception as e:
        alert.show_alert(f"❌ {e}")  # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile dell'autonoleggio
    txt_titolo = ft.Text(value=autonoleggio.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {autonoleggio.responsabile}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=autonoleggio.responsabile, label="Responsabile")

    # ListView per mostrare la lista di auto aggiornata
    lista_auto = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere una nuova automobile (marca, modello, anno, contatore posti)
    # TODO
    input_marca = ft.TextField(label="Marca", width=200)
    input_modello = ft.TextField(label="Modello", width=200)
    input_anno = ft.TextField(label="Anno", width=150)

    # Contatore Posti
    posti_count = ft.Text("4")  # Valore iniziale

    # --- FUNZIONI APP ---
    def aggiorna_lista_auto():
        lista_auto.controls.clear()
        # Popola la lista con le auto ordinate
        for auto in autonoleggio.automobili_ordinate_per_marca():
            # La stringa dell'oggetto auto include già Marca, Modello, Anno e Posti.
            stato = "✅" if auto.disponibile else "⛔"

            # ATTENZIONE ALLA SINTASSI di ListView: si usa un controllo (ft.Text) e non una stringa
            lista_auto.controls.append(ft.Text(
                f"{stato} {auto.codice} | {auto.marca} {auto.modello} ({auto.anno}) | {auto.posti} posti | {'Disponibile' if auto.disponibile else 'Noleggiata'}"))

        page.update()

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"
        page.update()

    def conferma_responsabile(e):
        autonoleggio.responsabile = input_responsabile.value
        txt_responsabile.value = f"Responsabile: {autonoleggio.responsabile}"
        page.update()

    def incrementa_posti(e):
        current_posti = int(posti_count.value)
        posti_count.value = str(current_posti + 1)
        page.update()

    def decrementa_posti(e):
        current_posti = int(posti_count.value)
        if current_posti > 1:  # Assicurati che i posti non siano meno di 1
            posti_count.value = str(current_posti - 1)
            page.update()

    def aggiungi_automobile(e):
        # 1. Recupera i valori
        marca = input_marca.value
        modello = input_modello.value
        anno_str = input_anno.value
        posti_str = posti_count.value

        # 2. Validazione dei campi numerici
        try:
            anno = int(anno_str)
            posti = int(posti_str)

            if anno <= 0 or posti <= 0:
                raise ValueError  # Controlla che siano valori positivi

        except ValueError:
            # Mostra l'alert come richiesto
            alert.show_alert("❌ Errore: inserisci valori numerici validi per anno e posti.")
            return

        # 3. Validazione campi stringa
        if not marca or not modello:
            alert.show_alert("❌ Errore: Marca e Modello non possono essere vuoti.")
            return

        # 4. Aggiungi l'auto usando la logica dell'Autonoleggio
        try:
            # La funzione aggiungi_automobile() deve essere presente in Autonoleggio
            # e creare un oggetto Automobile con un codice univoco.
            # Assumiamo la firma: autonoleggio.aggiungi_automobile(marca, modello, anno, posti)
            autonoleggio.aggiungi_automobile(marca, modello, anno, posti)
        except Exception as err:
            alert.show_alert(f"❌ Errore durante l'aggiunta: {err}")
            return

        # 5. Svuota i campi TextField (il contatore posti rimane al valore finale)
        input_marca.value = ""
        input_modello.value = ""
        input_anno.value = ""

        # 6. Aggiorna la lista
        aggiorna_lista_auto()

    # Handlers per la gestione dei bottoni utili all'inserimento di una nuova auto
    # TODO

    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.ElevatedButton("Conferma", on_click=conferma_responsabile)

    # Bottoni per la gestione dell'inserimento di una nuova auto
    # TODO
    btn_aggiungi_auto = ft.ElevatedButton("Aggiungi automobile", on_click=aggiungi_automobile)
    btn_meno = ft.IconButton(ft.icons.REMOVE, on_click=decrementa_posti, style=ft.ButtonStyle(shape=ft.CircleBorder()))
    btn_piu = ft.IconButton(ft.icons.ADD, on_click=incrementa_posti, style=ft.ButtonStyle(shape=ft.CircleBorder()))

    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3: Aggiunta nuova auto
        # TODO
        ft.Divider(),
        ft.Text("Aggiungi nuova automobile", size=20),
        ft.Row(
            controls=[
                input_marca,
                input_modello,
                input_anno,
                # Controlli del contatore
                ft.Row(
                    controls=[
                        btn_meno,
                        posti_count,
                        btn_piu
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        ft.Row(
            controls=[btn_aggiungi_auto],
            alignment=ft.MainAxisAlignment.CENTER
        ),

        # Sezione 4
        ft.Divider(),
        ft.Text("Automobili", size=20),
        lista_auto,
    )
    # L'aggiornamento iniziale DEVE essere dopo aver aggiunto lista_auto alla page
    aggiorna_lista_auto()


ft.app(target=main)



