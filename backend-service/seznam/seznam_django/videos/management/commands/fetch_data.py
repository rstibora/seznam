from typing import Any, Optional

from django.core.management.base import BaseCommand
from django.utils import timezone

from videos.lib.api_fetch import fetch_and_store_metadata


class Command(BaseCommand):
    help = "Fetches data from the external API if they are missing from the backup DB or are stale."

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        fetch_and_store_metadata()
