---
name: Deployment AI requirements fix
description: requirements.txt must read from code dict, not hardcoded FastAPI deps
---

## Rule
`generate_release_artifacts()` in `plugins/deployment_ai/agent.py` must derive
requirements from `code.get("requirements", [])`, never from a hardcoded list.

**Why:** The old hardcode `["fastapi","uvicorn","pydantic"]` shipped wrong deps for
every non-FastAPI project type (stdlib-only, Flask, tkinter, etc.).

**How to apply:** If deployment_ai is ever modified, verify the requirements block
reads from the code dict. Write an empty comment line when the list is empty so the
file is still valid.
