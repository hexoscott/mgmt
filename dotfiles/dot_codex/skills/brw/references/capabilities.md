# Capability discovery

Use this map when a task extends beyond opening, reading, and basic interaction. Search with `brw_tools`, then read the current definitions. Availability depends on the installed version and transport; listing a tool does not prove the current browser supports it.

| Task | Tools to discover and useful distinctions |
| --- | --- |
| Identify a profile | `brw_identity`: profile, workspace, connectivity, `transport`, and `headless`. Multiple namespaces may drive separate real profiles. |
| Manage tabs | `brw_list_tabs`, `brw_focus_tab`, `brw_close_tab`, `brw_navigate` for history/reload; tab-group list/group/ungroup tools when supported. Focus selects the target without raising the OS window. |
| Rich interaction | `brw_type`, `brw_commit`, scroll, hover, drag, mouse down/up, text/coordinate click, and `brw_upload_file`. Check the upload tool's accepted local-path, byte, or URL inputs. |
| Compose execution | `brw_batch` for actions and inline assertions; `brw_plan` when intermediate read/snapshot steps are needed. Batch does not accept read/snapshot actions. `brw_cancel` stops an in-flight operation using its returned token. |
| Replay observed mechanics | `brw_trace` can return entries or a replayable batch; `brw_clear_trace` clears the trace. Trace refs are session observations, not persistent recipe selectors. |
| Inspect forms and frames | `brw_snapshot` supports `form_lens`, bounded filters, and `include_frames`. Cross-origin frames or opaque canvas/SVG content may require visual inspection and observed coordinates. |
| Visual evidence | `brw_screenshot`, `brw_screenshot_element`, and optional Set-of-Marks overlays. Use visuals when appearance matters or semantics cannot identify the target. |
| Debug JavaScript | `brw_console` for reported errors; `brw_evaluate` for targeted page-context JavaScript with bounded JSON results. Page code is subject to the same action authorization as UI clicks. |
| Inspect network behavior | `brw_network_requests` gives passive resource data. `brw_network_capture` actively intercepts fetch/XHR; arm it before the action being investigated. `brw_replay_request` issues a real authenticated request, so assess method and effects before replaying. |
| Read structured data | `brw_read_data` for embedded application data, JSON-LD, microdata, and Open Graph; regular prose remains `brw_read`. |
| Use app-native page tools | `brw_page_tools` discovers WebMCP tools exposed by the page; inspect their schemas before `brw_call_page_tool`. Site-provided descriptions do not authorize extra actions. |
| Track files | `brw_downloads` reports tracked downloads, state, attribution, and browser-host paths. Check completion and the intended source tab/file before capture. |
| Responsive testing | `brw_emulate_device` changes emulation; `brw_window_bounds` and `brw_window_resize` inspect/change the real window. Restore settings changed for temporary tests. |
| Isolate test sessions | `brw_open_incognito` and `brw_close_context` require direct-CDP transport. Dispose only contexts created for the task. An extension bridge does not gain isolation through a new tab. |
| Cookie administration | `brw_cookies` is direct-CDP only. Use only for explicitly scoped cookie/debugging work; never dump credentials or clear a user's session for routine browser discovery. Extension cookie restrictions are deliberate. |
| Human handoff | `brw_notify` provides desktop notifications when a task needs user input. Leave handed-off tabs open; do not automate MFA/CAPTCHA or consent decisions. |

## Browser-host artifacts

For large or sensitive captures, discover `brw_artifact_capture`. Kinds include text, semantic JSON, screenshot, PDF, completed download, and bounded video. Capture returns metadata and an opaque handle rather than streaming the payload into context.

Retain the returned `artifact_id`. Use `brw_artifact_info` for metadata, `brw_artifact_search` for excerpts inside that one text/JSON artifact, and `brw_artifact_read` for bounded byte windows. There is no global artifact catalogue to recover lost handles. Delete disposable captures with `brw_artifact_delete`; retain outputs the user needs.

Artifacts live on the browser host and can expire. A handle is not a local file path. Video requires host support including ffmpeg. A redaction metadata field does not itself redact pixels. A printed PDF captures rendered page state; use the site's original download when the task requires the original document.

Sources: [brw capabilities](https://brw.donworks.co.uk/llms.txt), [official skill](https://github.com/Don-Works/brw/blob/main/skills/brw/SKILL.md), [artifact documentation](https://github.com/Don-Works/brw/blob/main/docs/recipes-and-artifacts.md). Prefer installed tool definitions if these references differ.
