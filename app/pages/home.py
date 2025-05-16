import reflex as rx
from app.states.home_state import HomeState, OrganDataHome
from app.components.sidebar import sidebar


def organ_card_display(
    organ: OrganDataHome,
) -> rx.Component:
    return rx.el.div(
        rx.el.img(
            src=organ["image_url"],
            alt=organ["name"],
            class_name="w-full h-40 object-contain rounded-t-lg bg-gray-200 p-2",
        ),
        rx.el.div(
            rx.el.h3(
                organ["name"],
                class_name="text-lg font-semibold text-gray-800",
            ),
            rx.el.p(
                organ["function"],
                class_name="text-sm text-gray-600 mt-1",
            ),
            rx.el.p(
                f"ID: {organ['id']}",
                class_name="text-xs text-gray-500 mt-2",
            ),
            class_name="p-4",
        ),
        class_name="bg-white rounded-lg shadow-md overflow-hidden border border-gray-200",
    )


def home_content_area() -> rx.Component:
    return rx.el.main(
        rx.el.div(
            rx.el.section(
                rx.el.h2(
                    "Bienvenue dans le Dashboard Technique Interactif – GPTA",
                    class_name="text-3xl font-bold text-gray-800 mb-4",
                ),
                rx.el.p(
                    "Ce dashboard permet la gestion des organes techniques du système GPTA, avec des indicateurs de performance (MTBF, MTTR, fiabilité, disponibilité), un historique de maintenance, etc.",
                    class_name="text-gray-700 mb-2",
                ),
                rx.el.p(
                    "Le projet est fait en Python avec Reflex.",
                    class_name="text-gray-700 mb-2",
                ),
                rx.el.p(
                    "Rôle du projet : visualisation, surveillance et gestion technique des équipements.",
                    class_name="text-gray-700",
                ),
                class_name="mb-8 p-6 bg-white rounded-lg shadow-lg border border-gray-200",
            ),
            rx.el.section(
                rx.el.h3(
                    "Chargement Dynamique des Organes",
                    class_name="text-2xl font-semibold text-gray-700 mb-6",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.h4(
                            "Importer depuis un fichier JSON",
                            class_name="text-xl font-medium text-gray-700 mb-3",
                        ),
                        rx.upload(
                            rx.el.button(
                                "Sélectionner Fichier JSON",
                                class_name="button-custom px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg shadow",
                            ),
                            id="json_upload",
                            accept={
                                "application/json": [
                                    ".json"
                                ]
                            },
                            on_drop=HomeState.handle_json_upload,
                            border="2px dashed #cbd5e1",
                            padding="2rem",
                            class_name="mb-6 p-6 border-2 border-dashed border-gray-300 rounded-lg text-center bg-gray-50 hover:bg-gray-100 transition-colors",
                        ),
                        rx.el.p(
                            "Exemple de format JSON attendu :",
                            class_name="text-sm text-gray-600 mt-2 mb-1",
                        ),
                        rx.el.pre(
                            '[\n  {\n    "id": "GPA1",\n    "name": "GPA1 - Groupe à vis",\n    "function": "Compresse l\'air du système.",\n    "image_url": "/images/gpa1.png" \n  }\n]',
                            class_name="text-xs bg-gray-100 p-3 rounded-md overflow-x-auto border border-gray-200",
                        ),
                        class_name="mb-6 md:mb-0",
                    ),
                    rx.el.div(
                        rx.el.h4(
                            "Ajouter un organe manuellement",
                            class_name="text-xl font-medium text-gray-700 mb-3",
                        ),
                        rx.el.form(
                            rx.el.div(
                                rx.el.label(
                                    "ID de l'organe:",
                                    class_name="block text-sm font-medium text-gray-700",
                                ),
                                rx.el.input(
                                    default_value=HomeState.form_id,
                                    name="form_id",
                                    placeholder="ex: GPA_MANUAL_1",
                                    required=True,
                                    class_name="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500",
                                ),
                                class_name="mb-4",
                            ),
                            rx.el.div(
                                rx.el.label(
                                    "Nom:",
                                    class_name="block text-sm font-medium text-gray-700",
                                ),
                                rx.el.input(
                                    default_value=HomeState.form_name,
                                    name="form_name",
                                    placeholder="ex: Moteur Principal",
                                    required=True,
                                    class_name="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500",
                                ),
                                class_name="mb-4",
                            ),
                            rx.el.div(
                                rx.el.label(
                                    "Fonction:",
                                    class_name="block text-sm font-medium text-gray-700",
                                ),
                                rx.el.input(
                                    default_value=HomeState.form_function,
                                    name="form_function",
                                    placeholder="ex: Assure la propulsion",
                                    required=True,
                                    class_name="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500",
                                ),
                                class_name="mb-4",
                            ),
                            rx.el.div(
                                rx.el.label(
                                    "URL de l'image (optionnel):",
                                    class_name="block text-sm font-medium text-gray-700",
                                ),
                                rx.el.input(
                                    default_value=HomeState.form_image_url,
                                    name="form_image_url",
                                    placeholder="ex: /images/my_organ.png ou laisser vide",
                                    class_name="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500",
                                ),
                                class_name="mb-4",
                            ),
                            rx.el.button(
                                "Ajouter Organe",
                                type="submit",
                                class_name="w-full px-6 py-3 bg-green-600 hover:bg-green-700 text-white rounded-lg shadow button-custom",
                            ),
                            on_submit=HomeState.add_organ_manually,
                            reset_on_submit=True,
                            class_name="p-6 border border-gray-300 rounded-lg bg-gray-50",
                        ),
                    ),
                    class_name="grid md:grid-cols-2 gap-8",
                ),
                class_name="mb-8 p-6 bg-white rounded-lg shadow-lg border border-gray-200",
            ),
            rx.el.section(
                rx.el.h3(
                    "Organes Chargés Dynamiquement",
                    class_name="text-2xl font-semibold text-gray-700 mb-6",
                ),
                rx.cond(
                    HomeState.loaded_organs.length() > 0,
                    rx.el.div(
                        rx.foreach(
                            HomeState.loaded_organs,
                            organ_card_display,
                        ),
                        class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6",
                    ),
                    rx.el.div(
                        rx.el.p(
                            "Aucun organe chargé pour l’instant.",
                            class_name="text-gray-600 text-lg",
                        ),
                        class_name="text-center p-10 border-2 border-dashed border-gray-300 rounded-lg bg-gray-50",
                    ),
                ),
                class_name="p-6 bg-white rounded-lg shadow-lg border border-gray-200",
            ),
            class_name="container mx-auto px-4 py-8",
        ),
        class_name="flex-grow transition-all duration-300 ease-in-out ml-64 bg-gray-100 min-h-screen pt-16",
    )


def home() -> rx.Component:
    return rx.el.div(
        rx.el.header(
            rx.el.div(
                rx.el.h1(
                    "Accueil – Gestionnaire d'Organes GPTA",
                    class_name="text-2xl font-bold text-white",
                ),
                class_name="container mx-auto px-4 py-4 flex items-center justify-between",
            ),
            class_name="bg-indigo-800 shadow-md fixed top-0 left-0 right-0 z-50 h-16",
        ),
        rx.el.div(
            sidebar(),
            home_content_area(),
            class_name="flex flex-row",
        ),
        class_name="font-sans antialiased text-gray-900 bg-gray-100",
    )