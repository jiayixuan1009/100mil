---
description: "Use when creating or editing Python scripts in scripts/. Covers warehouse scripts, validation scripts, and repeatable analysis automation for this repository."
applyTo: "scripts/**/*.py"
---
# Script Instructions

- Scripts in this repo should support repeatable analysis or validation, not one-off local hacks.
- Default to reading from repo-relative paths under `data/warehouse/`, `docs/`, or raw catalog sources already defined in the project.
- Keep failure output explicit enough that another AI or human can continue the task from the script result.
- Favor small CLI flags or narrow invocation options over hard-coded rerun-only behavior.
- If a script writes generated outputs, keep them in ignored warehouse paths or explicit docs CSV outputs.
- Run the touched script or the narrowest possible invocation after editing.
