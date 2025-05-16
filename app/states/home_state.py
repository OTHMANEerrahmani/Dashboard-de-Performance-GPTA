import reflex as rx
import json
from typing import TypedDict, List, Any


class OrganDataHome(TypedDict):
    id: str
    name: str
    function: str
    image_url: str


class HomeState(rx.State):
    """Manages the state for the Home page, including dynamic organ loading."""

    loaded_organs: List[OrganDataHome] = []
    form_id: str = ""
    form_name: str = ""
    form_function: str = ""
    form_image_url: str = ""

    @rx.event
    def add_organ_manually(self, form_data: dict):
        """Adds an organ based on manual form input."""
        form_id_val = form_data.get("form_id", "").strip()
        form_name_val = form_data.get(
            "form_name", ""
        ).strip()
        form_function_val = form_data.get(
            "form_function", ""
        ).strip()
        form_image_url_val = form_data.get(
            "form_image_url", ""
        ).strip()
        if (
            not form_id_val
            or not form_name_val
            or (not form_function_val)
        ):
            yield rx.toast.error(
                "Les champs ID, Nom et Fonction sont requis."
            )
            return
        new_organ: OrganDataHome = {
            "id": form_id_val,
            "name": form_name_val,
            "function": form_function_val,
            "image_url": (
                form_image_url_val
                if form_image_url_val
                else "/favicon.ico"
            ),
        }
        self.loaded_organs.append(new_organ)
        self.form_id = ""
        self.form_name = ""
        self.form_function = ""
        self.form_image_url = ""
        yield rx.toast.success(
            f"Organe '{new_organ['name']}' ajouté manuellement."
        )

    @rx.event
    async def handle_json_upload(self, files: Any):
        """Handles JSON file upload, parses it, and adds organs to the list."""
        if not files:
            yield rx.toast.error(
                "Aucun fichier sélectionné."
            )
            return
        try:
            uploaded_file: rx.UploadFile = files[0]
            content_bytes = await uploaded_file.read()
            content_str = content_bytes.decode("utf-8")
            data = json.loads(content_str)
            if not isinstance(data, list):
                yield rx.toast.error(
                    "Le fichier JSON doit contenir une liste d'organes."
                )
                return
            added_count = 0
            for item in data:
                if (
                    isinstance(item, dict)
                    and "id" in item
                    and ("name" in item)
                    and ("function" in item)
                ):
                    organ_id = str(item["id"]).strip()
                    organ_name = str(item["name"]).strip()
                    organ_function = str(
                        item["function"]
                    ).strip()
                    image_url_raw = str(
                        item.get("image_url", "")
                    ).strip()
                    if (
                        not organ_id
                        or not organ_name
                        or (not organ_function)
                    ):
                        yield rx.toast.warning(
                            "Un organe dans le JSON a des champs obligatoires vides et a été ignoré."
                        )
                        continue
                    organ: OrganDataHome = {
                        "id": organ_id,
                        "name": organ_name,
                        "function": organ_function,
                        "image_url": (
                            image_url_raw
                            if image_url_raw
                            else "/favicon.ico"
                        ),
                    }
                    self.loaded_organs.append(organ)
                    added_count += 1
                else:
                    yield rx.toast.warning(
                        "Un élément du JSON n'a pas le format attendu et a été ignoré."
                    )
            if added_count > 0:
                yield rx.toast.success(
                    f"{added_count} organe(s) importé(s) avec succès depuis le JSON."
                )
            elif not data:
                yield rx.toast.info(
                    "Le fichier JSON est une liste vide. Aucun organe importé."
                )
            else:
                yield rx.toast.info(
                    "Aucun organe valide trouvé dans le JSON."
                )
        except json.JSONDecodeError:
            yield rx.toast.error(
                "Erreur de décodage JSON. Vérifiez le format du fichier."
            )
        except Exception as e:
            yield rx.toast.error(
                f"Erreur lors du traitement du fichier : {str(e)}"
            )