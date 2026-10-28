# File conversion and job inspection

Contract: [file conversion](https://docs.rigyd.com/conversions/3d-to-simready.md), [formats](https://docs.rigyd.com/reference/supported-formats.md), [job retrieval](https://docs.rigyd.com/jobs/retrieve.md), [listing](https://docs.rigyd.com/jobs/list.md).

## conversion.submit

`POST /conversions`, multipart, authenticated. Required `file`: `.glb`, `.gltf`, `.fbx`, `.obj`, `.stl`, `.ply`, `.usd`, `.usda`, `.usdc`, `.usdz`, `.zip`. ZIPs need one unambiguous primary model and its relative dependencies. PLY must contain faces; point clouds/splats are refused before billing. Upload limit is 500 MB.

| Optional field | Contract |
| --- | --- |
| `description` | String ≤2000 characters; factual object/physics context |
| `declared` | JSON object/string: positive `mass_kg`, `volume_m3`, `wall_mm`; `dimensions_m` subset of `length_m`, `width_m`, `height_m`; `materials` string array; `construction=shell|solid`; supported `object_category` from docs |
| `asset_license` | Source license string ≤200 characters, default proprietary |
| `optimize` | Boolean, default false |
| `target_triangle_count` | Required with optimize true; integer 1000–1000000; invalid without optimize |
| `threshold` | Advanced collision concavity float |
| `llm_provider` | Advanced material-identification provider string |
| `skip_validation` | Advanced internal correctness-gate boolean; does not suppress SimReady scoring |

Expose supported advanced choices when requested; do not add overrides to ordinary conversion. Preserve explicit caller values. Declared physics outranks prose and inferred renders. Composer dimensions use unsuffixed keys; this endpoint uses suffixed keys. Default GLB skips preprocessing; optimized GLB and other formats preprocess.

Read `glb_to_simready` pricing before submission. `202` returns a conversion job with `id`, status (`queued`/`preprocessing`) and `credits_charged`. Return its handle; do not wait, download or simulate unless requested.

## job.get / job.list

`GET /conversions/:id` returns an owned conversion **or simulation** job with status, stage, progress, outputs, normalized report, charges and `simulations[]` when available. A composition ID is invalid here. Prototype generation is inspected through compositions.

`GET /conversions?page=1&pageSize=25&job_type=glb_to_simready,authored_to_simready` returns `data` array plus `meta:{page,pageSize,pageCount,total}`. Page size caps at 100. Default list excludes prototype-generation and simulation jobs. Request `job_type=simulate_usd` to list simulations; legacy converted history may have text/image/multiview job types. Detail returns the fuller report/output tree omitted from list records.

Waiting is a separate caller choice. Terminal job states are completed/failed. A completed conversion can contain validation failures: read report evidence before asserting fitness. A failed job is not permission to repeat a paid submission.
