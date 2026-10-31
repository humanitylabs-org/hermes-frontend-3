# Hermes Desktop in Browser

Desktop-style browser UI for your existing Hermes Agent.

A [Wizard app](https://www.aiwizards.com/wizard-apps): install it from the Wizard Apps screen, or with the Wizard App Manager on any box running stock [Runtipi](https://runtipi.io).

- `wizard.md`: what the app is and what it gives the agent (spec: wizard.md v0.2).
- `runtipi/`: stock Runtipi `config.json` and `docker-compose.yml`.

- `.github/workflows/publish.yml`: every push to `main` re-publishes to the index at apps.aiwizards.com.

Image build notes: [IMAGE.md](IMAGE.md).

## App identity and compatibility

The Wizard app id is `hermes-desktop-in-browser`, matching **Hermes Desktop in
Browser**. `renamed_from: [hermes-frontend-3]` lets the App Manager move existing
installs before updating them (`wam app-rename hermes-frontend-3
hermes-desktop-in-browser --dry-run` previews it). The Compose main service and
Runtipi id match the new id. The pinned GHCR image, backend URL setting, port and
source URL stay unchanged: they are existing artifact/API/repository references,
not app ids. No Hermes Agent code or data is changed.

Checks (Python 3.10+):
```sh
uv run --with pyyaml python -m unittest discover -s tests -v
```
This packaging repo had no test suite; these checks cover the identity contract
and backend-origin rejection. Upstream renderer build/smoke commands are
documented in [IMAGE.md](IMAGE.md), and are not included in this repo.
