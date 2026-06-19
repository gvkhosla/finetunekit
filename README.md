# FineTuneKit

Beginner-friendly, agent-native scaffolding for fine-tuning open-source models with [Unsloth](https://github.com/unslothai/unsloth).

> Independent community project. All credit for Unsloth itself goes to the [Unsloth team](https://github.com/unslothai/unsloth). FineTuneKit is built to complement Unsloth Core, [Unsloth Studio](https://unsloth.ai/docs/new/studio), official docs, and official notebooks — not replace them. For official Unsloth docs, see https://unsloth.ai/docs. See `NOTICE.md` for attribution and license notes.

## Why I built this

I wanted to make it personally easier to fine-tune open-source models and bring them into my own workflows and agents. Unsloth is powerful, but I kept wanting a simpler on-ramp for the repetitive beginner steps: choosing a model, checking data, creating train/eval splits, generating scripts, and giving coding agents a workflow they can reliably follow.

FineTuneKit helps anyone with a coding agent go from “I have a use case / CSV / chat examples” to a reproducible Unsloth project with:

- model + hardware recommendations
- data conversion, linting, and previews
- generated `train.py`, `chat.py`, and `eval.py`
- beginner-safe LoRA/QLoRA defaults
- agent-native workflows for Pi, Claude Code, Codex, Amp, OpenCode, and other coding harnesses

The CLI itself uses only Python stdlib. The generated training project installs Unsloth in the GPU environment.

## Ask your coding agent

If you are using Pi, Claude Code, Codex, Amp, OpenCode, or another harness, paste:

```text
Use this repo's AGENTS.md / FineTuneKit workflow. I want to fine-tune an open-source model with Unsloth for: <describe task>. Start small, check my environment, recommend a model, create a project, validate data before training, set up held-out evals, and do not start training or spend money without my approval.
```

More copy/paste prompts: `docs/COPY_PASTE_PROMPTS.md`.

## Get value immediately

If you just want to see what this does:

```bash
git clone https://github.com/gvkhosla/finetunekit.git
cd finetunekit
python3 -m finetunekit demo /tmp/finetunekit-demo
open /tmp/finetunekit-demo/START_HERE.md  # or just read it in your editor
```

That creates a tiny working project with sample train/eval data, `config.json`, `train.py`, `eval.py`, and `chat.py`.

## 60-second start with your own idea/data

If you're coming from the launch post, start here:

```bash
git clone https://github.com/gvkhosla/finetunekit.git
cd finetunekit
./scripts/install-cli.sh        # optional: installs `finetunekit` command to ~/bin
python3 -m finetunekit quickstart

# Or non-interactive:
python3 -m finetunekit doctor
python3 -m finetunekit recommend --task support-bot
python3 -m finetunekit new my-support-bot --task support-bot --model tiny-smoke-test
python3 -m finetunekit data check my-support-bot/data/train.jsonl
```

Then, in a GPU/Unsloth environment:

```bash
cd my-support-bot
python train.py
python eval.py --base
python eval.py
python chat.py
```

## Install as a CLI

The most reliable beginner install is the tiny wrapper script:

```bash
git clone https://github.com/gvkhosla/finetunekit.git
cd finetunekit
./scripts/install-cli.sh
finetunekit new my-bot
```

You can also use `python3 -m finetunekit ...` from the repo without installing anything.

## Attribution and licenses

FineTuneKit is MIT licensed and does not vendor Unsloth code, models, notebooks, or assets. Generated projects import Unsloth in your training environment.

Important: Unsloth, base models, and datasets have their own licenses/terms. Check official Unsloth docs and each model/dataset license before redistribution or commercial use. See `NOTICE.md`.

For generated-script assumptions and Unsloth API touchpoints, see `docs/UNSLOTH_COMPATIBILITY.md`.

## Why the Unsloth community might want this

Unsloth is already fast and powerful. FineTuneKit tries to reduce the beginner support burden around the parts that happen before and around training:

- “Which model fits my GPU?”
- “Is my dataset formatted correctly?”
- “How do I make train/eval splits?”
- “How do I compare base vs fine-tuned?”
- “How do I get my coding agent to help without inventing a broken training script?”

See `docs/UNSLOTH_COMMUNITY.md` for positioning and roadmap.

## Agent-native setup

FineTuneKit is designed for anyone working through a coding agent — Pi, Claude Code, Codex, Amp, OpenCode, or another harness.

- **Pi**: native `/finetune` launcher + agent-callable tools.
- **Claude Code / Codex**: shared `finetune-open-models` skill.
- **Amp / OpenCode / other harnesses**: repo-level `AGENTS.md` and command-first docs.

See `docs/AGENT_NATIVE.md` and `docs/COPY_PASTE_PROMPTS.md` for details.

Install shared skills for Pi / Claude Code / Codex and the Pi-native extension:

```bash
./scripts/install-agent-integrations.sh all
```

Then restart your agent or run `/reload` in Pi.

### Pi-native launcher

In Pi, use:

```text
/finetune
```

The Pi extension adds:

- a `/finetune` TUI launcher
- native tools for doctor, recommendations, project creation, data checks, CSV conversion, train/eval splitting, approved background training, and eval runs
- a live status/widget for background training logs

### Claude Code / Codex / Amp / OpenCode / other agents

The repo includes:

```text
AGENTS.md                         # generic coding-agent instructions
CLAUDE.md                         # Claude Code instructions
docs/AGENT_QUICKSTART.md          # command-first workflow
skills/finetune-open-models/SKILL.md
```

Agents should follow the same loop:

1. clarify task/data/hardware
2. run `doctor`
3. recommend a small model
4. create project
5. check data
6. baseline eval
7. train
8. adapter eval + chat inspection
9. iterate from failures

## Commands

```bash
# Instant demo project
python3 -m finetunekit demo /tmp/finetunekit-demo

# Interactive wizard
python3 -m finetunekit quickstart
python3 -m finetunekit quickstart --path my-bot --task support-bot --data support.csv

# Environment + model selection
python3 -m finetunekit doctor
python3 -m finetunekit recommend --task support-bot --vram-gb 8 --no-detect

# Project generation
python3 -m finetunekit new my-bot --task support-bot --model tiny-smoke-test
python3 -m finetunekit new my-bot --task domain-qa --model beginner-3b

# Data helpers
python3 -m finetunekit data check my-bot/data/train.jsonl
python3 -m finetunekit data convert input.csv my-bot/data/train.jsonl
python3 -m finetunekit data split all.jsonl my-bot/data/train.jsonl my-bot/data/eval.jsonl

# Generated-project workflow
cd my-bot
python eval.py --base
python train.py
python eval.py
python chat.py
python chat.py --base
```

## What `new` generates

```text
my-bot/
  START_HERE.md        # copy/paste guide for beginners
  config.json          # beginner-safe model + LoRA defaults
  train.py             # Unsloth SFT script
  chat.py              # interactive adapter/base chat
  eval.py              # tiny held-out before/after eval
  data/train.jsonl     # sample training data
  data/eval.jsonl      # sample held-out eval data
  notes/plan.md        # experiment checklist
```

## Data formats

Preferred chat JSONL:

```json
{"messages": [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]}
```

Also accepted by `data check`:

- `{"instruction": "...", "input": "...", "output": "..."}`
- `{"prompt": "...", "response": "..."}`
- `{"question": "...", "answer": "..."}`
- ShareGPT-ish `{"conversations": [{"from": "human", "value": "..."}, ...]}`

CSV conversion accepts headers:

- `instruction,output`
- `prompt,response`
- `question,answer`

```bash
python3 -m finetunekit data convert support.csv data/train.jsonl
```

## Training environment

For Unsloth Core, follow the current Unsloth install path in your GPU environment:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv unsloth_env --python 3.13
source unsloth_env/bin/activate
uv pip install unsloth --torch-backend=auto
```

Then run generated `train.py` from your project directory.

## Beginner rules baked in

- Use `quickstart` if you do not know where to begin.
- Run `doctor` before training.
- Run `data check` before training.
- Start with a 1B/3B smoke test before a 7B/8B run.
- Keep `data/eval.jsonl` held out.
- Compare `python eval.py --base` vs `python eval.py`.
- Inspect real outputs; do not trust loss alone.
- Do not launch paid cloud GPUs or push models to Hugging Face without explicit approval.

## Contributing

PRs and recipe requests are welcome. See `CONTRIBUTING.md`. If you are from the Unsloth team/community and something here should be corrected, credited differently, or removed, please open an issue or PR.

Especially useful contributions:

- task recipes
- tiny example datasets
- better evals
- Colab/RunPod launchers
- fixes when official Unsloth APIs/templates change

## Project health

The repo includes GitHub Actions CI for Python unit tests and CLI smoke tests.

Zero-dependency local smoke test:

```bash
python3 scripts/smoke-test.py
```

Full local check:

```bash
python3 -m unittest discover -v
python3 scripts/smoke-test.py
```

## Status

MVP scaffold. Good next additions:

- richer eval comparison summaries
- `/finetune-chat` Pi command
- LLM-as-judge evals
- task-specific recipes for extractor/classifier/domain-QA/writing-style
- Colab/RunPod launchers
- Hugging Face export helpers
