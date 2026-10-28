# Build geometry and exported artifacts

Revision is documented in [compose an asset](https://docs.rigyd.com/compositions/generate.md#revise-build-geometry). The scaffold, export and artifact-upload contract below is not in the public docs; this reference is the contract. These are customer operations on an owned composition, not worker callbacks or an arbitrary asset-ingestion API.

## prototype.inspect / prototype.revise

`GET /compositions/:id/geometry-alpha` refreshes Build state and returns the composition. `geometry_alpha.status=building|ready|failed`; ready state exposes source, manifest and its recorded `ground_version`. GET can refresh/reconcile server state; it does not request another prototype.

`POST /compositions/:id/geometry-alpha` accepts optional `geometry_builder=codex|responses`, first-attempt `generation_method=auto|procedural|generative`, and `feedback` (≤2000 characters). A first attempt honors method/Auto via prototype routing; this legacy path does not always force Build. To revise, require a ready procedural prototype and send nonempty feedback. Preserve its original builder and class. A valid revision reuses its prototype reservation; failed-settled attempts or an explicit new attempt can charge again. Do not apply a separate revision price or assume all retries are free.

Ready geometry without feedback gives `409` asking for revision feedback. Feedback without a ready Build gives `409`; Generate cannot be revised through this geometry endpoint. Changing class requires a separately requested new attempt. Return the `202` composition handle unless waiting was requested.

## scaffold.get / artifact.export

`GET /geometry-alpha/scaffold?ground_version=<recorded version>` requires authentication and returns `{data:{version,html}}`. Omit version only for a new default ground. An unknown version returns `422`. Load existing source with its saved ground rather than upgrading it implicitly.

For a requested artifact export, run that HTML/source in an isolated iframe with WebGL, using the message protocol below. The host supplies the Three.js module sources; the ground does not fetch dependencies itself. Do not give generated geometry access to secrets or the surrounding application. The scaffold produces the matching GLB, manifest and canonical captures in the delivered zero pose. Export is local work, not another HTTP generation endpoint. If the host lacks a browser/export capability, return the ready handle and exact missing export prerequisite; do not replace Build geometry by regenerating it with Tripo.

The pinned runtime is Three.js revision 183. Parent-to-iframe `rigyd-geometry-load` carries `groundVersion`, `assetSource`, `assetClass`, `threeSource` (`three.module.min.js`), `threeCoreSource` (`three.core.min.js`) and matching `exporterSource` (`examples/jsm/exporters/GLTFExporter.js`). The ground creates module blobs internally. Verify incoming messages come from that iframe. Wait for `rigyd-geometry-ready`, then send `rigyd-geometry-export-glb`; `rigyd-geometry-glb` returns `buffer` (ArrayBuffer), `manifest`, `captures` (`{role,data_url}`). Save the buffer and decode captures to the canonical PNG filenames. A `rigyd-geometry-error` ends that export attempt; retain the prototype handle.

## artifact.upload

`POST /compositions/:id/geometry-artifacts`, multipart:

| Field | Contract |
| --- | --- |
| `glb` | Required nonempty GLB, ≤500 MB |
| `manifest` | Required object or JSON string; nonempty `links`; class/link ownership must match the ready geometry |
| `artifact_sha256` | Optional hash of the exact uploaded GLB bytes; server verifies if supplied |
| `captures` | Optional repeated PNG files named `mesh_front.png`, `mesh_right.png`, `mesh_back.png`, `mesh_top.png` |

Ready `geometry_alpha` is required (`409` otherwise). Manifest coordinates are metres and Y-up (`unit=m`, `up_axis=Y` when present); mesh data must match the manifest and have geometry per link. Texture maps must use `TEXCOORD_0`; other UV sets are refused. Generate the hash and manifest from the exact exported bytes/pose, not separately estimated geometry.

`201` returns composition with `geometry_alpha.artifacts`: GLB URL/media ID/size/hash, captures, manifest and uploaded timestamp. Upload replaces stored artifacts; it does not submit a conversion. Conversion is a separate requested `/submit` operation after stored artifacts are ready. Converted USD/MJCF/report coordinates are Z-up: retain that distinction in scene handoff.
