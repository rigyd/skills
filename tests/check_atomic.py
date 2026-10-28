"""Check remaining atomic bindings: python3 tests/check_atomic.py result.json."""
import json
import sys
from urllib.parse import parse_qs, urlparse

cases = {case["id"]: case for case in json.load(open(sys.argv[1]))["cases"]}
expected = {
    "answer": ("POST", "/compositions/cmp-question/answer"),
    "message": ("POST", "/compositions/cmp-edit/message"),
    "brief": ("POST", "/compositions/cmp-brief-only/brief"),
    "select": ("POST", "/compositions/cmp-select/prerender/select"),
    "revise": ("POST", "/compositions/cmp-revise/geometry-alpha"),
    "geometry_status": ("GET", "/compositions/cmp-progress/geometry-alpha"),
    "scaffold": ("GET", "/geometry-alpha/scaffold"),
    "convert_ready": ("POST", "/compositions/cmp-stored/submit"),
    "file_conversion": ("POST", "/conversions"),
    "pricing": ("GET", "/conversions/pricing"),
    "jobs_list": ("GET", "/conversions"),
    "compositions_list": ("GET", "/compositions"),
    "sharing": ("PATCH", "/conversions/job-share/sharing"),
    "shared": ("GET", "/shared-conversions/job-public"),
    "gallery_list": ("GET", "/demo-assets"),
}
assert set(cases) == set(expected)
bodies = {}
queries = {}
for name, (method, suffix) in expected.items():
    requests = cases[name]["requests"]
    main = [r for r in requests if r["method"] == method and urlparse(r["url"]).path == "/api" + suffix]
    assert len(main) == 1, (name, "expected atomic operation not called exactly once")
    request = main[0]
    assert request["authentication"] == ("none" if name in ("shared", "gallery_list") else "rigyd"), name
    assert all(r is request or r["method"] in ("GET", "HEAD") for r in requests), (name, "extra mutation")
    if method == "GET":
        assert len(requests) == 1, (name, "read operation expanded")
    bodies[name] = json.loads(request["body_json"])
    queries[name] = parse_qs(urlparse(request["url"]).query)

assert bodies["answer"]["answers"] == [{"question_id":"q1","values":["medium"],"custom":"0.4 metres"}]
assert bodies["message"] == {"message":"make the shade wider"}
assert list(map(str, bodies["select"]["media_ids"])) == ["3", "2"]
assert bodies["revise"]["feedback"] == "increase hinge clearance"
assert bodies["revise"].get("geometry_builder", "responses") == "responses"
assert queries["scaffold"]["ground_version"] == ["rigyd-three-r183-alpha-12"]
assert bodies["convert_ready"]["asset_license"] == "CC0-1.0" and "job-converted" in cases["convert_ready"]["result"]
body = bodies["file_conversion"]
assert body["file"] in ({"file":"table.glb"}, "table.glb"), "Fixture upload may use a filename shorthand"
assert cases["file_conversion"]["requests"][-1]["encoding"] == "multipart"
assert body["optimize"] in (True, "true") and int(body["target_triangle_count"]) == 12000
assert float(body["threshold"]) == 0.06 and body["llm_provider"] == "azure"
assert body["skip_validation"] in (True, "true") and body["asset_license"] == "CC-BY-4.0"
declared = body["declared"]
if isinstance(declared, str):
    declared = json.loads(declared)
assert declared == {"mass_kg":3,"dimensions_m":{"height_m":0.8},"materials":["wood"],"construction":"shell","object_category":"solid_wood","wall_mm":5}
assert queries["jobs_list"]["page"] == ["2"] and queries["jobs_list"]["pageSize"] == ["10"]
assert set(queries["jobs_list"]["job_type"][0].split(',')) == {"glb_to_simready", "authored_to_simready"}
assert queries["compositions_list"] == {"page":["2"],"pageSize":["10"]}
assert bodies["sharing"] == {"is_public":True}
assert queries["gallery_list"] == {"tag":["furniture"],"show_on_landing":["true"]}
print("15 atomic cases passed bindings, scope, authentication, parameter and handle checks.")
