# Visibility and public assets

Contracts: [sharing](https://docs.rigyd.com/jobs/sharing.md), [gallery](https://docs.rigyd.com/assets/catalog.md).

| Operation | HTTP binding | Request / result |
| --- | --- | --- |
| `asset.share` | `PATCH /conversions/:id/sharing` | Authenticated owner; JSON `{is_public:true|false}`; returns `{data:{id,is_public}}`. Public sharing requires completion (`409` otherwise) |
| `shared.get` | `GET /shared-conversions/:id` | Anonymous; shared completed source-conversion ID; returns public detail, report, package/model URLs and completed simulation previews; otherwise `404` |
| `catalog.list` | `GET /demo-assets` | Anonymous; optional `tag` and `show_on_landing=true`; returns ordered `data` cards, no pagination |
| `catalog.get` | `GET /demo-assets/:id` | Anonymous; gallery **slug or demo document ID**, not card's source-conversion ID; returns public source detail plus curated filename, `demo_description`, tags |

Only change sharing for an explicitly requested visibility operation; using an asset in a local environment does not require making it public. Never create or curate gallery records through undocumented endpoints.

Gallery cards expose `id` as the **source conversion's ID**, along with `slug`, title, description, job type, status, thumbnail/model URL, order, tags, landing flag, asset class and joint count. Use the slug for gallery detail. Keep the source handle separately. Do not assume source sharing is enabled just because it is in the curated gallery.

Visibility is not a license grant. Check reported `simready_metadata.asset_license` and applicable source terms before reusing/distributing an asset. Missing terms remain unknown; a proprietary default is not permission to redistribute. Download public output URLs without a Rigyd key; owner-only result endpoints do not become anonymous.
