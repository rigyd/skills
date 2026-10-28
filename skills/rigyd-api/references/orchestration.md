# Asset provisioning for an orchestrator

Guide: [agent orchestration](https://docs.rigyd.com/guides/agent-orchestration.md).

Rigyd provides per-asset operations. The caller owns scene specifications, unique asset definitions, instances/transforms, dependency ordering, robot/controllers, import, budget, concurrency and environment tests. Do not impose a scene recipe, object category, simulator, provider, fixed concurrency or budget when the caller has its own policy.

Use the caller's checkpoint format. If none exists and multi-asset orchestration was requested, a small JSON mapping is sufficient:

```json
{
  "assets": {
    "cabinet": {
      "composition_id": "cmp-id",
      "conversion_id": "job-id",
      "operation": "prototype.convert",
      "attempt": 1,
      "status": "running",
      "reported_charge": null,
      "files": []
    }
  },
  "instances": [
    {"asset_key": "cabinet", "transform": "caller-owned"}
  ]
}
```

These are caller state fields, not Rigyd API arguments. `conversion_id` comes from the composition's top-level `conversion_job_id`. `reported_charge` is filled only where the API reports one (see "Where charges appear" in the skill).

Give each asset its own `robot_task`: the part of the scene task that involves that object. A shared scene-wide task can mislead routing; see the composition reference. Store requested parameters/estimated stage costs where needed for reconciliation. An unknown charge stays null. One completed asset definition may serve multiple scene instances without regenerating it.

On resume, inspect known handles and reuse completed work. Continue only the requested missing operations. Retain a failed asset independently so it does not invalidate completed siblings. On deadline or partial failure, return the mapping and unmet prerequisites. Restarting the process must not automatically repeat accepted submissions.

Saving an ID after acceptance reduces duplicate work but cannot close the crash window between acceptance and persistence. Rigyd does not offer durable customer submission idempotency here. Report ambiguous acceptance and let the caller reconcile it; do not claim exactly-once execution or invent `Idempotency-Key` support.

Budget each separately priced stage using current available keys. Auto can select a different prototype price, and prototype conversion/simulation are separate charges. Respect the caller's ceiling before dispatch; absent budget policy is not unlimited spending authorization. Use actual amounts when returned, without assuming refunds or unreported costs.

For handoff, provide per-asset entrypoint paths (read from each archive), package dependencies, source/license, delivered frame/units/scale, front direction, joint contract and validation evidence. When MJCF files will share one scene, pass on the merge caveats in the results reference: per-file ground planes, colliding names and default classes, max-friction contact pairing, and non-rolling casters. Scene transforms belong to instances. Run assembled-environment tests in the caller's simulator when requested and available. A per-asset conversion or demo/drop PASS does not establish that several assets interact correctly in that environment.
