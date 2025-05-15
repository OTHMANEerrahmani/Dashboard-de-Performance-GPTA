import reflex as rx
from typing import TypedDict, List, Optional
from datetime import datetime, timezone
import math


class OrganData(TypedDict):
    id: str
    name: str
    function: str
    image_url: str


class MaintenanceInterventionData(TypedDict):
    date: str
    organ_id: str
    type: str
    duration_h: float
    action: str
    remarks: str


ORGANS_LIST: List[OrganData] = [
    {
        "id": "GPA1",
        "name": "GPA1 - Groupe à vis",
        "function": "Compresse l'air du système.",
        "image_url": "/gpa1_vis.png",
    },
    {
        "id": "GPA2",
        "name": "GPA2 - Dessiccateur",
        "function": "Assèche l'air comprimé.",
        "image_url": "/gpa2_dessiccateur.png",
    },
    {
        "id": "GPA3",
        "name": "GPA3 - ADCU",
        "function": "Unité de contrôle et de surveillance.",
        "image_url": "/gpa3_adcu.png",
    },
    {
        "id": "GPA4",
        "name": "GPA4 - Ventilateur",
        "function": "Refroidit les composants du système.",
        "image_url": "/gpa4_ventilateur.png",
    },
    {
        "id": "GPA5",
        "name": "GPA5 - Capteurs / Pressostats",
        "function": "Mesure la pression et d'autres paramètres.",
        "image_url": "/gpa5_capteurs.png",
    },
    {
        "id": "GPA6",
        "name": "GPA6 - Soupape de sécurité",
        "function": "Prévient les surpressions.",
        "image_url": "/gpa6_soupape.png",
    },
    {
        "id": "GPA7",
        "name": "GPA7 - Système de graissage",
        "function": "Lubrifie les parties mobiles.",
        "image_url": "/gpa7_graissage.png",
    },
]
MAINTENANCE_HISTORY_DATA: List[
    MaintenanceInterventionData
] = [
    {
        "date": "2024-02-10",
        "organ_id": "GPA1",
        "type": "Corrective",
        "duration_h": 2.5,
        "action": "Remplacement roulements",
        "remarks": "Bruit",
    },
    {
        "date": "2024-02-25",
        "organ_id": "GPA2",
        "type": "Preventive",
        "duration_h": 1.0,
        "action": "Changement alumine",
        "remarks": "RAS",
    },
    {
        "date": "2024-03-15",
        "organ_id": "GPA3",
        "type": "Corrective",
        "duration_h": 3.0,
        "action": "Remplacement ADCU",
        "remarks": "EV HS",
    },
    {
        "date": "2024-03-30",
        "organ_id": "GPA4",
        "type": "Preventive",
        "duration_h": 1.0,
        "action": "Nettoyage",
        "remarks": "",
    },
    {
        "date": "2024-04-10",
        "organ_id": "GPA1",
        "type": "Corrective",
        "duration_h": 4.0,
        "action": "Réparation fuite huile",
        "remarks": "Fuite",
    },
    {
        "date": "2024-04-20",
        "organ_id": "GPA5",
        "type": "Corrective",
        "duration_h": 1.5,
        "action": "Remplacement capteur pression",
        "remarks": "Erreur P",
    },
    {
        "date": "2024-05-01",
        "organ_id": "GPA2",
        "type": "Corrective",
        "duration_h": 2.0,
        "action": "Remplacement valve dessiccateur",
        "remarks": "Bloquée",
    },
    {
        "date": "2024-05-10",
        "organ_id": "GPA1",
        "type": "Preventive",
        "duration_h": 0.5,
        "action": "Contrôle vibrations",
        "remarks": "OK",
    },
]


class GptaState(rx.State):
    organs: List[OrganData] = ORGANS_LIST
    maintenance_history: List[
        MaintenanceInterventionData
    ] = MAINTENANCE_HISTORY_DATA
    selected_organ_id: str = ""
    user_input_t_str: str = "1000"
    user_input_r0_str: str = "0.9"

    @rx.var
    def selected_organ(self) -> Optional[OrganData]:
        if not self.selected_organ_id:
            return None
        for organ in self.organs:
            if organ["id"] == self.selected_organ_id:
                return organ
        return None

    @rx.var
    def current_organ_interventions(
        self,
    ) -> List[MaintenanceInterventionData]:
        if not self.selected_organ_id:
            return []
        return [
            item
            for item in self.maintenance_history
            if item["organ_id"] == self.selected_organ_id
        ]

    @rx.var
    def _system_observation_period_hours(self) -> float:
        if not self.maintenance_history:
            return 0.0
        dates = [
            datetime.strptime(
                item["date"], "%Y-%m-%d"
            ).replace(tzinfo=timezone.utc)
            for item in self.maintenance_history
        ]
        min_date = min(dates)
        max_date = datetime.now(timezone.utc)
        duration = max_date - min_date
        return duration.total_seconds() / 3600

    @rx.var
    def num_failures(self) -> int:
        return len(
            [
                item
                for item in self.current_organ_interventions
                if item["type"] == "Corrective"
            ]
        )

    @rx.var
    def total_corrective_repair_duration_hours(
        self,
    ) -> float:
        return sum(
            (
                item["duration_h"]
                for item in self.current_organ_interventions
                if item["type"] == "Corrective"
            )
        )

    @rx.var
    def organ_total_operating_hours(self) -> float:
        if not self.selected_organ:
            return 0.0
        operating_hours = (
            self._system_observation_period_hours
            - self.total_corrective_repair_duration_hours
        )
        return max(0.0, operating_hours)

    @rx.var
    def mtbf(self) -> float | str:
        if self.num_failures == 0:
            return (
                "N/A (Pas de panne)"
                if self.organ_total_operating_hours > 0
                else "N/A"
            )
        if self.organ_total_operating_hours <= 0:
            return "N/A (Op. Hrs <=0)"
        return round(
            self.organ_total_operating_hours
            / self.num_failures,
            2,
        )

    @rx.var
    def mttr(self) -> float | str:
        if self.num_failures == 0:
            return "N/A (Pas d'intervention corrective)"
        return round(
            self.total_corrective_repair_duration_hours
            / self.num_failures,
            2,
        )

    @rx.var
    def lambda_rate(self) -> float | str:
        mtbf_val = self.mtbf
        if isinstance(mtbf_val, str) or mtbf_val <= 0:
            return "N/A"
        return round(1 / mtbf_val, 6)

    @rx.var
    def availability(self) -> float | str:
        mtbf_val = self.mtbf
        mttr_val = self.mttr
        if isinstance(mtbf_val, str) or isinstance(
            mttr_val, str
        ):
            if (
                isinstance(mtbf_val, str)
                and "Pas de panne" in mtbf_val
            ):
                return 1.0
            return "N/A"
        if mtbf_val + mttr_val == 0:
            return "N/A"
        return round(mtbf_val / (mtbf_val + mttr_val), 4)

    @rx.var
    def user_input_t(self) -> float:
        try:
            return float(self.user_input_t_str)
        except ValueError:
            return 1000.0

    @rx.var
    def user_input_r0(self) -> float:
        try:
            val = float(self.user_input_r0_str)
            return max(0.0001, min(val, 0.9999))
        except ValueError:
            return 0.9

    @rx.var
    def reliability_rt(self) -> float | str:
        lambda_val = self.lambda_rate
        if isinstance(lambda_val, str) or lambda_val < 0:
            if (
                isinstance(lambda_val, str)
                and self.num_failures == 0
            ):
                return 1.0
            return "N/A"
        t = self.user_input_t
        try:
            return round(math.exp(-lambda_val * t), 4)
        except OverflowError:
            return "N/A (Calcul impossible)"

    @rx.var
    def preventive_periodicity(self) -> float | str:
        lambda_val = self.lambda_rate
        r0 = self.user_input_r0
        if isinstance(lambda_val, str) or lambda_val <= 0:
            return "N/A (Lambda non positif)"
        if not 0 < r0 < 1:
            return "N/A (R0 hors limites)"
        try:
            return round(-math.log(r0) / lambda_val, 2)
        except (
            ValueError,
            ZeroDivisionError,
            OverflowError,
        ):
            return "N/A (Calcul impossible)"

    @rx.var
    def availability_display_str(self) -> str:
        val = self.availability
        if isinstance(val, float):
            return f"{val:.4f} ({val * 100:.2f}%)"
        return str(val)

    @rx.var
    def reliability_rt_display_str(self) -> str:
        val = self.reliability_rt
        if isinstance(val, float):
            return f"{val:.4f} ({val * 100:.2f}%)"
        return str(val)

    @rx.event
    def select_organ(self, organ_id: str):
        self.selected_organ_id = organ_id

    @rx.event
    def set_user_input_t_str(self, value: str):
        self.user_input_t_str = value

    @rx.event
    def set_user_input_r0_str(self, value: str):
        self.user_input_r0_str = value