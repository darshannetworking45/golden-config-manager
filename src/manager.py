"""Role-Based Golden Configuration Manager and Standardization Scorer."""

from typing import Dict, List, Set


class GoldenConfigManager:
    """Manages role-specific baseline templates and calculates compliance percentages."""

    def __init__(self):
        self.golden_templates: Dict[str, Set[str]] = {
            "access_switch": {
                "service password-encryption",
                "service timestamps log datetime msec",
                "no ip domain-lookup",
                "spanning-tree mode rapid-pvst"
            },
            "core_router": {
                "service password-encryption",
                "ip routing",
                "ip cef",
                "no ip domain-lookup"
            }
        }
        self.approved_exceptions: Dict[str, Set[str]] = {}

    def register_exception(self, hostname: str, command: str):
        """Registers a documented engineering waiver/exception for a device."""
        self.approved_exceptions.setdefault(hostname, set()).add(command)

    def calculate_standardization_score(self, hostname: str, role: str, running_config: str) -> Dict:
        """
        Calculates standardization score (0-100%).
        Accounts for approved exemptions so documented exceptions do not penalize metrics.
        """
        golden = self.golden_templates.get(role, set())
        running_lines = {l.strip() for l in running_config.splitlines() if l.strip()}
        exceptions = self.approved_exceptions.get(hostname, set())

        missing = golden - running_lines - exceptions
        adhered = len(golden) - len(missing)
        score_pct = (adhered / len(golden) * 100) if golden else 100.0

        return {
            "hostname": hostname,
            "role": role,
            "score_pct": round(score_pct, 1),
            "missing_golden_lines": sorted(list(missing)),
            "exemptions_applied": sorted(list(exceptions & (golden - running_lines)))
        }
