# wfh-007 · scout S2 — ESTABLISHED PRODUCTS · DISCOVERY

**Agent:** `wfh-007-s2-scout` · **Surface:** `products` · **Mode:** discovery
**Reuse-first dedup run:** `context_search` ×3 + `context_lookup(category:"technology", tags:["theme:workflow-harness"])` — 34 technology nodes enumerated. **Zero** of them are consumer or personal software. The theme has read this surface as CI/CD, policy engines, observability, AI gateways and coding harnesses. The cold leg below is genuinely cold, and the graph confirms it rather than my asserting it.

---

## 1. The Home Assistant vocabulary teardown

**Origin:** `owner-injection` (named as primary subject in SCOPE). **Reuse:** no existing node; **NEW**.
**Method note:** everything below is read off `home-assistant/core@dev` source, not off product pages. Where I quote docs I say so. Where I could not verify, I say so.

### 1.1 The verb / entity / area model — how an action is named, addressed, and scoped

**Mechanism.** Three separable axes, and their separation is the strongest thing in the design.

- **Naming** is `domain.service` — a flat two-level namespace, registered at runtime by `hass.services.async_register(DOMAIN, "hello", handler, schema=None)`. `DOMAIN` is the integration's own constant. There is no registry authority: any integration claims any verb inside its own domain, and the namespace is populated by whatever happens to be loaded.
- **Addressing** is by `entity_id` (`light.living_room`) — a global flat string keyspace, `domain.object_id`.
- **Scoping** is a separate *target* selector resolved at call time to a set of entity ids: **entity · device · area · floor · label**, freely combinable in one call.

**What this buys.** The target selector is the genuinely good part and the part most worth stealing. It is a *late-bound set-valued address*: an automation written against `area: kitchen` keeps working when the kitchen's device population changes. Scope is a query, not an enumeration. It is also **five orthogonal grouping schemes** (three structural — device/area/floor; one free-form — label; one direct — entity), which is how a single naming scheme survives a decade of heterogeneous hardware.

**The failure mode.** The target resolves to a set, and *the set is resolved before authority is considered and after intent is fixed*. `async_extract_referenced_entity_ids` returns `referenced | indirectly_referenced` — directly-named entities and entities pulled in via device/area/floor/label are merged into one flat set, and the distinction survives only to decide **whose failure gets logged**: unsupported entities are reported only if they were in `referenced` (directly named), not if they arrived via an area. So *the blast radius of an area-scoped call is silently larger than the reported one*. An agent that says "turn on the kitchen" cannot learn from the call what it actually touched.

**Scope against our need.** The target selector covers *addressing* well and is worth adopting as a shape. It does not cover **naming an action independent of the thing it acts on** — a Jurati capability vocabulary needs verbs that exist before any entity does (`derive`, `commit`, `delegate`), and HA has no verb that is not owned by a domain that owns devices.

### 1.2 `homeassistant.turn_on` — the generic verb

**Mechanism** (`homeassistant/components/homeassistant/__init__.py::async_handle_turn_service`, verified in source):

1. Resolve targets to a flat entity-id set. If empty → `_LOGGER.error(...)` and **`return`** — a no-op, not an exception.
2. `itertools.groupby` the set by domain prefix.
3. For each domain: skip `homeassistant` itself (comment in source: *"This leads to endless loop"*); if `hass.services.has_service(domain, service.service)` is false, add to `unsupported_entities` and `continue`.
4. Otherwise re-dispatch `hass.services.async_call(domain, same_verb, dict(service.data) | {entity_id: [...]}, blocking=True, context=service.context)`.
5. `asyncio.gather(*tasks)`. Unsupported entities → one `_LOGGER.warning`.

Registered as:
```python
service_schema = vol.Schema({ATTR_ENTITY_ID: cv.entity_ids}, extra=vol.ALLOW_EXTRA)
hass.services.async_register(DOMAIN, SERVICE_TURN_ON, async_handle_turn_service, schema=service_schema)
```

**What the genericity buys.** Exactly one thing, and it is real: **a heterogeneous target set under one call**. "Everything off" is expressible in one action across lights, switches, fans, media players, humidifiers. That is the whole value proposition, and no domain-typed verb can express it.

**What it costs — three concrete costs, all verified.**

- **The payload has no type.** `extra=vol.ALLOW_EXTRA` on the generic verb, against `cv.make_entity_service_schema(schema, *, extra=vol.PREVENT_EXTRA)` on every entity-platform verb it dispatches into. So `homeassistant.turn_on` *accepts* a strict superset of what its dispatch targets accept, and forwards `dict(service.data)` verbatim to each. Send `brightness: 255` at a target set containing a light and a switch: the light call validates, the switch call raises on PREVENT_EXTRA. **There is no type at which `homeassistant.turn_on(target, data)` is well-formed** — the genericity is bought by deferring validation to a fan-out that has no joint schema.
- **Partial application is the success case.** Unsupported entities are dropped with a log warning; the service returns `None`. `asyncio.gather` over per-domain tasks is not a transaction — if the switch leg raises, the light leg has already run and there is no compensation. The caller receives no per-entity result, no partial-success structure, and no failure signal distinguishable from success.
- **It can only express the verbs whose name collides across domains.** `turn_on` / `turn_off` / `toggle` and nothing else. The generic layer is not a generic dispatcher; it is three hardcoded names that happen to be homographs. `lock.lock` and `cover.open_cover` and `vacuum.start` all mean "engage" and none of them is reachable generically.

**What it cannot express, precisely:** any action with a **parameter**, across a **heterogeneous** target, with a **result**. Pick any two.

### 1.3 Script and scene collapse — where composition degenerates

**Two calling conventions for one object, with different semantics** (HA docs, `integrations/script`):

| | `script.<object_id>` (direct) | `script.turn_on` |
|---|---|---|
| Waits | yes | **no** — "continues as soon as the last script is started" |
| Error propagation | called script's abort aborts the caller | **errors do not propagate** |
| Variables | passed as action data | passed inside a `variables:` sub-dict |
| Return value | `response_variable` available | none |

This is the composition collapse in one table. The *same* script object is both an **entity** (with a `state`, targetable by `homeassistant.turn_on`, hence reachable by an area-scoped call) and a **callable procedure**. Reaching it as an entity silently selects fire-and-forget-with-swallowed-errors. An agent that composes by target selector cannot get the calling convention it needs, because the convention is chosen by *how you addressed the thing*, not by what you asked for.

Concurrency is likewise a property of the *definition*, not the *call*: `mode: single|restart|queued|parallel` + `max:` (default 10) are authored into the script. A caller cannot say "run this, but do not restart the one in flight."

**Scenes degenerate harder.** A scene is not a composition of actions; it is a **set of target states** — declarative, unordered, unconditioned. The scene entity is explicitly **stateless** (docs: it tracks only "the timestamp of when it was last called"). Consequences:

- No ordering, no conditions, no waits — anything requiring sequence must become a script, which loses the "restore a set of states" semantics.
- **A scene has no inverse.** You cannot un-apply it.
- The compensation is `scene.create` with `snapshot_entities`, which captures current states into an ad-hoc scene you can re-apply later. This is the significant finding: **HA promoted a userland undo idiom into core because the vocabulary has no undo primitive.** It is undo-by-convention — the caller must remember to snapshot, must name the snapshot, must know which entities to include, and the snapshot only restores what is expressible as entity state (so a `notify` or a `shell_command` inside the same script is unrecoverable).

### 1.4 The arbitrary `data` dict — the untyped escape hatch

**Mechanism.** Three tiers, and the strength of typing is inverse to the consequence of the action.

1. **Entity-platform services** — real voluptuous schemas via `async_register_entity_service`, `PREVENT_EXTRA` by default. `services.yaml` adds *selectors* (`select`, `number`, entity/device/area pickers) and `filter:` by `supported_features` / `attribute`. **Selectors are UI affordances, not runtime validators** — the runtime type is the voluptuous schema alone; the selector is what the frontend draws.
2. **Plain `async_register(..., schema=None)`** — the docs are explicit: *"If no schema is provided, all data is accepted without type enforcement."*
3. **The `data:` sub-dict**, canonically in `notify.*`: `message` / `title` / `target` are typed, and `data:` is a free dict whose meaning is defined entirely by the downstream platform. Docs say only *"some integrations support additional Data or Target information to customize the action… for more details, refer to their integration documentation."*

**How much real behaviour lives in it.** On the notify surface, effectively all of the consequential behaviour: actionable-notification buttons, images, TTS, channel/priority/critical-alert flags, URLs to open. Two further compounding factors I verified structurally: any value in `data:` may be a **Jinja template** resolved at call time (`SCRIPT_VARIABLES_SCHEMA`, `template_complex`), so the payload is not statically knowable even in principle; and `shell_command.<name>` is registered with **no schema at all**.

**Consequence of an unschematized payload — stated as the mechanism, not the vibe.** Three things become impossible, and each is something the personal-OS framing needs:

- **Static reachability analysis.** You cannot compute, from a workflow definition, the set of effects it may produce — the payload is a template over runtime state.
- **Authority derived from declared demand.** The wfh-005 base (WASI/Bazel/Nix/in-toto/`gh aw compile`) all derive a ceiling from a *declaration*. `data:` is the declaration refusing to declare. A ceiling derived from an HA action set is a ceiling over `{domain.verb}` only, never over what the verb will do.
- **Round-tripping.** An action cannot be re-serialized, diffed, or replayed with confidence, because its meaning lives in a downstream integration's undocumented dict.

### 1.5 Authority — what "ambient" precisely means here, and what they built and shelved

This is where the primary-source read paid off, and the answer is more interesting than "there is no authority model." **There is a complete one, and nothing ships that uses it.**

**What exists** (`homeassistant/auth/permissions/`, dev branch — files: `__init__ · const · entities · events · merge · models · system_policies · types · util`). Per the developer docs, the policy shape is:

```json
{"entities": {"domains": {}, "entity_ids": {}, "device_ids": {}, "area_ids": {}}}
```
resolved in priority order **entity_ids → device_ids → area_ids → domains → all**, with three verbs — **read / control / edit** — attached to **groups**, merged across group membership (any `True` wins). Docs: *"Permissions do not apply to the user that is flagged as 'owner'. This user will always have access to everything."*

**What ships** (`homeassistant/auth/permissions/system_policies.py`, in full):

```python
ADMIN_POLICY     = {CAT_ENTITIES: True}
USER_POLICY      = {CAT_ENTITIES: True}
READ_ONLY_POLICY = {CAT_ENTITIES: {SUBCAT_ALL: {POLICY_READ: True}}}
```

Three groups exist (`system-admin`, `system-users`, `system-read-only`). **`system-users` is entity-identical to `system-admin`.** And `AuthStore` (`homeassistant/auth/auth_store.py`) has **no `async_create_group`** — I enumerated its public methods. Custom groups are *loadable* from a hand-edited `.storage/auth` (the `else:` branch reads `name`/`policy` off the dict) but there is **no API, no websocket command, and no UI to create one**. `config/auth/create` accepts `group_ids: [str]` — references to existing groups only.

So: the entity-permission engine is fully built, fully enforced, and **unreachable**. That is the "tried and abandoned" answer, with the artifact.

**Where enforcement actually sits — and it is opt-in.** `ServiceRegistry.async_call` (`homeassistant/core.py`) performs **zero** authorization. Its first substantive line is `context = context or Context()` — a call with no context gets a fresh anonymous one with `user_id = None`. All checking is delegated into handlers, in exactly two places:

```python
# helpers/service.py — entity service path
if call.context.user_id:
    user = await hass.auth.async_get_user(call.context.user_id)
    if user is None: raise UnknownUser(context=call.context)
    if not user.is_admin:
        if admin_only: raise Unauthorized(context=call.context)
        entity_perms = user.permissions.check_entity      # → POLICY_CONTROL per entity
```
```python
# helpers/service.py — _async_admin_handler, used by async_register_admin_service
if call.context.user_id:
    ...
    if not user.is_admin: raise Unauthorized(context=call.context)
```

Read the guards literally: **no `user_id` ⇒ no check**, and **`is_admin` ⇒ no check**. Automations, scripts and integrations that construct their own context are unauthorized-by-omission, by construction. That is ambient authority in the precise sense — authority is a property of *being inside the process*, not of the caller.

**And a fourth failure I did not expect.** In the non-blocking path, `_run_service_call_catch_exceptions` catches `Unauthorized` and emits `_LOGGER.warning("Unauthorized service called %s/%s", ...)`. **A denied call in fire-and-forget mode fails silently.** A caller cannot distinguish denied from done unless it sets `blocking=True` — and `script.turn_on`, the entity-shaped calling convention, is precisely the non-blocking one.

**The authority annotations landed on the wrong axis.** I checked the registration mode of the consequential, non-entity services:

| Service | What it does | Registration |
|---|---|---|
| `shell_command.<name>` | runs an arbitrary shell command on the host | `async_register(..., supports_response=OPTIONAL)` — **no schema, no check** |
| `shell_command.reload` | re-reads the YAML file | `async_register_admin_service` — **admin-gated** |
| `mqtt.publish` | arbitrary topic + payload + `retain` | `async_register(..., schema=MQTT_PUBLISH_SCHEMA)` — **no check** |
| `mqtt.reload` | re-reads config | `async_register_admin_service` — **admin-gated** |

**Reloading a config file is privileged. Executing a shell command on the host is not.** This is the sharpest single result of my read. The `admin` flag is a binary inherited from *user management* — it distinguishes "may change the system's configuration" from "may use the system." Consequence in the world is a different axis entirely, and HA's vocabulary has no term for it, so the annotations could only land on the axis that existed. The permission model covers exactly the class of actions that are **reversible** (entity state) and covers **none** of the class that is not (send, publish, execute, order, notify).

**What breaks in the wild.** Long-lived access tokens are valid for **10 years** (developer docs, `auth_api`) and carry the full permission set of the user they belong to — which, for any non-read-only user, is `{entities: True}`. The docs describe no scoping because there is none. The community position is a standing, unanswered feature request ("Support for permissions on Long-Lived Access Tokens", 2019-, and a 2024-12 *"WTH can't I set permissions on a long-lived access token?"* whose only 2026 reply points at a **third-party** workaround, `vekexasia/varco`). I found **no maintainer commitment either way** — I am reporting an absence of response, not a refusal. The documented workaround is *create a second non-admin user account*, which, given `USER_POLICY = {CAT_ENTITIES: True}`, buys you the loss of admin-only services and **nothing at the entity layer**.

Separately, `home-assistant/architecture#832` ("Open letter for improving Home Assistant's Authentication system", opened 2022-11-26, **closed**) is about SSO/LDAP/OIDC, **not** about scopes — and it is useful negatively: two auth PRs (`core#37645` LDAP, `core#32926` OIDC) were declined on maintenance burden and token-revocation concerns. `@balloob`: *"Credentials are only validated during login, which results in the creation of a refresh/access token pair. Once granted, all interactions are done with these tokens and no one will check back with the OpenID provider if the user is still valid."* The project's own stated reason for declining federated identity is that **it has no revocation story**, which is the same root cause as the missing scope story.

### 1.6 The irreversibility question

**Does the vocabulary distinguish undoable from not? No — there is no term for it anywhere in the model.** Verified across: service registration signature (no flag), `services.yaml` schema (`target`, `fields`, `selector`, `filter`, sections — no consequence field), the permission verb set (`read`/`control`/`edit` — a CRUD axis, not a consequence axis), and the entity/domain model. `lock.unlock` and `light.turn_on` are the same kind of thing to every mechanism in the system.

**How users and the project compensate — four devices, all out-of-band, none of them in the vocabulary:**

1. **Exposure allowlists.** *"To control your devices over a voice command, you must expose your entities to Assist, which is done to avoid that sensitive devices, such as locks and garage doors, can inadvertently be controlled by voice commands."* This is the closest HA gets to a per-caller scope — and note what it is: a **binary per-entity allowlist per assistant**, sitting *beside* the vocabulary, expressing "don't let the voice thing near the lock." It is per-entity, not per-verb, so exposing a lock for `lock.lock` necessarily exposes `lock.unlock`. It is the irreversibility judgment made once, by hand, at configuration time, on the wrong granularity.
2. **PIN escalation, delegated to the cloud bridge.** The Google Assistant integration's `secure_devices_pin` gates lock/cover domains. This is the only per-action step-up in the stack and it lives in a *bridge integration*, not in core — i.e. the irreversibility model is imported from Google's ontology, not HA's.
3. **Snapshot-then-restore** (`scene.create` + `snapshot_entities`), §1.3 — undo-by-convention, and only for state-expressible effects.
4. **Non-exposure by omission** — the folk practice of simply not creating a `shell_command` you are afraid of.

**The structural point for triage.** All four compensations are *configuration-time and per-installation*. None is a property of an action that a caller, a gate, or a compiler could read. There is no query "is this action reversible?" that HA can answer, therefore no gate can be written against consequence, therefore consequence is enforced by the human who wrote the YAML — which is exactly the property that does not survive an agent writing the YAML.

### 1.7 Home Assistant — buy-before-build evidence

- **Scope against our need.** Covers, and covers well: a **late-bound set-valued target vocabulary** (entity/device/area/floor/label), a runtime action registry with per-action metadata and UI selectors, an always-on event loop with a state machine, ~1,500 integrations, and a working voice surface. Call it the 80%.
  **The uncovered remainder, precisely, and it is the differentiating part:** (a) **no consequence axis** on an action — §1.6; (b) **no per-caller, per-action authority** — the engine exists and ships three policies of which two are "all" — §1.5; (c) **no schema on the payload** at the tier where the consequential actions live — §1.4; (d) **no result** from a call — partial application is indistinguishable from success, and denial in the non-blocking path is a log line — §1.2/§1.5; (e) **no phase or session concept** at all — authority is not indexed by anything.
- **Cost and licence.** Apache-2.0, free, self-hostable. Nabu Casa Cloud ~$6.50/mo (remote access + cloud STT/TTS + Google/Alexa bridges) — optional. The real cost is **operational**: Python monolith, monthly breaking releases, `.storage/` JSON as the config-of-record, and integration quality that varies by maintainer.
- **Lock-in and exit.** Low-to-moderate and mostly *conceptual*. Data and config are local files; entity ids are yours. But you would inherit the flat `domain.service` namespace and the untyped `data:` dict as your public vocabulary, and every one of the ~1,500 integrations is written against them. **Adopting HA's vocabulary means adopting the absence of a consequence axis**, and that is not addable later without breaking every integration — which is precisely why HA has not added it.
- **Composability.** Good as a **device-domain adapter** underneath something else — it is the best-populated translation layer from real hardware to a uniform action registry that exists. Bad as *the* vocabulary. What sits in the seam: a wrapper would have to (i) classify every `domain.service` on a consequence axis HA does not provide, (ii) refuse to expose the untyped tier or re-schematize it per-integration, (iii) run every call `blocking=True` to recover a failure signal, and (iv) mint per-call contexts with real `user_id`s to make the entity permission engine fire at all — and would still be defeated by admin bypass and by any integration calling `hass.services.async_call` internally with a fresh `Context()`.

**`cites:`**
```
- type: repo    | ref: home-assistant/core (branch dev) — homeassistant/core.py, ServiceRegistry.async_call, _run_service_call_catch_exceptions | title: Home Assistant Core — service registry | org: Home Assistant | surface: products
- type: repo    | ref: home-assistant/core — homeassistant/helpers/service.py (entity_service_call, _async_admin_handler, async_register_admin_service) | title: Home Assistant service helpers — permission gates | org: Home Assistant | surface: products
- type: repo    | ref: home-assistant/core — homeassistant/auth/permissions/system_policies.py | title: ADMIN_POLICY / USER_POLICY / READ_ONLY_POLICY | org: Home Assistant | surface: products
- type: repo    | ref: home-assistant/core — homeassistant/auth/auth_store.py, homeassistant/auth/const.py | title: AuthStore — three system groups, no group-create API | org: Home Assistant | surface: products
- type: repo    | ref: home-assistant/core — homeassistant/components/homeassistant/__init__.py, async_handle_turn_service | title: generic turn_on/turn_off/toggle dispatch | org: Home Assistant | surface: products
- type: repo    | ref: home-assistant/core — homeassistant/helpers/config_validation.py, make_entity_service_schema | title: entity service schema defaults to PREVENT_EXTRA | org: Home Assistant | surface: products
- type: repo    | ref: home-assistant/core — homeassistant/components/shell_command/__init__.py, homeassistant/components/mqtt/__init__.py | title: consequential services registered unguarded; reload registered admin-only | org: Home Assistant | surface: products
- type: docs    | ref: https://developers.home-assistant.io/docs/auth_permissions/ | title: Permissions — Home Assistant Developer Docs | org: Home Assistant | surface: products
- type: docs    | ref: https://developers.home-assistant.io/docs/dev_101_services/ | title: Integration service actions | org: Home Assistant | surface: products
- type: docs    | ref: https://developers.home-assistant.io/docs/auth_api/ | title: Authentication API — long-lived access tokens valid for 10 years | org: Home Assistant | surface: products
- type: docs    | ref: https://www.home-assistant.io/actions/homeassistant.turn_on/ | title: Generic turn on | org: Home Assistant | surface: products
- type: docs    | ref: https://www.home-assistant.io/integrations/script/ | title: Script integration — direct call vs script.turn_on, modes | org: Home Assistant | surface: products
- type: docs    | ref: https://www.home-assistant.io/integrations/scene/ | title: Scene integration — stateless, scene.apply, scene.create snapshot_entities | org: Home Assistant | surface: products
- type: docs    | ref: https://www.home-assistant.io/integrations/notify/ | title: Notify — platform-specific `data` field | org: Home Assistant | surface: products
- type: docs    | ref: https://www.home-assistant.io/voice_control/voice_remote_expose_devices/ | title: Exposing entities to Assist | org: Home Assistant | surface: products
- type: repo    | ref: home-assistant/architecture#832 | title: Open letter for improving Home Assistant's Authentication system (opened 2022-11-26, closed) | org: Home Assistant | year: 2022 | surface: products
- type: blog    | ref: https://community.home-assistant.io/t/wth-cant-i-set-permissions-on-a-long-lived-access-token/805237 | title: WTH can't I set permissions on a long-lived access token? | org: Home Assistant Community | year: 2024 | surface: products
```

**Alias flags for the leader:** S4 (adjacent) will likely meet this as *"the smart-home ontology problem"*; S3 (literature) as *"coarse-grained capability / permission-granularity mismatch."* The `scene.create` + `snapshot_entities` idiom is the **compensating-transaction / saga** pattern under a consumer name — S4 will find it in event sourcing.

---

## 2. Candidates

### C1 — Matter Access Control Cluster (CSA) — the counter-example living *underneath* Home Assistant
**Origin:** `external-scan` (cold leg) · **NEW** — no graph node · **In-lens:** it is a shipped, per-action, per-subject authority model for a personal-device domain vocabulary, i.e. the exact thing §1.5 says HA lacks.

**Mechanism.** Every Matter node carries an Access Control Cluster on endpoint 0 holding a fabric-scoped ACL attribute. Each ACL entry is four fields:
- **Privilege** — `View < Operate < Manage < Administer`, strictly hierarchical (*"an ACL for Manage privilege will work for operations which require Operate or View privilege (but not Administer privilege)"*).
- **AuthMode** — `CASE` (session-authenticated) or `Group`.
- **Subjects** — Node IDs or **CATs (CASE Authenticated Tags)**; empty list = any subject in that AuthMode.
- **Targets** — a list of `{Cluster ID?, Endpoint ID?, DeviceType?}`; *"at least one must be present, and the endpoint and device type fields are mutually exclusive."* Empty = all targets.

Individual clusters may demand *stricter* privileges than the default for specific operations — i.e. **the authority requirement is a property of the action, declared by the action's own specification**, which is exactly the annotation HA does not have. The Access Control Cluster itself requires `Administer` for all operations (no privilege escalation through the ACL).

**CATs** are the delegation primitive: a tag embedded in a controller's CASE credentials, carrying its own **version number**, so a whole class of controllers is granted or revoked by re-issuing at a new version rather than by editing every device's ACL. That is bulk attenuation + revocation without per-resource writes.

**Resource envelope.** Designed for constrained MCUs — the ACL is a bounded on-device attribute list (spec-mandated minimum entries per fabric, single-digit); enforcement is a table lookup in the Interaction Model dispatch path. Negligible latency; the cost is commissioning complexity.

**Demonstrated vs claimed.** *Demonstrated by the ecosystem* — shipped in `project-chip/connectedhomeip` and in commercial Matter devices/controllers. *I did not verify* real-world ACL granularity in practice: my read is that most consumer controllers write a single Administer-privilege entry for themselves and never use targets, which would make the mechanism present-and-inert (compare **#196**, the emergent finding on vacuous guarantees). **Flagged as unverified — worth one targeted check by S1.**

**Buy-before-build:**
- **Scope vs need.** Covers: per-subject × per-target × per-privilege authority, hierarchical, with revocation, on a personal-device domain, at consumer scale. **Does not cover:** (a) the privilege ladder is four fixed rungs — `Operate` covers both `lock` and `unlock`, so **no consequence axis here either**; (b) targets are cluster/endpoint/device-type — no per-*command* granularity; (c) nothing outside the device domain (no files, money, messages, code); (d) no phase/session indexing — an ACL is standing, not derived per task.
- **Cost and licence.** Spec is free to read; **the CSA membership + certification regime is the cost** (Adopter/Participant tiers, four-to-five-figure annual, plus per-product certification) if you ship a *certified* product. Using the Apache-2.0 SDK privately costs nothing.
- **Lock-in and exit.** Adopting the *model* costs nothing. Adopting the *fabric* means adopting commissioning, certification, and the CSA's release cadence.
- **Composability.** High as a **design donor**, low as a component. The seam: Matter's privilege ladder would have to be re-projected onto a consequence axis, and it terminates at the device boundary.

**`cites:`**
```
- type: docs  | ref: https://project-chip.github.io/connectedhomeip-doc/guides/access-control-guide.html | title: Matter Access Control Guide | org: Connectivity Standards Alliance | surface: products
- type: repo  | ref: project-chip/connectedhomeip | title: Matter SDK — Access Control Cluster implementation | org: Connectivity Standards Alliance | surface: products
```
**Alias flag:** S4 will meet CATs as **attenuated capability tokens / macaroons**; S3 as **ABAC with hierarchical privileges**. High merge probability — do not let it count as three independent hits.

---

### C2 — Apple App Intents: `IntentAuthenticationPolicy` — a shipped consequence declaration on an action
**Origin:** `external-scan` (cold leg) · **NEW** · **In-lens:** it is the missing §1.6 primitive, shipping on ~1.5B devices, declared *by the action author* and enforced *by the OS*.

**Mechanism.** App Intents is Apple's capability vocabulary for the personal device: **`AppIntent`** (the verb, with typed `@Parameter`s), **`AppEntity`** (the addressable noun — `Identifiable`, with a typed identifier and a `DisplayRepresentation`), **`AppEnum`**, and `AppShortcutsProvider` binding phrases. One vocabulary drives Siri, Spotlight, Shortcuts, Widgets, Control Center, the Action Button and Apple Pencil Pro — **one declaration, many callers**, which is structurally the personal-OS shape.

Three things it has that HA does not:

1. **`AppIntent.authenticationPolicy: IntentAuthenticationPolicy`** — *"an enumeration that describes the authentication policy to use when running an app intent… indicates whether this app intent requires the device to be unlocked or otherwise authenticated."* Values: **`.alwaysAllowed`**, **`.requiresAuthentication`**, **`.requiresLocalDeviceAuthentication`**. This is a **per-action, author-declared, system-enforced consequence annotation**, and the graduated third value ("must authenticate *on this device*, not on a paired one") is a genuine consequence *ladder*, not a boolean.
2. **`requestConfirmation(...)`** — an in-flow, resumable confirmation that suspends the intent and returns control: dialog text, a SwiftUI snippet view, a confirmation button label, and a `showPrompt` flag. Confirmation is a **first-class control-flow construct in the action's own execution**, not a client-side courtesy.
3. **Typed parameters with resolution** — parameters are strongly typed and *resolved* (with disambiguation dialogs) before `perform()` runs. There is no `data:` dict.

**Resource envelope.** Compile-time metadata extraction into an app-intents manifest; runtime is an OS-brokered XPC dispatch. Intents may run in the background without a foreground launch — which is precisely why `authenticationPolicy` exists as a separate axis (Apple's own note: a foreground launch already implies full access under the device lock state, so the policy matters for **background** execution).

**Demonstrated vs claimed.** *Demonstrated* — shipped API, documented, in production since iOS 16, extended at WWDC24/25/26 (App Schemas). **Author-report, not verified by me:** whether `requestConfirmation` behaves reliably under Siri invocation is contested — there is an open developer-forum thread reporting it does not. Treat "confirmation works" as `claimed`.

**Buy-before-build:**
- **Scope vs need.** Covers, and is the best thing I found on this surface: a typed verb/entity vocabulary with **per-action authentication policy** and **in-flow confirmation**, driving many surfaces from one declaration. **Does not cover:** (a) the policy axis is *authentication*, not *authority* — it answers "is the human present?" and never "may this caller do this?"; there is no per-caller, per-phase scope at all; (b) it is **declared by the app author**, so it is a self-assessment, exactly the trust posture the firewall rejects — nothing verifies that a destructive intent declared `.alwaysAllowed`; (c) **fully proprietary and unusable off-platform**; (d) no irreversibility *record* — confirmation is a prompt, not an attestation.
- **Cost and licence.** Free to use; **$99/yr** Apple Developer Program to ship; the real cost is Swift + Apple platforms, full stop.
- **Lock-in and exit.** **Maximal.** Not portable, not self-hostable, not inspectable. Adopting the *implementation* is off the table for a build-once/any-backend thesis (theme lens: anti-lock-in). Adopting the *shape* is free.
- **Composability.** Zero as a component. High as the **single best donor design** for the consequence annotation.

**`cites:`**
```
- type: docs | ref: https://developer.apple.com/documentation/appintents/intentauthenticationpolicy | title: IntentAuthenticationPolicy | org: Apple | surface: products
- type: docs | ref: https://developer.apple.com/documentation/appintents/appintent/authenticationpolicy | title: AppIntent.authenticationPolicy | org: Apple | surface: products
- type: docs | ref: https://developer.apple.com/documentation/appintents | title: App Intents framework | org: Apple | surface: products
- type: blog | ref: https://developer.apple.com/videos/play/wwdc2025/244/ | title: Get to know App Intents (WWDC25) | org: Apple | year: 2025 | surface: products
- type: blog | ref: https://developer.apple.com/videos/play/wwdc2026/240/ | title: Build intelligent Siri experiences with App Schemas (WWDC26) | org: Apple | year: 2026 | surface: products
- type: blog | ref: https://developer.apple.com/forums/thread/767140 | title: App Intents: requestConfirmation method not working with Siri invocation | org: Apple | surface: products
```
**Alias flag — high priority.** This is structurally the same object as **MCP tool annotations** (`readOnlyHint` / `destructiveHint` / `idempotentHint` / `openWorldHint`), which S1/S3 will find under that name. *(That equivalence is `[asserted from prior knowledge, not re-verified this run]` — my web-search budget ran out before I could pull the MCP annotations page. **Leader: have S1 confirm it, including the spec's own statement that annotations are advisory and must be treated as untrusted.**)* If both land, they are **one cluster with two shipped instances and opposite trust postures** — Apple's is OS-enforced-but-self-declared; MCP's is explicitly untrusted. That contrast is more valuable than either alone.

---

### C3 — FDX consent (Financial Data Exchange) — shipped scoped, time-limited, revocable delegation over a person's money
**Origin:** `external-scan` (cold leg) · **NEW** · **In-lens:** the delegation component, in a personal domain, at population scale, with an audit trail.

**Mechanism.** OAuth-based, consumer-permissioned access to financial data. The consumer grants a **third party** access to **named data clusters** (account basic, balances, transactions, statements, tax, customer contact) for a **bounded duration**, revocable by the consumer at the source institution, with an **auditable consent log**; issued tokens carry the granted rights and are validated per API call. FDX publishes **UX guidelines** for the consent screen itself — i.e. the standard specifies not just the token but *how the delegation is presented to the person*, which is a component the personal-OS framing needs and which no engineering source will supply. v4.5 (2026) extends the standard toward open finance / pay-by-bank.

**Resource envelope.** n/a (a REST/OAuth standard).

**Demonstrated vs claimed.** *Demonstrated at scale* — FDX reports **>130 million consumer accounts** connected via the FDX API as of early 2026. That is a vendor-published figure and I did not independently verify it; treat the number as `author-report`, the existence of large-scale deployment as well-corroborated. **Regulatory context I could not verify this run:** the US CFPB §1033 rule's status in 2026 was in litigation/revision, which materially affects whether FDX remains a voluntary consortium standard or a compliance floor. **Declared hole.**

**Buy-before-build:**
- **Scope vs need.** Covers: **scoped + expiring + revocable + logged delegation, third-party-to-person, at scale**, plus the consent-presentation problem. **Does not cover:** (a) it is overwhelmingly **read** delegation — the consequence/irreversibility axis appears only at the payments edge (4.5) and I did not verify its authority model; (b) scopes are fixed **data clusters** — a coarse, standardized taxonomy authored by a consortium, not derived from a task's declared demand; (c) it is **one domain**, and its vocabulary is not extensible by us; (d) the consent is **standing**, not phase-indexed.
- **Cost and licence.** Spec access is via FDX/FS-ISAC membership (four-to-five figures annually for the full standard); implementing against an aggregator (Plaid/MX/Finicity) is per-call/per-item commercial pricing. For a personal user, effectively: you consume it, you do not implement it.
- **Lock-in and exit.** For a *consumer* of the standard, low — consent is revocable by design, which is the point. For an *implementer*, high (membership + certification).
- **Composability.** Good — it is the best available **shape for a durable, revocable, person-granted delegation record**, and it composes with anything because it is just OAuth plus a taxonomy. Seam: the taxonomy. Ours would have to be authored, and FDX shows that authoring the taxonomy took a consortium a decade.

**`cites:`**
```
- type: standard | ref: FDX API v4.5 | title: Financial Data Exchange API — consumer-permissioned data sharing | org: Financial Data Exchange | year: 2026 | surface: products
- type: docs     | ref: https://docs.secureauth.com/iam/oauth--consent--and-api-security-for-financial-data-exchange--fdx- | title: OAuth, Consent, and API Security for FDX | org: SecureAuth | surface: products
- type: product  | ref: https://www.openbankingtracker.com/standards/fdx | title: FDX — US open banking standard, adoption figures | org: Open Banking Tracker | surface: products
```
**Alias flag:** S3 will meet this as **UCON / usage control / consent receipts**; S4 as **open banking**. Merge.

---

### C4 — Commercial CD stage-scoped role binding (Spinnaker Fiat · Harness · Azure DevOps) — **closes a standing method hole**
**Origin:** `external-scan` (warm-adjacent; explicitly named as an unspent hole in wfh-005 / themes.md L415) · **NEW as characterized** — near neighbours **#205** (SPIFFE/Vault, credential-minting leg) and **#198** (gh-aw). **In-lens:** it is the incumbent answer to "bind authority to a phase," and wfh-005 recorded it unread under its only BUILD recommendation (**#210**).

**Mechanism — three shipped shapes, and they differ in an interesting way.**

- **Spinnaker (Fiat).** Permissions are `READ | WRITE | EXECUTE` (EXECUTE for applications only), attached to **applications** (Front50), **cloud accounts** (Clouddriver) and **build services** (Igor). *"To successfully run a pipeline in app X that deploys to account Y, you need (at least) EXECUTE on the app X and WRITE on the account Y."* A pipeline runs **as a service account**, and — the load-bearing bit — *"in order to prevent a privilege escalation vulnerability, only users with every role the service account has may use it."* **That is an explicit attenuation rule: a caller may not invoke a runner more privileged than itself.** Pipeline Permissions exist as an alternative to hand-managing service accounts for auto-triggered pipelines.
- **Harness.** `Principal × Role × ResourceGroup`, applied at account / org / project / individual-resource scope. Connectors (credential holders) are scoped by the level they are created at — account-scope connectors are visible everywhere, org-scope only within that org. Resource groups can enumerate **specific pipelines or specific connectors**. Fine-grained, but the grain is *administrative object*, not *pipeline stage*.
- **Azure DevOps.** The closest to phase-indexed: **Environments** are resources that a stage consumes, and *"as the owner of a resource, such as an environment, you can define approvals and checks that must be satisfied before a stage consuming that resource starts."* Approvals-and-checks also attach to **service connections**, so using a credential in a pipeline triggers an approval workflow. Practice is one service connection per environment.

**Demonstrated vs claimed.** *Demonstrated* — all three are GA, documented, widely deployed. I read vendor documentation, **not** deployments; whether real installations use the fine grain is unverified (again the **#196** vacuity risk).

**Buy-before-build:**
- **Scope vs need.** Covers: **authority bound to a phase of a defined process**, with a human gate at the phase boundary, an audit trail, and — in Spinnaker only — a **formal attenuation invariant**. **Does not cover, and this is the whole gap:** the binding is **administrator-provisioned and author-declared** (someone creates a service connection, someone assigns a role, someone writes the stage), never **derived from what the stage declares it will do**. It is `phase → pre-existing credential`, not `declared demand → minted ceiling`. That is the precise distance between the incumbents and the wfh-005 residual composition claim, and it is now measured rather than assumed. Further gaps: authority is granted to the **whole stage**, never per call; the ceiling is a *cloud account*, an order of magnitude coarser than a tool call; and none of the three has a consequence axis (an approval gate is a human standing in for one).
- **Cost and licence.** Spinnaker: Apache-2.0, free, **very high** operational burden (≥10 microservices, Halyard/kustomize, a well-known ops tax). Harness: commercial SaaS, per-service/per-developer, free tier exists, enterprise tiers four-to-five figures/yr. Azure DevOps: ~$6/user/mo above the free tier, plus Azure tenancy.
- **Lock-in and exit.** Spinnaker: low licence lock-in, high **operational** lock-in. Harness: high — proprietary pipeline YAML, RBAC model and connectors; exit means re-authoring everything. ADO: high — Entra ID identity, service connections and environments are Azure-native.
- **Composability.** As *components*, poor — all three are whole platforms and none is personal-scale. As **evidence**, valuable: they establish that stage-scoped role binding is thirty-year-mature commercial practice, that **Spinnaker already ships the attenuation invariant** (so "a delegate cannot exceed its delegator" is not novel), and that **nobody derives the ceiling from the declaration**.

**`cites:`**
```
- type: docs | ref: https://spinnaker.io/docs/setup/other_config/security/authorization/ | title: Spinnaker Authorization (RBAC) — Fiat | org: Spinnaker | surface: products
- type: docs | ref: https://spinnaker.io/docs/setup/other_config/security/authorization/service-accounts/ | title: Spinnaker Service Accounts — role-containment rule | org: Spinnaker | surface: products
- type: docs | ref: https://spinnaker.io/docs/setup/other_config/security/authorization/pipeline-permissions/ | title: Spinnaker Pipeline Permissions | org: Spinnaker | surface: products
- type: docs | ref: https://developer.harness.io/docs/platform/role-based-access-control/rbac-in-harness/ | title: Role-based access control (RBAC) in Harness | org: Harness | surface: products
- type: docs | ref: https://developer.harness.io/docs/platform/role-based-access-control/add-resource-groups/ | title: Manage resource groups | org: Harness | surface: products
- type: docs | ref: https://learn.microsoft.com/en-us/azure/devops/pipelines/process/approvals | title: Pipeline deployment approvals — Azure Pipelines | org: Microsoft | surface: products
- type: docs | ref: https://microsoft.github.io/code-with-engineering-playbook/CI-CD/dev-sec-ops/azure-devops-service-connection-security/ | title: Azure DevOps Service Connection Security | org: Microsoft | surface: products
```
**Alias flag:** S3 will meet Fiat's containment rule as **delegation attenuation / no-privilege-escalation** and as part of the TBAC/WAM lineage already settled in wfh-005. **Do not count it as new prior art — count it as the commercial instance of settled prior art.**

---

## 3. Secret broker — who has actually shipped one for a *personal* user

The framing names a **secret broker** as a component. The honest answer from this surface: **essentially nobody has shipped one for a personal user, and the two nearest products explicitly exclude the personal case.** Near neighbour in graph: **#205** (SPIFFE/SPIRE + Vault, ASSEMBLE) — infrastructure-scale, not personal.

| Product | Scope for a personal user | Verdict on the surface question |
|---|---|---|
| **1Password Service Accounts** | Token scoped to **specific vaults × {read, write, share}** and to Environments (read-only). Up to 100 service accounts. **Documented limitation, quoted:** service accounts *"cannot be granted access to your built-in Personal, Private, or Employee vault, or your default Shared vault."* Business-plan feature. | **Explicitly excludes the personal user's actual vault.** The one product that got scoped programmatic secret access right, ruled the personal case out of scope by design. |
| **Bitwarden Secrets Manager** | Machine accounts issue access tokens scoped to **projects**. Free tier: 2 users / 3 projects / 3 machine accounts. Teams $6/user/mo (20 machine accounts), Enterprise $12 (50). Self-hostable. | Closest usable fit, but the grain is a **project**, not an action or a phase, and it is a separate silo from the user's password vault. **Licence trap:** Bitwarden's Secrets Manager server code lives under `bitwarden_license/`, governed by the **Bitwarden License Agreement** (`LICENSE_BITWARDEN.txt`), **not** the AGPL that covers the rest of `bitwarden/server`. Self-hosting SM is not the OSS-first path it looks like from the outside. |
| **macOS Keychain ACLs** | The genuine one, and it is 25 years old. Per-**item** ACLs with a **trusted-application list**; `kSecACLAuthorizationPartitionID` binds an item to `teamid` / `apple` / `cdhash`, so an application must match a **code-signing identity** to read the item without prompting. Arbitrary code-signing *requirements* can be attached to an item. Readable via `SecAccessCopyACLList`. | **A per-caller, per-secret broker with cryptographic caller identity, shipped to a personal user, enforced by the OS.** It is the strongest existing answer to the component. Gaps: single-platform and unexportable; the grain is *(item × application)* with **no phase, no expiry, no attenuation, no delegation chain**; and the human-facing fallback is the "Always Allow" dialog, which trains the user to grant standing authority — the ambient-authority failure re-entering through the UI. |
| **HashiCorp Vault** (**known — #205**) | No change to report since 2026-08-01. | Right primitives, wrong scale for one person. |
| **HA long-lived tokens** | 10-year, unscoped, full-user authority (§1.5). | An **anti-**broker: the negative control. |

**The gap, stated plainly.** Scoped programmatic secret access is a solved, commercial, *business*-tier product. For one person on their own machine there are exactly two shipped options — a business SKU that refuses to touch the personal vault, and an OS keychain whose caller identity is code-signing and whose scope is a static item list. **Nothing ships an expiring, attenuable, phase-indexed secret grant for an individual.** I searched for it and did not find it; that absence is this section's finding.

**`cites:`**
```
- type: docs    | ref: https://www.1password.dev/service-accounts/get-started | title: Get started with 1Password Service Accounts — limitations | org: AgileBits (1Password) | surface: products
- type: docs    | ref: https://www.1password.dev/service-accounts/ | title: 1Password Service Accounts overview | org: AgileBits (1Password) | surface: products
- type: docs    | ref: https://bitwarden.com/help/machine-accounts/ | title: Bitwarden Machine Accounts | org: Bitwarden | surface: products
- type: product | ref: https://bitwarden.com/products/secrets-manager/ | title: Bitwarden Secrets Manager — plans and machine-account limits | org: Bitwarden | surface: products
- type: repo    | ref: bitwarden/server — bitwarden_license/ | title: Bitwarden License Agreement (LICENSE_BITWARDEN.txt) covers this directory | org: Bitwarden | surface: products
- type: docs    | ref: https://developer.apple.com/library/archive/technotes/tn2206/_index.html | title: TN2206 macOS Code Signing In Depth — keychain ACLs and code-signing requirements | org: Apple | surface: products
- type: docs    | ref: https://hacktricks.wiki/en/macos-hardening/macos-red-teaming/macos-keychain.html | title: macOS Keychain — ACL structure, kSecACLAuthorizationPartitionID, SecAccessCopyACLList | surface: products
```
**Alias flag:** macOS Keychain ACLs will read to S4 as an **OS capability model**; to S3 as **code-identity-based access control**. Merge.

---

## 4. Warm leg — last-looked table and deltas since 2026-08-01

| Entry | Re-check condition | Last looked | **Delta** |
|---|---|---|---|
| **MCP authorization specification** | *a proposal for per-tool or per-resource scopes opens* | **2026-08-17 (wfh-007)** | **Condition NOT met — and the spec moved the other way.** See below. |
| **Coding-agent permission and hook models** | *`anthropics/claude-agent-sdk-typescript#172` closes, or subagent permission-mode inheritance becomes overridable* | **2026-08-17 (wfh-007)** | **Condition NOT met. Zero movement.** #172 (*"AgentDefinition.tools and disallowedTools are not enforced for subagent child processes"*) is **still OPEN**, label `bug`, `updatedAt: 2026-03-03` — its most recent event is a **corroborating** report (`twhalm`: *"Also seeing this behavior when explicitly disallowing Bash. It will still spawn a Task with subagent_type = Bash and continue on its merry way"*), with **no maintainer response in 5½ months**. Read plainly: the declared tool restriction on a subagent is **not an enforcement boundary** in the SDK this garage runs on. That is a live instance of **#196** — a control that is present, configured, believed and inert. I did **not** verify the second clause (subagent permission-mode override) — **declared hole**, budget-limited. |
| **Commercial agent platforms with an authorization story** | standing | **2026-08-17 (wfh-007)** | **Thin, and I am saying so.** #202/#203/#204 remain the coverage and I report **no material change** since 2026-08-01 (not re-litigated, per instruction). I attempted a check on **Microsoft Entra Agent ID** (first-class agent identities with conditional access) and **could not complete it** — WebSearch budget exhausted and `learn.microsoft.com/en-us/entra/identity/agent-id/overview` returned 404. **Declared hole, named, for a targeted re-check.** |

**MCP delta, in detail — the important warm-leg result.** The `2026-07-28` revision's authorization work is **six SEPs of OAuth/OIDC hardening and nothing else**: SEP-2468 (`iss` validation, RFC 9207) · SEP-837 (OIDC `application_type` at registration) · SEP-2352 (credentials bound to issuer, re-register on migration) · SEP-2207 (refresh via `offline_access`) · SEP-2350 (scope **accumulation during step-up** — the nearest miss, and it is about how a client *computes* required scopes, not about the spec *defining* tool-level ones) · SEP-2351 (`.well-known` discovery suffix). The spec's own framing is *"align more closely with how OAuth 2.0 and OpenID Connect are deployed in practice."* Per-tool scopes remain **a vendor pattern layered above the spec** (WorkOS, 2026-07-14, positions them as *best practices for implementers to follow, not standardized requirements within MCP itself*; Descope likewise), resting only on the June-2025 RFC 8707 resource indicators, which bind a token to a *server*, never to a tool.

**Two regressions against our need, which the re-check condition was not written to catch and which matter more than the non-delta:**
- **SEP-2567 removes `Mcp-Session-Id` and protocol-level sessions**; SEP-2575 removes the `initialize`/`initialized` handshake. The protocol went **stateless**. A design that wants per-phase credentials bound to a session now has **no session in the protocol to bind to** — that state must be reconstructed by a gateway (**#203**) or carried in every request.
- **SEP-2577 deprecates Roots, Sampling and Logging.** **Roots was MCP's only resource-scoping primitive** — the client-declared URI boundary telling a server where it may operate. Deprecating it removes the one place the spec expressed a scope over resources.

**Net warm-leg verdict:** the MCP authorization surface did not stand still; it **moved away** from what this theme needs, on two axes, while hardening the axis that was already fine. That is a stronger signal than "no change," and it should be recorded against the watchlist entry with a **rewritten re-check condition** — the current one ("a per-tool scope proposal opens") would now miss the thing that actually happened.

---

## 5. Surface-coverage report

### 5.1 What I searched
**Primary source (strongest evidence, and where the real findings came from):** `home-assistant/core@dev` fetched and read directly — `core.py` (ServiceRegistry), `helpers/service.py` (both permission gates + `async_register_admin_service`), `auth/permissions/system_policies.py`, `auth/auth_store.py`, `auth/const.py`, `components/config/auth.py`, `components/homeassistant/__init__.py`, `helpers/config_validation.py`, `components/shell_command/__init__.py`, `components/mqtt/__init__.py`. `bitwarden/server` licence layout. `gh issue view anthropics/claude-agent-sdk-typescript#172`.

**Vendor and standards documentation:** HA developer docs (`auth_permissions`, `dev_101_services`, `auth_api`) and user docs (`homeassistant.turn_on`, `script`, `scene`, `notify`, `voice_control/voice_remote_expose_devices`); `home-assistant/architecture#832`; MCP spec blog (2026-07-28 RC); WorkOS + Descope MCP authorization writeups; Matter Access Control Guide (`project-chip`); Apple `IntentAuthenticationPolicy` / `AppIntent.authenticationPolicy` / App Intents framework + WWDC24/25/26; 1Password Service Accounts (`get-started`, overview); Bitwarden Machine Accounts + Secrets Manager pricing; Spinnaker Fiat (authorization, service accounts, pipeline permissions); Harness RBAC (rbac-in-harness, resource groups); Azure DevOps approvals + service-connection security; FDX (v4.5 release, SecureAuth consent/OAuth docs, Open Banking Tracker); Apple TN2206 + macOS keychain ACL reference.

**Queries actually run** (representative, 12 of ~14 before budget exhaustion): HA long-lived token scopes/ADR · HA generic turn_on dispatch limits · HA auth permissions entities read/control · HA Assist exposure + lock safety · MCP 2026 per-tool scopes/resource indicators/SEP · Azure DevOps stage-scoped service connection least privilege · Harness RBAC resource groups · Spinnaker Fiat READ/WRITE/EXECUTE · 1Password Service Accounts scoped vault · Bitwarden Secrets Manager machine accounts pricing · Apple App Intents authenticationPolicy · Matter Access Control Cluster privileges · macOS Keychain SecACL trusted applications · FDX consent data clusters.

### 5.2 Declared holes — deliberately skipped or blocked, with reasons
1. **Microsoft Entra Agent ID** — attempted, `learn.microsoft.com/.../agent-id/overview` 404, WebSearch budget exhausted. **Blocked, not skipped.** Highest-value single re-check on this surface.
2. **Google Home APIs / Gemini for Home; Amazon Alexa Smart Home + Alexa+** — the two other million-home personal platforms with a permission model. **Deliberately skipped:** budget went to reading HA's *source* rather than three product pages, and I judged one verified teardown worth more than three impressionistic ones. **Named hole.** Alexa's `Alexa.LockController` PIN requirement and Google's `secure_devices_pin` are the specific cells.
3. **Apple Shortcuts "Ask Before Running" / personal-automation confirmation policy** — attempted; the Apple Support page I reached covers trigger types only. **Unverified.** Would sharpen §1.6's compensation list.
4. **Solid / Inrupt ESS, Anytype, Urbit as commercial products** — **deliberately skipped: assigned to S4** by the scan shape. Duplicating them here would inflate the surface tally with pseudo-independent hits, which is the exact wfh-005 failure the mandatory merge exists to prevent.
5. **Personal-finance aggregation as *products*** (Plaid, MX, Finicity, Monarch, Copilot Money) — I read the **standard** (FDX) rather than the aggregators, on the judgment that the authorization model lives in the standard and the aggregators are implementations of it. **Named hole** if triage wants commercial terms.
6. **IFTTT / Zapier / Make consumer tiers** — skipped; they are the *weakest* authority story on the surface (per-connection OAuth, no per-action scope, no consequence axis) and I did not expect a finding. **Asserted expectation, unverified.**
7. **#200 and #202** — not re-litigated, per instruction. **No material change to report** on either since 2026-08-01.
8. **Patent prior art** — out of my surface; remains the theme's other standing hole.

### 5.3 Cold-leg record — the protected spend, and it was the majority of this run
**Assigned cold leg: read the established-products surface as *consumer and personal software*, which this theme has never done.** Confirmed cold by graph query, not by assertion: of 34 `technology` nodes tagged `theme:workflow-harness`, **zero** are consumer software.

**Spend: roughly two-thirds of this run**, and it produced three of the four candidates plus the entire secret-broker section — i.e. the cold leg outperformed the warm leg by a wide margin this cycle.

- **Matter Access Control Cluster (C1)** — a per-subject × per-target × per-privilege authority model with tag-based bulk revocation, shipping in consumer devices *underneath* Home Assistant. Productive.
- **Apple App Intents `authenticationPolicy` + `requestConfirmation` (C2)** — a shipped, OS-enforced, per-action consequence declaration. The single best find of my run, and it exists only because the cold leg was protected: nothing in the theme's declared reading surfaces ("CI/CD platforms, workload-identity systems, policy engines, secrets brokers, commercial agent platforms") would ever have surfaced Siri.
- **FDX consent (C3)** — scoped, expiring, revocable, logged personal delegation at 130M-account scale. Productive.
- **macOS Keychain ACLs (§3)** — a per-caller secret broker for a personal user, using code-signing identity. Productive.
- **Consumer automation confirmation UX (Shortcuts, IFTTT/Zapier)** — **dry**, and blocked before completion. Reported as dry, not omitted.
- **Google Home / Alexa permission models** — **dry, because unread.** Declared hole 2.

### 5.4 Theme-revision signal *(first-class output; relayed to the owner at the triage gate; does not alter this scan)*

**Signal 1 — the coverage grid has no cell where my strongest finding can land, and that is a grid defect, not a finding defect.** The eight dimensions (structure · context provisioning · security · introspection · cost · self-improvement · recovery/durability · human steering) are coding-agent-harness-shaped, as the scope already suspects. My load-bearing result — *HA's authority annotations landed on config-mutation rather than on effect-in-the-world, because the vocabulary has no term for consequence* — is not a security finding (the mechanism works exactly as designed), not a human-steering finding, and not a structure finding. It is a **consequence** finding, and there is nowhere to put it. **I support promoting "irreversibility and consequence" to a first-class dimension, on evidence:** three independent products on this surface have shipped a consequence primitive under three different names (Apple `IntentAuthenticationPolicy`; Google/Alexa `secure_devices_pin`; HA's Assist exposure allowlist as the degenerate case), which is what a real dimension looks like — the same concern reinvented independently. "Domain vocabulary" is likewise supported by §1 in its entirety. I have **no evidence** on the person model or on always-on/proactivity from this surface and take no position on those two.

**Signal 2 — the lens sentence excludes the material that produced this run's best findings.** The theme's lens is *"context-injection & control architectures for LLM coding agents"* and its declared products surface is *"CI/CD platforms with derived job identity, workload-identity systems, policy engines, secrets and credential brokers, commercial agent platforms."* Read strictly, **Apple App Intents, Matter, FDX and the macOS Keychain are all out of lens** — none is about a coding agent and none is about context injection. They were in scope only because the SCOPE file overrode the theme for this run. If the personal-OS reframe is ratified, the products surface needs rewriting to name **consumer and personal software with a domain vocabulary or an authorization model** explicitly; if it is *not* ratified, the owner should know that the current lens would have excluded C1–C3 and §3 and that this surface would have returned a thin warm leg and little else.

**Signal 3 — one watchlist re-check condition is now known to be mis-specified.** The MCP entry's condition ("a per-tool scope proposal opens") is a *presence* test, and the thing that actually happened was two *removals* (sessions, Roots) that damage our need more than the missing addition does. Presence-only re-check conditions cannot see regressions. I would rewrite it as: *"the authorization or session model changes in either direction — including deprecation of a scoping primitive."* Method note for the retro, not a change I am making.

---

## 6. Compact return list

| Find | Lens | New / Known | Buy-before-build evidence present? |
|---|---|---|---|
| **Home Assistant** — vocabulary + authority teardown (§1) | **in** | **NEW** (no graph node) | **Yes** — scope-vs-need with the 5-part uncovered remainder named, cost, lock-in, composability |
| **C1 Matter Access Control Cluster + CATs** | **in** | **NEW** | **Yes** (CSA membership/certification cost; design-donor composability) |
| **C2 Apple App Intents `IntentAuthenticationPolicy` / `requestConfirmation`** | **in** | **NEW** | **Yes** (max lock-in — donor only, not a component) |
| **C3 FDX consent (v4.5)** | **in** | **NEW** | **Yes** (membership cost; revocable-by-design = low consumer lock-in) |
| **C4 Spinnaker Fiat · Harness · Azure DevOps stage-scoped binding** | **in** | **NEW as characterized** — **closes the standing hole** at themes.md L415 / **#210** | **Yes** (three cost/lock-in profiles; gap = provisioned, not derived) |
| **1Password Service Accounts** (§3) | **in** | **NEW** | **Yes** — *excludes the personal vault by design* |
| **Bitwarden Secrets Manager** (§3) | **in** | **NEW** | **Yes** — *server code is Bitwarden-licensed, not AGPL* |
| **macOS Keychain ACLs** (§3) | **in** | **NEW** | **Yes** — the only shipped personal-user secret broker found |
| **MCP authorization spec** (warm) | **in** | **known cluster (#203)** | Delta only — **condition not met; two regressions** |
| **claude-agent-sdk-typescript #172** (warm) | **in** | known | Delta only — **still open, 5½ months silent, corroborated** |
| **#200 ruvnet / #202 AgentCore+Cedar** | in | **KNOWN — settled, not re-litigated** | **No material change since 2026-08-01** |

**Flags for the leader**
1. **Merge risk is high and concentrated.** C1↔S4 (OS capability models / attenuated tokens) · C2↔S1 (**MCP tool annotations** — same object, opposite trust posture; verify) · C3↔S3 (UCON / consent receipts) · C4↔S3 (delegation attenuation, already settled by wfh-005 — **must not re-count as new prior art**) · Keychain↔S4. Left unmerged, my five "independent" authority finds would collapse to about **two** clusters: *per-action consequence declaration* and *scoped delegation with revocation*.
2. **Firewall.** Everything above is `claimed`. Nothing was demonstrated by us. Three items are explicitly `[unverified]`: Matter ACL granularity in real deployments, FDX's 130M figure and §1033 regulatory status, and the App Intents `requestConfirmation`-under-Siri reliability report.
3. **`vekexasia/varco`** (third-party HA token-scoping workaround, surfaced 2026-06 in the WTH thread) — I did not read it. **Hand to S1 (active-dev)**; a low-star personal-scale token broker is exactly the shape the #216 low-star instrument exists to catch.
