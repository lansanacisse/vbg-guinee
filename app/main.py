from nicegui import ui
from pages.home import home_page

with ui.tabs() as tabs:
    ui.tab(name='accueil', label='Accueil', icon='home')
    ui.tab(name='declarer', label='Declarer', icon='info')
    ui.tab(name='api', label='API', icon='api')
    ui.tab(name='association', label='Association', icon='group')
    ui.tab(name='projets', label='Projets', icon='project')
with ui.tab_panels(tabs, value='accueil'):
        with ui.tab_panel(name='accueil'):
            home_page()
        with ui.tab_panel(name='declarer'):
            ui.label('Page de déclaration')
        with ui.tab_panel(name='api'):
            ui.label('Page API')
        with ui.tab_panel(name='association'):
            ui.label('Page Association')
        with ui.tab_panel(name='projets'):
            ui.label('Page Projets')

ui.run()