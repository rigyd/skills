# Results, evidence and asset simulations

Contracts: [download](https://docs.rigyd.com/jobs/download.md), [simulation](https://docs.rigyd.com/conversions/simulate.md), [report lifecycle](https://docs.rigyd.com/reference/job-lifecycle.md), [validation](https://docs.rigyd.com/simready-validation/overview.md).

## result.download

Owned completed conversion: `GET /conversions/:id/result?format=usd|mjcf|all`; default all. Read response content type. Current responses stream ZIP bytes with authentication. Legacy records without packages can instead return JSON `{data:{url}}`. Fetch the returned storage URL without forwarding the Rigyd bearer token to another host. Handle redirects with the same credential boundary; do not blindly forward sensitive headers.

Save/extract into the requested destination with the full relative directory tree. Current USD uses `usd/<name>/<name>.usd` plus payloads/textures; MJCF uses `mjcf/<name>.xml` plus meshes/textures. Existing jobs may use older layouts, so inspect the archive rather than hard-code one root. Report usable entrypoint paths. A missing requested MJCF package returns `404`; do not fabricate one or silently substitute USD.

For shared/gallery assets, use public `output.usd_package`/`mjcf_package` URLs or available public model URLs. The authenticated `/conversions/:id/result` endpoint remains owner-only; gallery membership does not grant it.

## result.inspect

Use actual normalized top-level `report` fields (`geometry`, `mass`, `materials`, `contact`, `bodies`, `joints`, `checks`, `validation`, provenance), not an assumed `report.pipeline` nesting. Older fields may be absent; absence means unmeasured. Output includes `usd_package` as well as model/MJCF links when available.

For validation, branch on `validation.spec_release`; summarize `targeted_profiles` and each target's `profiles[name].status`. `profiles_passing` includes incidental passes, and `overall` is not the requested profile verdict. A completed job or preview does not certify conformance, simulator import, joint behavior or a complete scene. Include relevant `optional_unmet` and failed/unmeasured checks.

For scene handoff, report delivered dimensions/scale and source, metres/Z-up frame, bodies and joint origins/axes/limits relative to the delivered zero pose. Build prototype GLB is metres/Y-up. Do not apply an extra unit/axis conversion silently. Where relevant, distinguish `remesh_refit` collision from per-part decomposition; preserve press-joint `stiffness`/`return_force_n` evidence. USD assets' package dependencies must remain together.

## simulation.start

`POST /conversions/:id/simulate`, authenticated JSON optionally `{scene:"demo"}` or `{scene:"drop"}`. Source must be a completed asset conversion (`409` otherwise); a simulation source is invalid (`422`). Inspect `simulate_usd` pricing, including zero.

`202` creates a **new simulation job ID**, with `source_job_id` and charged amount. Return the new handle; poll `GET /conversions/<simulation-id>` only when waiting was requested. On completion, inspect available `output.sim_video`, `sim_gif`, `sim_log`; parent detail can also expose simulations. Preserve missing outputs as missing.

This predefined individual-asset demo/drop operation has no multi-asset scene input. Building, importing and testing an assembled environment belongs to the caller's simulator/orchestrator. Do not call this automatically after a download or claim its success proves scene-level behavior.
