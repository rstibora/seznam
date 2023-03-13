from datetime import datetime, timedelta
import json
import os
from unittest.mock import patch, MagicMock

from django.test import TestCase

import videos.tasks as tasks
from .models import FetchMetadata, Metadata


class TestMetadataCheck(TestCase):
    @patch("videos.tasks._update_metadata")
    def test_fetch_matadata_empty(self, patched_update_function):
        tasks.check_fetch_store_metadata()
        assert patched_update_function.called

    @patch("videos.tasks._update_metadata")
    def test_fetch_matadata_stale(self, patched_update_function):
        fetch_metadata = FetchMetadata.load()
        fetch_metadata.data_expires_at = datetime.now() - timedelta(hours=1)
        fetch_metadata.save()

        tasks.check_fetch_store_metadata()
        assert patched_update_function.called

    @patch("videos.tasks._update_metadata")
    def test_fetch_matadata_fresh(self, patched_update_function):
        fetch_metadata = FetchMetadata.load()
        fetch_metadata.data_expires_at = datetime.now() + timedelta(hours=1)
        fetch_metadata.save()

        tasks.check_fetch_store_metadata()
        assert patched_update_function.not_called


class TestMetadataUpdate(TestCase):
    def test_update_metadata_works(self):
        with open(f"{os.path.dirname(os.path.realpath(__file__))}/test_data.json", "r") as test_json_file:
            response = MagicMock(
                json=lambda: json.load(test_json_file),
                headers={"expires": "Fri, 10 Mar 2023 20:08:10 GMT"})
            with patch("requests.get", return_value=response) as patched_get: 
                assert len(Metadata.objects.all()) == 0
                tasks._update_metadata()
                assert len(Metadata.objects.all()) == 90
                assert patched_get.called
                assert FetchMetadata.load().data_expires_at is not None
                assert FetchMetadata.load().data_expires_at.day == 10
                assert FetchMetadata.load().data_expires_at.month == 3
                assert FetchMetadata.load().data_expires_at.year == 2023
                assert FetchMetadata.load().data_expires_at.hour == 20
                assert FetchMetadata.load().data_expires_at.minute == 8
