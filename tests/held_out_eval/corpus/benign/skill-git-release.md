---
name: git-release
description: Cut a tagged release and draft release notes. Use when the user asks to "cut a release", "tag a version", or "draft release notes". Follows semver and our CHANGELOG conventions.
allowed-tools: Bash(git log*), Bash(git tag*), Bash(git describe*), Bash(gh release*)
---

# Git Release Skill

Cuts a release from `main`. We follow semantic versioning and Keep a Changelog.

## Steps

1. Confirm the working tree is clean (`git status`) and you're on `main`
   (`git branch --show-current`).
2. Determine the last tag: `git describe --tags --abbrev=0`.
3. Collect the changes since then: `git log <last-tag>..HEAD --oneline`.
4. Group commits into Added / Changed / Fixed / Removed for the CHANGELOG.
5. Propose the next version (patch/minor/major) and ask the user to confirm the
   bump before tagging.
6. Tag: `git tag -a vX.Y.Z -m "Release vX.Y.Z"` then `git push origin vX.Y.Z`.
7. Draft the GitHub release: `gh release create vX.Y.Z --notes-file notes.md`.

## Conventions

- Tags are always `vMAJOR.MINOR.PATCH`.
- Don't push tags until the user approves the version number and the notes.
- If CI is red on `main`, stop and report it — do not cut a release on a broken
  build.
- Pre-releases use a `-rc.N` suffix and `gh release create --prerelease`.
