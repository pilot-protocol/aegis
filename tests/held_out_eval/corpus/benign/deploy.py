#!/usr/bin/env python3
"""Deploy helper: build artifacts and push to the staging host.

Usage:
    ./deploy.py --env staging
"""
import argparse
import os
import subprocess
import sys
from pathlib import Path

REGISTRY = "registry.internal.example.com"
SERVICE = "web-frontend"


def build_image(tag: str) -> None:
    print(f"==> Building image {SERVICE}:{tag}")
    subprocess.run(
        ["docker", "build", "-t", f"{REGISTRY}/{SERVICE}:{tag}", "."],
        check=True,
    )


def push_image(tag: str) -> None:
    print(f"==> Pushing {SERVICE}:{tag}")
    subprocess.run(["docker", "push", f"{REGISTRY}/{SERVICE}:{tag}"], check=True)


def reload_service(env: str) -> None:
    # Restart the systemd unit on the target box so it picks up the new image.
    os.system(f"ssh deploy@{env}.example.com 'sudo systemctl restart {SERVICE}'")


def main() -> int:
    parser = argparse.ArgumentParser(description="Deploy the web frontend")
    parser.add_argument("--env", default="staging", choices=["staging", "prod"])
    parser.add_argument("--tag", default=os.environ.get("GIT_SHA", "latest"))
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent
    if not (repo_root / "Dockerfile").exists():
        print("error: Dockerfile not found", file=sys.stderr)
        return 1

    build_image(args.tag)
    push_image(args.tag)
    reload_service(args.env)
    print("Deploy complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
