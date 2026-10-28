"""Check offline host request plans: python3 tests/check_behavior.py result.json."""
import json
import sys
from urllib.parse import urlparse

results = json.load(open(sys.argv[1]))
cases = {case["id"]: case for case in results["cases"]}
assert len(cases) == 12, "Every fixture must receive one result"


def calls(name, method=None):
    return [r for r in cases[name]["requests"] if method is None or r["method"] == method]


def one(name, method, suffix):
    mutations = [r for r in calls(name) if r["method"] not in ("GET", "HEAD")]
    assert len(mutations) == 1, (name, "unexpected mutation count", mutations)
    request = mutations[0]
    assert request["method"] == method and urlparse(request["url"]).path.endswith(suffix), name
    assert request["authentication"] == "rigyd", name
    return json.loads(request["body_json"])


body = one("generate", "POST", "/compositions/generate")
assert body["generation_method"] == "procedural"
assert body["geometry_builder"] == "responses" and body["asset_class"] == "articulated"
assert body.get("auto_submit", False) in (False, "false"), "Multipart accepts a serialized boolean"
assert body["negative_prompt"] == "extra handles"
assert [file["file"] for file in body["images"]] == ["front.png", "right.png", "back.png", "left.png"]
context = body["physical_context"]
if isinstance(context, str):
    context = json.loads(context)
assert context["mass_kg"] == 12 and context["dimensions_m"] == {"length": 0.7, "height": 1}
assert context["materials"] == ["wood"] and context["fixed_base"] is True
assert "cmp-new" in cases["generate"]["result"]

body = one("interactive_images", "POST", "/compositions/start")
assert [file["file"] for file in body["images"]] == ["a.png", "b.png", "c.png"]
assert "cmp-lamp" in cases["interactive_images"]["result"]

body = one("brief_patch", "PATCH", "/compositions/cmp-brief")
assert set(body) == {"asset_brief"}
brief = body["asset_brief"]
assert brief["declared"]["fixed_base"] is False and brief["declared"]["mass_kg"] == 12
assert brief["declared"]["materials"] == ["wood"] and brief["declared"]["dimensions_m"] == {"height": 1}
assert brief["articulation_hint"][0]["travel_frac"] == 0.7 and brief["confidence"] == 0.9

for name in ["convert_failed_prototype", "missing_simulation_price", "wrapped_failure", "resume_status"]:
    assert all(r["method"] in ("GET", "HEAD") for r in calls(name)), (name, "unrequested or unavailable paid operation")
assert "cmp-saved" in cases["wrapped_failure"]["result"]

body = one("zero_simulation", "POST", "/conversions/job-ok/simulate")
assert body["scene"] == "drop" and "sim-new" in cases["zero_simulation"]["result"]

body = one("upload_only", "POST", "/compositions/cmp-ready/geometry-artifacts")
assert body["glb"]["file"] == "asset.glb"
assert "manifest" in body and "cmp-ready" in cases["upload_only"]["result"]

gallery = calls("gallery_download")
assert all(r["method"] == "GET" and r["authentication"] == "none" for r in gallery)
gallery_reads = [r for r in gallery if "/demo-assets/" in urlparse(r["url"]).path]
assert all(urlparse(r["url"]).path.endswith("/demo-assets/cabinet-demo") for r in gallery_reads)
assert gallery_reads or "cabinet-demo" in cases["gallery_download"]["result"], "Already-read detail must retain gallery identity"
assert any(r["url"] == "https://assets.example/cabinet.zip" for r in gallery)
assert not any("/conversions/source-job/result" in r["url"] for r in gallery)

legacy = calls("legacy_download")
assert all(r["method"] == "GET" for r in legacy)
assert any(r["url"] == "https://storage.example/legacy.zip" and r["authentication"] == "none" for r in legacy)
assert "usd/cabinet/cabinet.usd" in cases["legacy_download"]["result"]

body = one("reference_only", "POST", "/compositions/cmp-ref/prerender")
assert body == {"mode": "fresh", "instruction": "matte blue finish"}

for case in cases.values():
    for request in case["requests"]:
        assert "/internal/" not in request["url"]
        if request["authentication"] == "rigyd":
            assert urlparse(request["url"]).hostname == "api.rigyd.com", "Credential sent to storage host"
print("12 fixture cases passed HTTP, field preservation, handle and credential-boundary checks.")
