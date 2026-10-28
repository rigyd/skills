# Rigyd API skill validation

Release: **v1.0.0**, reviewed 28 October 2026. Portable source: `skills/rigyd-api`. Publisher: `rigyd/skills`; license: MIT.

## Contract and packaging

The skill covers all **25 customer HTTP bindings** in the reviewed API, including interactive editing, scaffold/artifact operations, sharing and public gallery reads. Five worker-only bindings are excluded. Operation references were checked against the controllers and response formatters at API revision `26fc24d`; docs baseline was `d140bf5`, followed by the local synchronization in this workspace.

Skill Creator's validator passes. All seven local reference links and their public Markdown targets resolve against the built docs. `npx skills add . --list` discovers exactly one `rigyd-api` skill. The skill folder contains no credentials, private workspace paths or private-repository dependencies. The release ZIP contains only the portable skill folder and its optional Codex metadata.

The Astro docs build passes with 23 pages. The public docs are limited to API reference: sharing, gallery, geometry scaffold/export and orchestration guidance live only in the skill references, which state that they are the contract. All three generated agent indexes exclude account, billing and internal endpoints. Every documentation link in the skill returns 200.

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

## Public-content handling (W011)

The skill explicitly treats public gallery/shared metadata as untrusted data. Embedded instructions and authority claims cannot authorize credentials, mutations, spending or different tool use. IDs/slugs stay within encoded API path segments; filenames cannot choose output paths; requested downloads use validated structured output URLs rather than links in prose. Agent handoffs retain the content's source and untrusted-data status.

Four adversarial cases passed independently in Claude Code and Codex: metadata requesting credential disclosure and simulation, gallery text requesting command execution/sharing with a traversal filename, a shared asset with an invalid package URL and an injected workaround, and a hostile slug requesting an authenticated PATCH. Request plans preserved valid listing/inspection and the legitimate HTTPS package download. Local actions were reviewed for credential access, command execution and writes outside the caller's destination. No live API requests or credential disclosures were performed.

```sh
python3 tests/check_public_content.py tests/results/claude-public-content.json
python3 tests/check_public_content.py tests/results/codex-public-content.json
```

These checks demonstrate the tested instruction boundaries, not prompt-injection immunity. Public content exposure remains by design, so W011 may still be reported. A fresh external audit verdict has not been confirmed.

## Multipart integration check

Claude Code generated a standalone Node integration using the final multipart guidance. That temporary integration was executed against a loopback HTTP mock under Node **v24.15.0**. The mock inspected actual multipart file bytes, filenames, boundaries, JSON declarations, advanced options and Authorization headers.

Five scenarios passed: paid conversion, zero-priced conversion, omitted pricing without submission, ambiguous POST failure without retry, and missing reported charge retained as unknown. Each successful attempt made one pricing read and one conversion POST; no simulation, sharing or polling followed. Only a fixture key was used, and no production requests were made. The generated integration is evaluation material, not a shipped SDK or skill runtime helper.

## Field-feedback revision (28 October 2026)

An agent that used the skill to provision a multi-asset MuJoCo scene reported 14 gaps. Each was checked against the API controllers (`composer.ts`, billing routes) and the Physiq MJCF exporters before changing the skill:

- `/compositions/generate` returns `202`, also for a coalesced in-flight duplicate. Any `2xx` is treated as accepted, and the generate fixture in `tests/cases.json` now uses `202`.
- `conversion_job_id` is top-level on the composition (not under `workflow`), shown with a completed-response example.
- Where charges are reported: Generate `rigid_prototype.credits_charged`, conversion/simulation `credits_charged`. A Build charge is not reported. Actual spend can be checked with `GET /me` balance or the browser billing history.
- Codex vs Responses trade-off, and a worked prototype-price table for Auto routing.
- New "Combining MJCF assets in one scene" guidance: per-file ground planes, colliding names and unnamed defaults, max-friction contact pairing, non-rolling casters, and the Build facing convention (+Z Y-up → −Y Z-up, to be verified).
- Credentials in non-interactive shells and `~/.config/rigyd/config.json`, a minimal curl sequence, per-asset `robot_task`, and prompt-derived entry-point names.

Offline with-skill vs previous-skill evaluation in Claude Code (three cases: scene pricing, status script, MJCF scene merge): **17/17** assertions for the revision vs **13/17** for the previous skill. The previous skill missed the Codex trade-off, the charge fields/balance check and the non-interactive shell note, and quoted `201`. The existing behavior, atomic and public-content checks above still pass. Exporter changes that remove these MJCF merge issues at the source are tracked separately in Physiq.

## Limits and release gates

These checks establish instruction routing, request-plan behavior and the tested multipart integration. They do not establish live generation quality, production availability, actual geometry export, simulator import or multi-asset scene correctness. Browser export needs the pinned rendering ground and Three.js runtime; durable exactly-once paid submission remains an API limitation.

The repository is published as `rigyd/skills` under MIT. Skills CLI 1.7.4 discovered exactly one skill from the remote repository, and a clean project install for Claude Code and Codex succeeded. All nine files in both installed skill folders matched the published source byte-for-byte. The [skills.sh directory page](https://skills.sh/rigyd/skills/rigyd-api) returned 200 and displayed the skill instructions.

Tagged v1.0.0 after the synchronized docs were deployed and every linked page returned 200. No native marketplace submission has been created.
