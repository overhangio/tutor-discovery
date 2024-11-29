import subprocess
from functools import lru_cache


@lru_cache(maxsize=None)
def is_docker_rootless() -> bool:
    """
    A helper function to determine if Docker is running in rootless mode.

     - https://docs.docker.com/engine/security/rootless/
    """
    try:
        results = subprocess.run(["docker", "info"], capture_output=True, check=True)
        return "rootless" in results.stdout.decode()
    except subprocess.CalledProcessError:
        return False
