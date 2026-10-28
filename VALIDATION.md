# Rigyd API skill validation

Release candidate: **v0.1.0**, reviewed 28 October 2026. Portable source: `skills/rigyd-api`. Publisher: `rigyd/skills`; license: MIT. Tagged release and expanded public docs deployment remain pending.

## Contract and packaging

The skill covers all **25 customer HTTP bindings** in the reviewed API, including interactive editing, scaffold/artifact operations, sharing and public gallery reads. Five worker-only bindings are excluded. Operation references were checked against the controllers and response formatters at API revision `26fc24d`; docs baseline was `d140bf5`, followed by the local synchronization in this workspace.

Skill Creator's validator passes. All seven local reference links and their public Markdown targets resolve against the built docs. `npx skills add . --list` discovers exactly one `rigyd-api` skill. The skill folder contains no credentials, private workspace paths or private-repository dependencies. The release ZIP contains only the portable skill folder and its optional Codex metadata.

The Astro docs build passes with 27 pages. New interactive, geometry, sharing, gallery and orchestration pages have Markdown exports. All three generated agent indexes exclude account, billing and internal endpoints. These changes are local and need deployment before the new public links are advertised as live.

## Independent host evaluation

The same instruction package was installed into isolated projects using `.claude/skills/rigyd-api` and `.agents/skills/rigyd-api`. Each host independently mapped raw fixtures to request plans, with real Rigyd credentials removed and production requests prohibited. The evaluator received user requests and response/state fixtures, without the checking scripts or expected answers.

| Host | Version | Result |
| --- | --- | --- |
| Claude Code | 2.1.308 | 12 workflow + 15 atomic-operation cases passed |
| Codex CLI | 0.146.1 | 12 workflow + 15 atomic-operation cases passed |

The cases check exact HTTP bindings, advanced option preservation, image ordering, full-brief replacement, resource handles, prototype/conversion boundaries, missing and zero prices, wrapped failures, terminal-state resumption, anonymous gallery reads, legacy downloads and cross-host credential boundaries. Report evidence and scene ownership were also reviewed in the returned plans.

Codex's first run with user configuration bypassed failed authentication before evaluation. The successful runs used its normal configured provider. Fixture checks accept legitimate multipart boolean strings and filename shorthand in conceptual request plans; supplied already-read state does not require redundant reads.

Recorded synthetic results are in `tests/results/`. Recheck them from this directory:

```sh
python3 tests/check_behavior.py tests/results/claude.json
python3 tests/check_behavior.py tests/results/codex.json
python3 tests/check_atomic.py tests/results/claude-atomic.json
python3 tests/check_atomic.py tests/results/codex-atomic.json
```

The final shared guidance explicitly states multipart file/object serialization, and the prototype reference explicitly stops prototype-only work at an already ready handle.

An additional Claude Code forward check after that boundary clarification passed: prototype-only work on an already ready composition returned the existing handle without a conversion POST. The fixture and result are `tests/ready-case.json` and `tests/results/claude-ready.json`.

## Multipart integration check

Claude Code generated a standalone Node integration using the final multipart guidance. That temporary integration was executed against a loopback HTTP mock under Node **v24.15.0**. The mock inspected actual multipart file bytes, filenames, boundaries, JSON declarations, advanced options and Authorization headers.

Five scenarios passed: paid conversion, zero-priced conversion, omitted pricing without submission, ambiguous POST failure without retry, and missing reported charge retained as unknown. Each successful attempt made one pricing read and one conversion POST; no simulation, sharing or polling followed. Only a fixture key was used, and no production requests were made. The generated integration is evaluation material, not a shipped SDK or skill runtime helper.

## Limits and release gates

These checks establish instruction routing, request-plan behavior and the tested multipart integration. They do not establish live generation quality, production availability, actual geometry export, simulator import or multi-asset scene correctness. Browser export needs the pinned rendering ground and Three.js runtime; durable exactly-once paid submission remains an API limitation.

The repository is published as `rigyd/skills` under MIT. Remote discovery and isolated installation for Claude Code and Codex are checked during publication. Deploy the synchronized docs before tagging v0.1.0; the expanded linked pages currently return 404. No tag or native marketplace submission has been created.
