from nicegui import ui

def api_page():
    ui.markdown('''
        # API VBG Guinée

        Notre API permet aux développeurs d'accéder aux données et aux fonctionnalités de notre plateforme de lutte contre les violences basées sur le genre (VBG) en Guinée. Vous pouvez utiliser notre API pour intégrer nos services dans vos applications, créer des tableaux de bord personnalisés ou analyser les données sur les VBG.

        ## Points de terminaison disponibles

        - **/api/vbg** : Obtenez une liste des incidents de VBG déclarés.
        - **/api/vbg/{id}** : Obtenez les détails d'un incident de VBG spécifique.
        - **/api/statistiques** : Obtenez des statistiques agrégées sur les VBG en Guinée.

        ## Comment utiliser l'API

        1. Inscrivez-vous pour obtenir une clé API.
        2. Utilisez la clé API pour authentifier vos requêtes.
        3. Consultez notre documentation pour connaître les paramètres et les formats de réponse.

        Nous sommes engagés à protéger la confidentialité et la sécurité des données, et nous encourageons tous les utilisateurs à respecter ces principes lors de l'utilisation de notre API.

    ''')