from datetime import datetime, timedelta
from unittest.mock import patch

from django.test import TestCase

import videos.tasks as tasks
from .models import FetchMetadata


class TestMetadataUpdate(TestCase):
    @patch('videos.tasks._update_metadata')
    def test_fetch_matadata_empty(self, patched_update_function):
        tasks.check_fetch_store_metadata()
        assert patched_update_function.called

    @patch('videos.tasks._update_metadata')
    def test_fetch_matadata_stale(self, patched_update_function):
        fetch_metadata = FetchMetadata.load()
        fetch_metadata.data_expires_at = datetime.now() - timedelta(hours=1)
        fetch_metadata.save()

        tasks.check_fetch_store_metadata()
        assert patched_update_function.called

    @patch('videos.tasks._update_metadata')
    def test_fetch_matadata_fresh(self, patched_update_function):
        fetch_metadata = FetchMetadata.load()
        fetch_metadata.data_expires_at = datetime.now() + timedelta(hours=1)
        fetch_metadata.save()

        tasks.check_fetch_store_metadata()
        assert patched_update_function.not_called
