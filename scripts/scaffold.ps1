param(
    [switch]$Force
)

$root = Split-Path -Path $PSScriptRoot -Parent

$directories = @(
    '.vscode',
    'configs',
    'prompts',
    'prompts/book',
    'prompts/chapter',
    'prompts/compliance',
    'schemas',
    'schemas/neo4j',
    'schemas/chroma',
    'schemas/json',
    'scripts',
    'runtime',
    'runtime/novels',
    'runtime/logs',
    'runtime/cache',
    'docs',
    'tests',
    'src',
    'src/xiaoshuo_ai',
    'src/xiaoshuo_ai/config',
    'src/xiaoshuo_ai/core',
    'src/xiaoshuo_ai/agents',
    'src/xiaoshuo_ai/memory',
    'src/xiaoshuo_ai/memory/graph',
    'src/xiaoshuo_ai/memory/vector',
    'src/xiaoshuo_ai/domain',
    'src/xiaoshuo_ai/storage',
    'src/xiaoshuo_ai/utils'
)

$files = @(
    'README.md',
    '.gitignore',
    '.env.example',
    'requirements.txt',
    'pyproject.toml',
    '.vscode/settings.json',
    '.vscode/launch.json',
    'configs/app.yaml',
    'configs/logging.yaml',
    'configs/memory.yaml',
    'prompts/book/00_brief.md',
    'prompts/book/01_outline.md',
    'prompts/book/02_chapter_map.md',
    'prompts/chapter/00_plan.md',
    'prompts/chapter/01_write.md',
    'prompts/chapter/02_review.md',
    'prompts/chapter/03_edit.md',
    'prompts/chapter/04_summary.md',
    'prompts/chapter/05_memory_extract.md',
    'prompts/compliance/tomato_rules.md',
    'prompts/compliance/content_filter.md',
    'schemas/neo4j/constraints.cypher',
    'schemas/neo4j/indexes.cypher',
    'schemas/neo4j/seed.cypher',
    'schemas/chroma/collections.yaml',
    'schemas/json/character.json',
    'schemas/json/location.json',
    'schemas/json/item.json',
    'schemas/json/chapter.json',
    'schemas/json/book.json',
    'scripts/healthcheck_memory.ps1',
    'scripts/healthcheck_memory.py',
    'scripts/neo4j_seed_demo.py',
    'scripts/chroma_seed_demo.py',
    'runtime/novels/.gitkeep',
    'runtime/logs/.gitkeep',
    'runtime/cache/.gitkeep',
    'tests/.gitkeep',
    'docs/architecture.md',
    'docs/api.md',
    'docs/usage.md',
    'docs/directory_structure.md',
    'src/xiaoshuo_ai/__init__.py',
    'src/xiaoshuo_ai/cli.py',
    'src/xiaoshuo_ai/config/__init__.py',
    'src/xiaoshuo_ai/config/loader.py',
    'src/xiaoshuo_ai/core/__init__.py',
    'src/xiaoshuo_ai/core/orchestrator.py',
    'src/xiaoshuo_ai/core/pipeline.py',
    'src/xiaoshuo_ai/core/context_builder.py',
    'src/xiaoshuo_ai/agents/__init__.py',
    'src/xiaoshuo_ai/agents/planner.py',
    'src/xiaoshuo_ai/agents/writer.py',
    'src/xiaoshuo_ai/agents/summarizer.py',
    'src/xiaoshuo_ai/agents/critic.py',
    'src/xiaoshuo_ai/agents/editor.py',
    'src/xiaoshuo_ai/agents/compliance.py',
    'src/xiaoshuo_ai/memory/__init__.py',
    'src/xiaoshuo_ai/memory/graph/__init__.py',
    'src/xiaoshuo_ai/memory/graph/client.py',
    'src/xiaoshuo_ai/memory/graph/schema.py',
    'src/xiaoshuo_ai/memory/graph/queries.py',
    'src/xiaoshuo_ai/memory/vector/__init__.py',
    'src/xiaoshuo_ai/memory/vector/client.py',
    'src/xiaoshuo_ai/memory/vector/collections.py',
    'src/xiaoshuo_ai/domain/__init__.py',
    'src/xiaoshuo_ai/domain/models.py',
    'src/xiaoshuo_ai/domain/validators.py',
    'src/xiaoshuo_ai/storage/__init__.py',
    'src/xiaoshuo_ai/storage/local_store.py',
    'src/xiaoshuo_ai/storage/snapshot_store.py',
    'src/xiaoshuo_ai/utils/__init__.py',
    'src/xiaoshuo_ai/utils/ids.py',
    'src/xiaoshuo_ai/utils/time.py',
    'src/xiaoshuo_ai/utils/retry.py',
    'src/xiaoshuo_ai/utils/log.py'
)

function Get-Template {
    param(
        [string]$RelativePath
    )

    switch ($RelativePath) {
        '.gitignore' {
            return @'
.venv/
__pycache__/
*.pyc
.pytest_cache/
.mypy_cache/
.ruff_cache/
.idea/
.vscode/*
!.vscode/settings.json
!.vscode/launch.json
runtime/logs/*
!runtime/logs/.gitkeep
runtime/cache/*
!runtime/cache/.gitkeep
'@
        }
        '.env.example' {
            return @'
NEO4J_URI=bolt://192.168.1.195:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=CHANGE_ME
CHROMA_HOST=192.168.1.195
CHROMA_PORT=8000
'@
        }
        'requirements.txt' {
            return @'
neo4j
chromadb
python-dotenv
pyyaml
requests
'@
        }
        'pyproject.toml' {
            return @'
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "xiaoshuo-ai"
version = "0.1.0"
description = "Scaffold for a dual-machine AI novel writing system with Neo4j and Chroma memories."
readme = "README.md"
requires-python = ">=3.11"
dependencies = []
authors = [
  { name = "xiaoshuo team", email = "dev@xiaoshuo.local" }
]

[project.scripts]
xiaoshuo = "xiaoshuo_ai.cli:main"

[tool.setuptools]
package-dir = { "" = "src" }

[tool.setuptools.packages.find]
where = ["src"]
'@
        }
        '.vscode/settings.json' {
            return @'
{
  "python.defaultInterpreterPath": "python",
  "python.envFile": "${workspaceFolder}/.env",
  "python.analysis.extraPaths": [
    "${workspaceFolder}/src"
  ],
  "editor.formatOnSave": true,
  "editor.defaultFormatter": null
}
'@
        }
        '.vscode/launch.json' {
            return @'
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Run xiaoshuo CLI",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/src/xiaoshuo_ai/cli.py",
      "console": "integratedTerminal",
      "justMyCode": true
    }
  ]
}
'@
        }
        'README.md' {
            return @'
# xiaoshuo AI Writing System Skeleton

## Purpose
- Provide a grounded, engine-level scaffold for the A-machine writing console and the B-machine memory servers (Neo4j + Chroma), leaving structural touchpoints for Codex to implement workflows.

## Environment
- Developed for Python 3.11+. A `venv` named `xiaoshuo` already exists, but this repository recommends activating a `.venv` inside the workspace.

## Configuration
- Copy `.env.example` to `.env` and update `NEO4J_URI`, `NEO4J_USER`, `NEO4J_PASSWORD`, `CHROMA_HOST`, and `CHROMA_PORT` (B-machine IP: `192.168.1.195`).

## Scripts
- Rebuild the scaffolding after major changes with `powershell -ExecutionPolicy Bypass -File .\scripts\scaffold.ps1`.
- Health checks for the memory services are marked TODO until workflows are added.

## Directory overview
- See `docs/directory_structure.md` for a guided tour of each surface and how the two machines collaborate via Neo4j/Chroma memories.
'@
        }
        'configs/app.yaml' {
            return @'
app:
  name: xiaoshuo-ai
  description: "Skeleton entry points for the two-machine novel writing platform."
memory:
  neo4j_uri: ${NEO4J_URI}
  neo4j_user: ${NEO4J_USER}
  neo4j_password: ${NEO4J_PASSWORD}
  chroma_host: ${CHROMA_HOST}
  chroma_port: ${CHROMA_PORT}
'@
        }
        'configs/logging.yaml' {
            return @'
version: 1
formatters:
  standard:
    format: "%(asctime)s %(levelname)s %(name)s: %(message)s"
handlers:
  console:
    class: logging.StreamHandler
    formatter: standard
    level: INFO
root:
  level: INFO
  handlers: [console]
memory:
  neo4j_uri: ${NEO4J_URI}
  neo4j_user: ${NEO4J_USER}
  neo4j_password: ${NEO4J_PASSWORD}
  chroma_host: ${CHROMA_HOST}
  chroma_port: ${CHROMA_PORT}
'@
        }
        'configs/memory.yaml' {
            return @'
memory:
  neo4j_uri: ${NEO4J_URI}
  neo4j_user: ${NEO4J_USER}
  neo4j_password: ${NEO4J_PASSWORD}
  chroma_host: ${CHROMA_HOST}
  chroma_port: ${CHROMA_PORT}
  detail_level: placeholder
'@
        }
        'docs/architecture.md' {
            return @'
# Architecture Overview

The xiaoshuo AI stack is split between the A-machine writing station and the B-machine memory servers. The A-machine hosts the CLI, orchestrator, agents, and domain logic, while the B-machine persists graph memories in Neo4j and embeddings in Chroma. Communication is mediated by exported config values and agent pipelines that orchestrate chapter planning, writing, review, and memory extraction.

Future iterations should document data flows through `src/xiaoshuo_ai/core`, agent responsibilities, and how prompts live in the `prompts/` directory.
'@
        }
        'docs/api.md' {
            return @'
# API Surface

This repository exposes the CLI located at `src/xiaoshuo_ai/cli.py` and a planned set of orchestrators, agents, and memory connectors. Each module is currently a TODO placeholder to keep the boundary defined when Codex fills in the logic.

Document actual endpoints and invocation patterns as soon as the orchestrator and agents gain concrete implementations.
'@
        }
        'docs/usage.md' {
            return @'
# Usage Guide

1. Clone the repo and install dependencies via `pip install -r requirements.txt` inside an activated `.venv`.
2. Copy `.env.example` to `.env` and fill in B-machine credentials.
3. Run `powershell -ExecutionPolicy Bypass -File .\scripts\scaffold.ps1` to ensure scaffolding is complete before starting development.

Additional usage steps (e.g., running CLI commands) will be documented once the orchestrator and agents are implemented.
'@
        }
        'docs/directory_structure.md' {
            return @'
# Directory Structure

## Top-level layout
| Directory | Purpose | Notes |
| --- | --- | --- |
| `configs/` | YAML config for app, logging, and memory endpoints. | Loader will parse and inject env vars for Neo4j/Chroma credentials. |
| `prompts/` | Codex prompt templates organized by intent (book planning, chapter work, compliance). | Maintain best prompts here so that agents can reference them when prompting Codex later. |
| `schemas/` | Neo4j/Chroma schema seeds plus domain JSON schemas. | Neo4j cypher files define constraints/indexes; JSON files sketch entity properties. |
| `scripts/` | Utility scripts such as `scaffold.ps1` and memory health checks. | Scripts should be idempotent and help rehydrate the skeleton or validate services. |
| `runtime/` | Runtime directories for novels, logs, and cache with `.gitkeep` placeholders. | Keeps git aware of runtime surface and prevents accidental deletion. |
| `docs/` | Supporting documentation for architecture, API, usage, and this overview. | Add future drill-downs for new boundaries or workflows here. |
| `tests/` | Empty directory reserved for automated tests. | Add integration/unit tests once concrete logic exists. |
| `src/` | Source packages under `xiaoshuo_ai` following the src layout. | Contains CLI, agents, memory, domain, storage, and utility modules. |

## `src/xiaoshuo_ai` modules
- `cli.py`: Entry point for the A-machine writing console, eventually wiring together configs, orchestrator, and user prompts.
- `config/`: Loader logic grabs environment-aware settings to share Neo4j/Chroma credentials across modules.
- `core/`: Orchestrator, pipeline, and context builder coordinate chapter planning and agent execution steps.
- `agents/`: Planner, writer, summarizer, critic, editor, and compliance agents describe stage-specific Codex interactions and enforcement.
- `memory/`: Splits into `graph/` (Neo4j client, schema, queries) for hard memory and `vector/` (Chroma client, collections) for soft memory.
- `domain/`: Models and validators define the story domain, ensuring incoming data matches expected structures.
- `storage/`: Local persistence helpers capture snapshots and reusable files on the writing machine.
- `utils/`: IDs, time helpers, retry wrappers, and logging utilities shared across modules.

## Memory strategy
Hard memories live in Neo4j (`memory/graph/`), recording structured relationships (chapters, characters, timelines). Soft memories rely on Chroma (`memory/vector/`) to embed textual artifacts for similarity search. Keep connectors separate so data can be synchronized to whichever service suits a workflow.

## Prompt management
Prompts under `prompts/book`, `prompts/chapter`, and `prompts/compliance` are the curated messages sent to Codex. Each stage (like `01_outline` or `03_edit`) should have a text file describing the prompt structure, expected inputs, and any guardrails. Treat this directory as the source-of-truth for future prompt tuning.

## Expansion suggestions
- Add integration tests that exercise `scripts/healthcheck_memory` and the orchestrator once its workflow exists.
- Document environment hand-off between A-machine and B-machine (networking, authentication) alongside the configs.
- Introduce templates or `jinja` prompt builders for `prompts/` to keep instructions consistent as they evolve.
'@
        }
        default {
            return @"
# Placeholder for $RelativePath
TODO: populate this file with the desired skeleton content.
"@
        }
    }
}

$dirCreated = 0
$filesCreated = 0
$filesSkipped = 0
$backups = 0

foreach ($dir in $directories) {
    $fullDir = Join-Path $root $dir
    if (-not (Test-Path $fullDir)) {
        New-Item -ItemType Directory -Force -Path $fullDir | Out-Null
        $dirCreated++
    }
}

foreach ($relative in $files) {
    $fullPath = Join-Path $root $relative
    $parentDir = Split-Path -Parent $fullPath
    if (-not (Test-Path $parentDir)) {
        New-Item -ItemType Directory -Force -Path $parentDir | Out-Null
    }

    $content = Get-Template -RelativePath $relative
    if (Test-Path $fullPath) {
        if ($Force) {
            $ts = Get-Date -Format yyyyMMddHHmmss
            $backup = "$fullPath.bak-$ts"
            Copy-Item -Path $fullPath -Destination $backup -Force
            $backups++
            $content | Set-Content -Encoding utf8 -Path $fullPath
            $filesCreated++
        }
        else {
            $filesSkipped++
        }
    }
    else {
        $content | Set-Content -Encoding utf8 -Path $fullPath
        $filesCreated++
    }
}

Write-Host "Scaffold complete; directories created: $dirCreated, files created: $filesCreated, skipped: $filesSkipped, backups: $backups."
Write-Host "OK"
