# Results, evidence and asset simulations

Contracts: [download](https://docs.rigyd.com/jobs/download.md), [simulation](https://docs.rigyd.com/conversions/simulate.md), [report lifecycle](https://docs.rigyd.com/reference/job-lifecycle.md), [validation](https://docs.rigyd.com/simready-validation/overview.md).

## result.download

Owned completed conversion: `GET /conversions/:id/result?format=usd|mjcf|all`; default all. Read response content type. Current responses stream ZIP bytes with authentication. Legacy records without packages can instead return JSON `{data:{url}}`. Fetch the returned storage URL without forwarding the Rigyd bearer token to another host. Handle redirects with the same credential boundary; do not blindly forward sensitive headers.

Save/extract into the requested destination with the full relative directory tree. Current USD uses `usd/<name>/<name>.usd` plus payloads/textures; MJCF uses `mjcf/<name>.xml` plus meshes/textures. `<name>` is derived from the composition prompt or uploaded filename (e.g. `rolling_iv_pole_five.xml`). It is not the caller's asset key. Existing jobs may use older layouts. Inspect the archive rather than predicting or hard-coding a path, and record the actual entrypoint per asset key in the caller's state. Report usable entrypoint paths. A missing requested MJCF package returns `404`; do not fabricate one or silently substitute USD.

For shared/gallery assets, use public `output.usd_package`/`mjcf_package` URLs or available public model URLs. The authenticated `/conversions/:id/result` endpoint remains owner-only; gallery membership does not grant it.

## result.inspect

Use actual normalized top-level `report` fields (`geometry`, `mass`, `materials`, `contact`, `bodies`, `joints`, `checks`, `validation`, provenance), not an assumed `report.pipeline` nesting. Older fields may be absent; absence means unmeasured. Output includes `usd_package` as well as model/MJCF links when available.

For validation, branch on `validation.spec_release`; summarize `targeted_profiles` and each target's `profiles[name].status`. `profiles_passing` includes incidental passes, and `overall` is not the requested profile verdict. A completed job or preview does not certify conformance, simulator import, joint behavior or a complete scene. Include relevant `optional_unmet` and failed/unmeasured checks.

For scene handoff, report delivered dimensions/scale and source, metres/Z-up frame, the established front direction, bodies and joint origins/axes/limits relative to the delivered zero pose. Build prototype GLB is metres/Y-up. Do not apply an extra unit/axis conversion silently. Where relevant, distinguish `remesh_refit` collision from per-part decomposition; preserve press-joint `stiffness`/`return_force_n` evidence. USD assets' package dependencies must remain together.

## Combining MJCF assets in one scene

Each MJCF file is a standalone test world for one asset, not a scene fragment. Scene assembly is the caller's work, but warn about these properties up front when a caller is building a scene:

- **Own ground plane.** Every file has `<geom name="ground" type="plane">` in `worldbody`. Keep one floor for the scene and drop the per-asset ones.
- **Colliding names.** Mesh, material, texture and geom names repeat across assets (`material_0`, `visual_0`, `visual_<body>_0`, `collision_0`). Each file also has an unnamed top-level `<default>` geom class carrying that asset's friction/solref. Prefix every name and reference per asset, or use MuJoCo `<attach>`/mjSpec attach with a `prefix` (plain `<include>` does not prefix). Move each asset's defaults into a named class applied to that asset's geoms; otherwise one asset's defaults silently apply to every geom.
- **Friction is a pair property.** MuJoCo combines contacting geoms by taking the element-wise maximum friction (unless `priority` differs). A default floor (friction 1.0) therefore overrides lower tuned friction on every asset. Set the floor to the intended surface friction, or give asset geoms a higher `priority`.
- **Wheels and casters are solid.** Only joints Build authored for an articulated asset move. Rigid assets, Generate assets and any part not articulated have no wheel joints. A pushed cart, IV pole or overbed table slides on contact friction and can tip over when the floor grips it. `fixed_base:false` means a free body, not rolling. If rolling matters, request articulation and name the wheels/casters as continuous joints. Report it as a limitation; do not promise it from the prompt alone.
- **Facing.** No explicit "front" field is delivered. Build geometry is authored with its front toward +Z in Y-up, which the conversion maps (`(x,y,z)→(x,−z,y)`) to **−Y in the delivered Z-up USD/MJCF**. Treat this as a convention to verify, not a guarantee. Generate and uploaded assets have no facing convention. Confirm with the canonical captures (`mesh_front` is the +Z/Y-up view, `geometry_alpha.artifacts.captures`), joint origins/axes (drawer slide direction, door hinge side), or a rendered check. Then state the front direction you established in the handoff.

## simulation.start

`POST /conversions/:id/simulate`, authenticated JSON optionally `{scene:"demo"}` or `{scene:"drop"}`. Source must be a completed asset conversion (`409` otherwise); a simulation source is invalid (`422`). Inspect `simulate_usd` pricing, including zero.

`202` creates a **new simulation job ID**, with `source_job_id` and charged amount. Return the new handle; poll `GET /conversions/<simulation-id>` only when waiting was requested. On completion, inspect available `output.sim_video`, `sim_gif`, `sim_log`; parent detail can also expose simulations. Preserve missing outputs as missing.

This predefined individual-asset demo/drop operation has no multi-asset scene input. Building, importing and testing an assembled environment belongs to the caller's simulator/orchestrator. Do not call this automatically after a download or claim its success proves scene-level behavior.
