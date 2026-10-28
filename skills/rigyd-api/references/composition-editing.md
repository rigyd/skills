# Interactive planning and editing

All operations require an owned composition except creation. Contract and complete editable brief schema: [interactive composition](https://docs.rigyd.com/compositions/edit.md). These operations return composition state, not a finished SimReady job, and currently do not reserve prototype credits.

| Operation | HTTP binding | Input / prerequisite | Result and stopping point |
| --- | --- | --- | --- |
| `composition.start` | `POST /compositions/start` | `input` nonempty ≤2000 characters; optional repeated multipart `images`, 0–4 JPEG/PNG/WebP ≤10 MB each | `201` composition with questions and `enough_info`; return questions/handle |
| `composition.answer` | `POST /compositions/:id/answer` | `answers` array of `{question_id, values, custom}` using returned question IDs/options | Questions with `enough_info=false` or a draft with `stage=draft`; brief is a separate operation |
| `composition.message` | `POST /compositions/:id/message` | `message` nonempty ≤2000 characters; existing draft required | Revised draft; may clear conversion/Tripo references when prompt changes |
| `composition.brief` | `POST /compositions/:id/brief` | Existing draft; empty JSON body sufficient | Ready Physics brief; `prompt_revised` may be true; no prototype starts |
| `composition.update` | `PATCH /compositions/:id` | Requested supported fields; active input changes conflict | Updated ready composition; inspect returned dependent state |
| `reference.create` / `reference.edit` | `POST /compositions/:id/prerender` | Existing draft; optional `instruction` ≤2000; `mode=fresh` generates, default `edit` uses an existing reference when possible | `201` composition plus `prerender`; reference image only |
| `reference.select` | `POST /compositions/:id/prerender/select` | `media_ids` ordered array (or single `media_id`) drawn from source images/prerenders of this composition | Updated composition; first reference also becomes primary; empty array clears selection |

The automatic 0/1/4 image-count rule does not apply to interactive start, which accepts up to four. Selection deduplicates media IDs, preserves order, rejects foreign IDs and clears conversion/Tripo references. It does not regenerate a prototype. Do not assume all edits clear existing Build source; use the returned state.

## Direct editable fields

`draft_prompt` ≤1024 characters (different from the 2000-character seed), `negative_prompt` ≤255, `generation_method=auto|procedural|generative`, `tripo_params`, `asset_brief`.

Tripo accepts `model_version` (`v3.1-20260211`, `v3.0-20250812`, `v2.5-20250123` at review), `pbr` boolean, `geometry_quality=standard|detailed`, `smart_low_poly` boolean. `face_limit` and `texture_quality` are platform-fixed; submitting custom values does not make them user controls.

`asset_brief` is normalized as a replacement object, not a deep partial patch. Read the current brief and merge the requested edits before sending it, preserving other supported fields. Supported content includes classification, `generation_plan`, confidence/reasoning, articulation hints, declared physics, image `proportion_contract` and `context_conflicts`; consult the linked schema for all fields and limits. Prompt fields derive from the effective composition draft/negative prompt, so edit those at top level.

Use `rigid` or `articulated` for current behavior. Legacy `deformable` is normalized to rigid and `mixed` to articulated with `simplified_from`. Articulation hints support revolute/prismatic/continuous joints, at most 12. Composer/brief dimensions use `length/width/height`, not upload-conversion's suffixed keys.

Changing a recorded generation method clears the old generation/artifact/linked-job state. Prompt, Tripo and brief input changes are rejected during active attempts. This operation does not itself reserve a new attempt; a later explicitly requested start may charge.

At 40 stored messages, the message endpoint returns `429` for conversation length. Backoff cannot shorten it. Return the limit rather than retrying forever or silently creating a new composition.
