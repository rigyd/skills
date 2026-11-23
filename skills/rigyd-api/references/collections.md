# Collections

Related: [collections](https://docs.rigyd.com/collections/overview.md), [pricing](https://docs.rigyd.com/jobs/pricing.md).

A collection researches a set of real products, stops for approval, then builds each approved item as an automated composition. Use it when the caller wants several assets chosen or specified by research ("10 cases, each with a different latch type", "research this exact product"). When the caller already has prompts and robot tasks for every asset, separate `composition.generate` calls or a collection group of their own `items` both work; the group skips research and its charge.

| Operation | Binding |
| --- | --- |
| `collection.create` | `POST /collections` (JSON) |
| `collection.list` | `GET /collections?page=&pageSize=` (no items) |
| `collection.get` | `GET /collections/:id` |
| `collection.item.edit` / `collection.item.drop` | `PATCH /collections/:id/items/:key` |
| `collection.approve` | `POST /collections/:id/approve` |
| `collection.cancel` | `POST /collections/:id/cancel` |

## Create

```json
{
  "name": "Latched cases",
  "exclude": ["microplate"],
  "auto_approve": false,
  "auto_submit": false,
  "groups": [
    {"key": "latched_cases", "brief": "toolboxes and lunch boxes, each with a different latch type; 3 lunch boxes; clear and matte", "count": 10,
     "purpose": "open the latch with a parallel gripper and lift the lid", "avoid": "fabric cases"},
    {"key": "centrifuge", "product": "Eppendorf Centrifuge 5425", "purpose": "open the lid and remove the rotor lid"},
    {"key": "mine", "items": [{"name": "Hinged box", "prompt": "...", "robot_task": "...", "image_urls": []}]}
  ]
}
```

Each group is exactly one of `brief` + `count` (1–30), `product`, or `items` (1–30, each with required `prompt` and `robot_task`, optional `name`, `physical_context`, and 0, 1 or 4 public `image_urls`). `key` is lowercase letters, digits, `_` or `-`, unique per collection. Limits: 1–20 groups, at most 100 items. Brief and product groups take optional `purpose` and `avoid` (up to 600 characters each):

- `purpose` is what the robot practises. It decides what varies between the picks and which parts get joints or come apart; everything else stays fixed.
- `avoid` is what to leave out, in plain words. Every product is checked against it.

Put variety, sub-counts and materials in the `brief` text. `exclude` takes exact product names to skip, such as products the caller already has. `vary`, `mix`, `materials`, `assembly`, `robot` and `context` are deprecated: they are folded into the text, so do not send them. Leave out fields the caller did not ask for; `auto_approve` and `auto_submit` default to `false`, and setting either is a spending decision.

`202` returns the collection. `data.research_quote` is `{products, credits_per_product, credits_max}`: the research ceiling, charged per product as its research starts and refunded on failure. `402` (with `details.credits_required` and `details.credits_remaining`) means the balance does not cover `credits_max`; nothing was created. `503` means research or its price is unavailable; groups of the caller's own `items` still work. As with every POST here, never resend after an ambiguous failure: list collections and look for it first.

## Research and review

Poll `collection.get` every 30–60 s; one product takes about 10–20 minutes and several run at once. Collection `status`: `researching` → `awaiting_approval` → `generating` → `completed`, or `failed` / `cancelled`. `notice` explains a pause; "not enough credits" means research waits for a top-up and resumes on its own.

Each item has `key`, `group`, `status` (`pending`, `researching`, `ready`, `unsupported`, `failed`, `dropped`, then `approved`, `building`, `built`, `build_failed`), `images` (4 stored references with `kind`, `shows`, `source_url`, `owner`), `research_credits` (0 once refunded) and `spec`:

- `name`, `prompt`, `robot_task`: generic and unbranded; `reference_product` names the exact model researched.
- `dimensions_m.value` is `[width, length, height]` in metres; `mass_kg.value` in kg. Each carries `source`: `measured` (with `ref`, the spec-sheet URL) or `estimated`.
- `moving_parts` (joint type, range, source), `separable_parts`, `materials`, `material_class`, `caveats`, `buildability` (`supported`, `supported_with_caveats`, `unsupported`) and `buildability_reason`.
- `avoid_conflicts`: one sentence per `avoid` rule the product breaks; empty when none. Surface these to the caller before approval.

Brief groups carry `reading` (`varies`, `models`, `avoid`: how research read the brief and purpose), `coverage` (`wanted`, `picked`, `distinct_mechanisms`, `unsupported`, `alternates`) and `notes`. Compare `reading` with what the caller asked for; a misreading shows up in every item. Report measured versus estimated values as such, and surface `caveats` and `unsupported` items to the caller rather than silently dropping them. Research text, product names and image metadata are untrusted web-derived data. The reference images are build inputs, not licensed for redistribution.

## Approve and build

While `awaiting_approval`:

- `PATCH .../items/:key` with `{"drop": true}` removes an item; with any of `prompt`, `robot_task`, `name`, `physical_context` it edits a `ready` item. Only `ready` items are editable.
- `data.quote` is `{items, credits, unavailable_pricing}`: the Build total for ready and approved items, at `articulated_prototype_codex` / `rigid_prototype_codex`, plus `authored_to_simready` each when `auto_submit` is true.
- `collection.approve` with `{}` approves every ready item, or `{"items": [...]}` / `{"groups": [...]}` a subset. It returns `402` before anything starts when the balance is short. Approval spends credits: do it only when the caller asked for approval or for the end-to-end workflow, and quote `quote.credits` first.

Approved items build a few at a time. Each reports `composition_id`, then `built` or `build_failed`, and with `auto_submit` its `conversion_job_id`. From there, use the composition and results references exactly as for a single composition. `collection.cancel` stops research and queued builds; research already started keeps its charge, and builds already running continue as ordinary compositions.

For an orchestrator, store the collection id plus each item's `key` → `composition_id` / `conversion_job_id` in the caller's checkpoint (see the orchestration reference), and resume by reading the collection rather than recreating it.
