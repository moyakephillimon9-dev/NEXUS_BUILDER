---
name: Vision document bugs
description: Two bugs that appear when goal is a large vision document instead of a short goal string
---

## Bug 1: monitoring_ai NameError in _metrics_script

**Symptom:** `NameError: name 'tag_str' is not defined` at monitoring_ai/agent.py line ~299.

**Root cause:** `_metrics_script` is an f-string that generates Python code. The line
`return f"{{name}}{{{{{tag_str}}}}}"` tried to interpolate `tag_str` from the outer
Python scope, but `tag_str` is only defined inside the *generated* code.

**Fix:** Replace the f-string interpolation with string concatenation in the generated code:
`return name + "{{" + tag_str + "}}"` — `{{` and `}}` in the f-string become literal `{` and `}`.

**Why:** Nested f-strings with escaped braces fail silently when a variable name in the
generated code accidentally matches the outer f-string's interpolation scope.

## Bug 2: deployment_ai OSError — file name too long

**Symptom:** `OSError: [Errno 36] File name too long` when creating the deployment folder.

**Root cause:** `_sanitize_name(project["goal"])` used the full goal text. For vision
documents this is thousands of characters, producing an OS-rejected folder path.

**Fix:** `_sanitize_name` now takes only `text.strip().splitlines()[0]` (first line)
and caps the slug at 50 characters with a regex strip of non-word chars.

**How to apply:** Any worker that slugifies `project["goal"]` for a filesystem path
must truncate the goal to a short identifier first.
