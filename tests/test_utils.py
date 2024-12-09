import subprocess
import unittest
from unittest.mock import MagicMock, patch

from tutordiscovery import utils


class UtilsTests(unittest.TestCase):
    @patch("subprocess.run")
    def test_is_docker_rootless(self, mock_run: MagicMock) -> None:
        # Mock rootless `docker info` output
        utils.is_docker_rootless.cache_clear()
        mock_run.return_value.stdout = "some prefix\n rootless foo bar".encode("utf-8")
        self.assertTrue(utils.is_docker_rootless())

        # Mock regular `docker info` output
        utils.is_docker_rootless.cache_clear()
        mock_run.return_value.stdout = "some prefix, regular docker".encode("utf-8")
        self.assertFalse(utils.is_docker_rootless())

    @patch("subprocess.run")
    def test_is_docker_rootless_podman(self, mock_run: MagicMock) -> None:
        """Test the `is_docker_rootless` when podman is used or any other error with `docker info`"""
        utils.is_docker_rootless.cache_clear()
        mock_run.side_effect = subprocess.CalledProcessError(1, "docker info")
        self.assertFalse(utils.is_docker_rootless())
