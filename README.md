# Rigyd agent skills

Portable customer asset operations for Claude Code and Codex. The same `skills/rigyd-api` directory uses the Agent Skills format; optional `agents/openai.yaml` supplies Codex UI metadata.

Available on [skills.sh](https://skills.sh/rigyd/skills/rigyd-api).

## Install

```sh
npx skills add rigyd/skills --skill rigyd-api -a claude-code -a codex
```

Inspect available skills without installing:

```sh
npx skills add rigyd/skills --list
```

Alternatively copy `skills/rigyd-api` to `.claude/skills/rigyd-api` for Claude Code or `.agents/skills/rigyd-api` for Codex in the target project. Personal installs use `~/.claude/skills` or `~/.agents/skills` respectively. Restart/refresh the host after installation.

Invoke `/rigyd-api` in Claude Code or `$rigyd-api` in Codex, or describe a Rigyd asset task for automatic selection. Supply `RIGYD_API_KEY` through the host's existing secret environment for authenticated operations. Anonymous gallery/shared reads need no key.

Example: “Use rigyd-api to inspect conversion job `<id>` and report its status and targeted validation profiles.” This is a read operation; the skill also supports paid creation/conversion, editing, artifact upload, download, simulation and explicitly requested sharing.

## Package boundaries

The skill exposes 25 customer HTTP bindings through seven focused references. It does not install an SDK, start an MCP server, change account/billing settings or assemble a scene implicitly. Orchestrators retain their own state, budget, placements and simulator tests. Public documentation remains the authoritative parameter contract.

Published under the [MIT license](LICENSE). Validation evidence lives in [VALIDATION.md](VALIDATION.md), outside the loaded skill.

Current release: [v1.0.0](https://github.com/rigyd/skills/releases/tag/v1.0.0). Every public documentation page the skill links to is live, including interactive editing, geometry artifacts, sharing, gallery reads and orchestration.

skills.sh tracks installations through the Skills CLI and lists skills automatically. Listing and ranking can lag behind repository publication.
