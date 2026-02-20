from nicegui import ui
from pages.home import home_page
from pages.declarer import declarer_page
from pages.api import api_page
from pages.association import association_page
from pages.projet import projet_page

with ui.tabs() as tabs:
    ui.tab(name='accueil', label='Accueil', icon='home')
    ui.tab(name='declarer', label='Déclarer', icon='report')
    ui.tab(name='api', label='API', icon='api')
    ui.tab(name='association', label='Association', icon='group')
    ui.tab(name='projet', label='Projet', icon='info')

with ui.tab_panels(tabs, value='accueil').classes('w-full'):
    with ui.tab_panel(name='accueil'):
        home_page()
    with ui.tab_panel(name='declarer'):
        declarer_page()
    with ui.tab_panel(name='api'):
        api_page()
    with ui.tab_panel(name='association'):
        association_page()
    with ui.tab_panel(name='projet'):
        projet_page()
ui.run(title='VBG Guinée', favicon='🛡️')