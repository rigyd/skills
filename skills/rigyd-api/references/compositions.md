# Compositions and prototype submission

HTTP paths below are relative to `/api`; all require customer authentication. Contract: [generate](https://docs.rigyd.com/compositions/generate.md), [composition state](https://docs.rigyd.com/jobs/compositions.md), [editing](https://docs.rigyd.com/compositions/edit.md).

## composition.generate

`POST /compositions/generate` creates an automatic composition and starts its prototype. This is a composite convenience operation, not just planning.

Required `prompt` and `robot_task`: nonempty strings, each at most 2000 characters. Use the actual task supplied by the caller; do not invent robot behavior to fill a template. Optional fields:

| Field | Contract |
| --- | --- |
| `asset_class` | `auto` (default), `rigid`, `articulated` |
| `generation_method` | `auto` (default), `procedural` (Build), `generative` (Tripo Generate) |
| `geometry_builder` | `codex` (default) or `responses`; applies to Build |
| `auto_submit` | Boolean, default false; true includes subsequent conversion |
| `negative_prompt` | At most 255 characters |
| `physical_context` | Object: positive `mass_kg`; `dimensions_m` with positive `length`, `width`, `height` (subset allowed); `materials` string array; `fixed_base` boolean |
| `images` / `images[]` | Multipart files: 0, 1 or 4 JPEG/PNG/WebP, at most 10 MB each; four ordered front/right/back/left |

Use JSON without images, multipart with images. JSON-encode object fields in multipart; booleans can be strings `true`/`false`. Do not send image URLs in place of uploads. Creation returns `201` with `data.id` (composition), not a conversion ID. Return that handle; wait only when requested. With `auto_submit=false`, the workflow stops at a reviewable prototype. With true, follow `conversion_job_id` after conversion is created.

Rigid describes simulation behavior, not a method: Auto may choose either method. Generate cannot deliver working articulation. Legacy deformable/mixed briefs can be simplified to rigid/articulated with `simplified_from`; expose that limitation when it affects the request. A prototype is not evidence that deformability or the complete environment was simulated.

## composition.get / composition.list

`GET /compositions/:id` returns the full owned composition. `GET /compositions?page=1&pageSize=25` returns `data` array, newest first, with page size capped at 100 and **no pagination metadata**. The list omits geometry source and artifact manifest; get a single record for those.

Automatic records expose `workflow.status`, `stage`, `progress`, `error`, `assumptions`. Interactive records may have `workflow=null`. Read `geometry_alpha.status` for Build; `rigid_prototype.status`, `stage`, `model` for Generate. Use `GET /compositions/:id/geometry-alpha` to refresh an interactive Build. Media IDs in images/prerenders are distinct from document IDs.

## prototype.start / prototype.convert

Both bind to `POST /compositions/:id/submit`, JSON body optionally containing `generation_method` and `asset_license` (string ≤200 characters, default proprietary). Prototype start also accepts `geometry_builder`. Inspect the composition first:

| Existing state | What `/submit` does |
| --- | --- |
| Draft and Physics brief, no ready prototype | Starts a prototype; `202` composition; prototype price applies |
| Build ready with stored, valid `geometry_alpha.artifacts` | Converts those artifacts; `202` conversion job; `authored_to_simready` applies |
| Build ready source but no exported artifacts | `409`; export/upload artifacts if within the requested workflow |
| Tripo completed at `prototype_ready` with model | Converts that model; `202` conversion job; `authored_to_simready` applies |
| Build failed/non-ready | May start another paid attempt; it is not a conversion-only call |
| Active attempt | Conflict; inspect existing work |

For a conversion-only request with no ready artifact/model, return the unmet prerequisite. Do not start another prototype. On a known existing conversion, use its handle for status/download rather than repeating `/submit`. Read the actual response shape to identify which resource was returned.

For prototype-only work with an already ready prototype, return that existing handle. Calling `/submit` on it can convert it instead. Revision or a new attempt needs the corresponding requested operation; do not turn a prototype start into conversion merely because the endpoint can do so.

Existing attempts keep their recorded method; a conflicting specific method gives `409`. Explicit method changes use `PATCH /compositions/:id` and can clear old artifacts/references and create a new paid attempt. Geometry revisions use the separate operation reference.
