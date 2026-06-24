# Notebook Review Log — Chapter 6 (Lenses)

Standing editorial log for `index.ipynb`: open issues, book-coverage gaps, known
compromises. Maintained per `workflow/stewardship-standard.md`. Newest entries on
top; date every entry. Companion to `workflow/TODO.md` (figure build progress) and
`workflow/audit-2026-06-23.md` (full audit detail).

Status: 🔴 open · 🟡 in progress · ✅ resolved · 💬 needs human decision

---

## 2026-06-24 (cont. 7) — Markdown cleanup pass + Fig 6.11 patch (per cleanup-task drop)

Applied the 16 edits from the cleanup task. Notebook runs top-to-bottom; 0 NumPy; 0 toolchain-in-markdown.

- ✅ **Fig 6.11 patch (id 34):** header `# Figure 6.9(e) … (book §6.2)` → `# Figure 6.11 — Variables for the depth-of-field calculation (book §6.3.1)`; save path `fig06_lenspropt_e.png` → `fig06_11.png`; deleted the orphan `fig06_lenspropt_e.png`. **The long-standing Fig 6.9(e) naming anomaly is now resolved.**
- ✅ **Markdown trims/corrections (2a–2n):** deleted preview-prose cell (id 7) and merged the Fig 6.4(b) caption + "Reading" cell (id 13+14 → one); trimmed §6.2 intro (dropped notation table, id 2); rewrote the c-cancels derivation to drop the invented δ shorthand (id 16); fixed "lowest"→"upper" extreme ray (id 10, P2); de-(Top/Middle/Bottom)'d the Fig 6.10 caption (id 30); trimmed Fig 6.5 outro (id 19), Fig 6.6 intro (id 20), Fig 6.10 outro (id 32), Fig 6.11 caption (id 33), Fig 6.11 outro (id 35), Fig 6.12 intro (id 36) and outro (id 38), Fig 6.14 outro (id 7e2e825a). **43 → 41 cells.**
- ⚠️ **One deliberate deviation from the task text:** the provided 2l (Fig 6.12 intro) reintroduced "**Kornia** Gaussian blur" — the exact toolchain term removed from cell 38 last turn. Per the contract (no library/toolchain names in markdown), applied as "a Gaussian blur with σ ∝ 1/N". Flag for sign-off.
- Verified: dog_scene.png is now a real PNG and the broken Fig 6.1 cell is gone (prior cleanup), so the notebook executes clean. All 16 edits spot-checked.

---

## 2026-06-24 (cont. 6) — Supervisor pass after Fig 6.13 + §6.3.2 landed

Notebook had grown to 46 cells with duplicated blocks (buffer churn). Cleaned up; runs top-to-bottom, 11 figures, 0 NumPy.

- ✅ **Removed duplicated §6.3.2 "Concave Lenses" block** — the section header, the 114-line Fig 6.13 code, and its intro markdown were present **twice** (non-adjacent, so the earlier adjacent-dup check missed them). Kept one copy.
- ✅ **Removed misplaced duplicate "four properties" markdown.** It references "panel (c) **above**" (Fig 6.8c), so it belongs *after* Fig 6.8 — kept that copy, dropped the one before Fig 6.8. Plus 2 empty markdown cells. Net **46 → 40 cells**.
- ✅ **Toolchain talk in markdown fixed (cell 38):** "The cell uses **Kornia's GPU-accelerated `gaussian_blur2d`**…" → "The depth-dependent blur is discretized into a small number of levels…" (concept, not library/GPU).
- ✅ **`hide-input` added to Fig 6.13.** All 11 figure cells now tagged.
- ✅ **Fig 6.13 reviewed — compliant:** uses `COLORS`, reuses `lens_curves`/`draw_biconvex_lens`/`focal_length`, no hex literals, §6.3.2 label correct.
- Clean: 0 NumPy, no strays, no dead helpers, voice clean, no remaining duplicate cells.

**Open:**
- 🔴 **Fig 6.9(e) naming mess (cell ~31)** — still "Fig 6.9(e) — … (book §6.2)" → `fig06_lenspropt_e.png`. Wrong number/section/filename. Unresolved.
- 💬 **Possible missing intro for Fig 6.8** — after removing the misplaced markdown, the `## 6.3` header sits directly before the Fig 6.8 cell with no figure caption. Verify whether 6.8 wants a short intro.

---

## 2026-06-24 (cont. 5) — Contract pass after §6.3.1 depth-of-field figures landed

Three new figures arrived via buffer save (6.10, a "6.9(e)", 6.12). Reviewed against the standard; notebook runs top-to-bottom (Kornia depth-of-field included).

- ✅ **Color redefinition fixed (6.10).** Cell re-defined `dark`/`blue`/`cyan` as hex literals + a drifted `gray = #666666`. Routed all through `COLORS` (gray → palette `#555555`). Other new cells (6.9e, 6.12) were already clean.
- ✅ **`hide-input` added** to the three new figure cells (6.10, 6.9e, 6.12). All 10 figure cells now tagged.
- ✅ **Stray images removed:** `fig06_11.png`, `fig06_depth_of_field.png`, `fig06_rulers.png`, `fig06_rulers_source.png` (no cell writes them, unreferenced). `images/` now = exactly the 10 savefig outputs.
- ✅ **TODO synced:** collapsed 6.8 (a/b/c) → one combined ✅ row (`fig06_08abc.png`); filled §6.3.1 with 6.10 ✅ + 6.12 ✅; recorded the 6.9(e) anomaly.
- ✅ `kornia`/`DEVICE` are now actually used (depth-of-field blur) — earlier "unused scaffolding" flag is resolved.

**Open / needs decision:**
- ✅ **NumPy — RESOLVED.** Cell 37 (Fig 6.12): `ax.imshow(panel.numpy())` → `ax.imshow(panel)` (matplotlib converts the CPU tensor internally). 6.12 re-rendered **byte-identical**; notebook now has **0 NumPy references**. (Note: `img = torch.tensor(plt.imread(...))` still loads via matplotlib's numpy-backed reader at the I/O boundary — not our code calling numpy; could move to `kornia.io.load_image` later for full purity, but it risks changing pixel values so left as-is.)
- 🔴 **Fig 6.9(e) naming/section/filename mess (cell 34).** Header "Fig 6.9(e) — Depth of field and aperture (book §6.2)" → saves `fig06_lenspropt_e.png`. Figure number conflicts with 6.9 (conjugate points), section should be §6.3.1 not §6.2, and the filename is non-standard. Needs a proper figure number + filename + section label. Structural — propose, not performed.

---

## 2026-06-24 (cont. 4) — Standard sweep after Fig 6.9 landed

New Fig 6.9 (conjugate points, 5 panels) arrived via buffer save. Reviewed against the standard and applied clear-cut fixes; full top-to-bottom run OK, all 7 figure cells tagged, 7 images, no strays.

- ✅ **`hide-input` re-added** to Fig 6.4(a) (reverted **again** by a buffer save, even post-commit) and added to new Fig 6.9.
- ✅ **Toolchain comment removed** from the imports cell ("device-agnostic… renders per-pixel blur… GPU" — violated "no toolchain talk in comments"). Kept the bare `DEVICE` line and `kornia` import as imminent-use setup for §6.3.1.
- ✅ **Fig 6.9 header fixed** `(book §6.2)` → `(book §6.3)` — internal contradiction (its own caption + TODO + book all say §6.3).
- ✅ **Fig 6.9 reviewed — compliant:** physical knobs (n,R1,R2,c) → derives f/b via helpers; reuses `lens_curves`/`draw_biconvex_lens`/`focal_length`/`image_distance`; uses `COLORS` directly (per the forward rule); physics correct (a=3f→1.5f, 2f→2f, 1.5f→3f, ±∞ limits).
- Section structure present: `## 6.2 — Lensmaker's Formula` (cell 2) and `## 6.3 — Imaging with Lenses` (cell 22).

**Still open / proposed (not performed — judgment/fidelity):**
- ✅ **Fig 6.6 section attribution — RESOLVED.** Checked the book: Fig 6.6 (off-axis points) is in **§6.2** ("by rotating the lens… the lensmaker's equation also holds for light originating off the optical axis"); Fig 6.5 → §6.2, Fig 6.8 → §6.3 — all matching the notebook. **The notebook was correct; `TODO.md` was wrong.** Moved Fig 6.6 from §6.3 to §6.2 in TODO with a "do not re-file" note. Also flipped Fig 6.9 → ✅ (built).
- 🟡 **TODO 6.8 row-structure mismatch (minor).** TODO lists Fig 6.8 as three rows `(a)/(b)/(c)` with separate output files `fig06_08a/b/c.png`, but the notebook renders one combined `fig06_08abc.png`. Status still ⬜ there. Reconcile the TODO rows to the combined figure when convenient (not done — needs a small restructure decision).
- 💬 **Imports cell `DEVICE`/`kornia` unused.** Kept as scaffolding because §6.3.1 (depth of field, cell 28 says "next") will use them. If that section slips, they're dead code — revisit.
- ⚠️ **Buffer churn persists post-commit.** Fig 6.4(a)'s tag was reverted *after* the commit, and Fig 6.9 arrived untagged — meaning a stale VS Code buffer is still overwriting committed disk state. Each new figure needs a re-tag pass until the editing workflow stops saving stale buffers over the working tree.

---

## 2026-06-24 (cont. 3) — Color palette consolidation

Precondition met (Fig 6.6 **and** 6.8 both integrated and rendering). Applied the "consolidate color palette" findings.

- ✅ **`COLORS` dict added** to the drawing-helpers cell (dark/gray/blue/red/green/cyan/panel/normal), with the rationale comment.
- ✅ **All six figure cells swept** to pull from `COLORS`; inline literals in 6.4(b) routed through named colors; `black`→`dark` in 6.8. Documented one-offs kept local (6.3a tints `#eef4fb`/`#d4e1f0`/`#1f3a5f`, 6.4b caveat `#4d74a6`, lens-body fill `#dbe7f5`).
- ✅ **Drift eliminated:** `#2266ff`, `#c7362b`, `#ff3b0a`, `#1f49ff`, `#1748f4`, `#169b59`, `#666666` all gone.
- ✅ **Verification:** top-to-bottom run OK. 6.3a / 6.4a / 6.5 **byte-identical** (already canonical). 6.4b / 6.6 / 6.8 shifted **color-only** — visually confirmed geometry intact in each. 6.6's bright-orange red (`#ff3b0a`) is now the muted palette red, consistent with the other figures.
- **New baseline hashes:** 03a `e8e05145`, 04a `ca8f13b4`, 04b `7c049346`, 05 `8a8b7178`, 06 `9cccc159`, 08abc `43509b98`.
- Suggested commit title (per findings): `notebooks(mit-book-ch6): consolidate color palette into shared helpers cell`.
- **Forward rule:** new figure cells should use `COLORS["…"]`, not fresh hex literals.

**NOT bundled (per the findings' "don't bundle" rule) — still open:**
- 🔴 **`hide-input` missing on Fig 6.6 (cell 20) and Fig 6.8 (cell 24).** My earlier 6.6 tag was reverted by a buffer save; 6.8 arrived untagged. Needs re-tagging.
- ⚠️ **Buffer-revert churn is destroying edits.** The on-disk notebook keeps being overwritten by VS Code buffer saves that drop prior changes (6.6 tag lost; figures 6.6→6.8 added between turns). Recommend committing to make work durable, or using **Revert File** (not Save) consistently. This color pass is itself at risk until committed.

---

## 2026-06-24 (cont. 2) — Guideline sweep after 6.5 / 6.6 landed

New figures Fig 6.5 (R↔θ_S) and Fig 6.6 (off-axis) arrived via a buffer save. Reviewed against the four coding guidelines; both render correctly and are physically sound (6.6: `P2 = −b·P1/a`, parallel ray through focal point — verified). Fixed the clear-cut violations:

- ✅ **`hide-input` added** to Fig 6.5 and Fig 6.6 (they `savefig` but were untagged). Now all 5 figure cells + drawing-helpers carry it; no figure cell missing it.
- ✅ **Duplicate markdown removed** — the §6.5 wrap-up and the §6.6 intro/caption were each duplicated (adjacent identical cells). Removed the 2 dupes (24 → 22 cells).
- ✅ **Stray PNGs removed** — `fig06_rotated_lens.png` and `fig06_thinLens_abc.png` — orphaned experimental renders, written by no `savefig` and referenced nowhere. `images/` now holds exactly the 5 live figures.
- ✅ **TODO.md updated** — Fig 6.4(b), 6.5, 6.6 → ✅ (built). §6.2 figure set complete.
- ✅ Full top-to-bottom execution still succeeds; all 5 figures save.

**Still open (held for human decision):**
- 💬 **Imports cell (cell 1):** `DEVICE` and `kornia` are imported/defined but used nowhere, and the comment "(which renders per-pixel blur) uses DEVICE…" is toolchain-flavored (`renders`) **and** forward-refs a depth-of-field section that doesn't exist. Decide: drop the unused setup + comment, or leave as scaffolding for the coming section.
- 💬 **Cell 23 forward promises:** re-introduces "depth of field, concave lenses, Galilean telescope" — the same teaser we removed from the intro (cell 0). Section-closer teaser vs. consistency with the de-scoped intro.
- 🔴 **NEW — §ation of Fig 6.6:** `TODO.md` files Fig 6.6 under **§6.3 (Imaging with Lenses)**, but notebook cell 23 says **"§6.2 is complete"** with 6.6, and the surrounding prose treats it as a §6.2 off-axis extension. Verify against the book which section owns Fig 6.6 and reconcile the prose/TODO. (Order/fidelity check — flagged, not changed.)

---

## 2026-06-24 (cont.) — Sign fix + 6.4(b) bloat loops (static-review handoff)

Applied the static-review findings. Full top-to-bottom execution succeeds; **all three figures byte-identical** after every change.

- ✅ **A — sign-convention fix (derivation markdown).** Changed the two boxed formulas from `(1/R₁ − 1/R₂)` to `(1/R₁ + 1/R₂)`. Now consistent across the derivation cell, the closing cell, and `focal_length`. **No minus form remains anywhere.** Markdown only.
- ✅ **B4 — clarity nit (Reading 6.4(b)).** `($n_1\sin\theta \approx n_1\theta$)` → `(the small-angle form $\sin\theta \approx \theta$)`. Markdown only.
- ✅ **B1–B3, B5 — physics confirmed correct, no edits.** Sanity values right; derivation chain `2θ_S = θ₂+θ₃ → θ_S = c/(2(n-1))(1/a+1/b) → f = R/2(n-1)` correct; exaggerated-angle caveat honest.
- ✅ **C1 — surface-normal blocks → loop.** Folded front/back normals into a 2-iteration loop. **Byte-identical.**
- ✅ **C2 — right-angle-mark blocks → loop.** Folded into a loop over `(hit, normal_air, tangent)`; tangents precomputed to keep values bit-exact. **Byte-identical.** (Biggest single win.)
- ⏹️ **C3 — declined (correctly).** After C1/C2 the `center + radius*stack([cos,sin])` idiom remains only *inside* the already-single `main_angle_specs` loop (not duplicated). Routing those through `draw_angle` would replace 6.4(b)'s `FancyArrowPatch` arrowhead arcs with `draw_angle`'s plain `ax.plot` arcs — a **visual change**, so not done. Matches the "don't over-abstract" guidance.
- ✅ **D — voice clean.** grep of all markdown cells for `we/our/let's/I'll` → none.
- **Result:** 6.4(b) cell ~363 → ~336 lines (−27), no visual change.

---

## 2026-06-24 — Tier A applied; 6.4(b) regression check; execution-order bug

Statuses here supersede the 2026-06-23 entry below.

### Done this pass (markdown/metadata only — zero render risk; figure cells untouched)

- ✅ **`hide-input` restored** on Fig 6.3(a) and Fig 6.4(a). All four plotting/support cells (6.3a, 6.4a, drawing-helpers, 6.4b) now tagged.
- ✅ **Cell 14 ("Reading Figure 6.4(b)") rewritten** — dropped the stale "two coordinated views / angle inset on the right"; now describes the single diagram (bent ray, θ₁–θ₄, normals/θ_S, C₁/C₂ height brackets, a/b/d distance brackets). Removed "renders".
- ✅ **First-person voice removed** in markdown cells 0, 2, 5, 6, 12, 16 → second-person/neutral. Verified 0 remaining `we/our/let's`.
- ✅ **Empty markdown cell deleted.**
- ✅ **Intro (cell 0) re-scoped** to delivered content (Snell's law → lensmaker's formula); depth-of-field and telescope promises removed until those sections land.

### Dead code

- ✅ **`draw_surface_slice` removed** from drawing-helpers (orphaned by the dropped angle-inset, 0 refs). 6.4(b) re-rendered **byte-identical** (md5 `997f249b…`).
- ✅ **Deleted (confirmed 2026-06-24):** `visually_exaggerate_angle` (drawing-helpers) + `theta23_scale`, `theta23_target_min_deg`, `theta23_target_max_deg` (6.4b params). 6.4(b) re-rendered **byte-identical**.

### ✅ Fig 6.4(b) "regression" check — RESOLVED, no regression (premise correction)

- `back_hit` is computed from `theta2_axis` in the live cell **and** in the committed `working 6.2` (f0a461a). `theta2_display`/`visually_exaggerate_angle` **never** fed `back_hit` in any version — they only ever drove the dropped angle-inset's exaggerated wedges.
- Current render **is** the intended look: in-glass ray slopes ~3.7°, θ₂ at the front, θ₃ at the back, clearly separated. Readability comes from the exaggerated lens *gap* (`exaggeration=5`) + leader-annotated θ₂/θ₃, not from exaggerating the ray angle.
- ∴ the four names are genuinely orphaned (inset leftovers), safe to delete. Held only because this contradicts the original "stale cramped version" premise — awaiting confirmation.

### ✅ RESOLVED — notebook now executes top-to-bottom (execution-order bug)

Drawing-helpers cell sat at index 13 while Fig 6.3(a) (index 7) calls `draw_angle` (defined in 13), so sequential execution (`execute_notebook.py` / papermill) failed at cell 7 with `NameError: draw_angle`. **Fixed 2026-06-24:** moved the drawing-helpers cell to immediately after the physics-helpers cell (now cells 3 → 4), which also resolves its odd mid-document placement. Full top-to-bottom execution now succeeds; all three figures re-rendered **byte-identical** (03a `e8e05145…`, 04a `ca8f13b4…`, 04b `997f249b…`).

### Note — `hide-input` on the drawing-helpers cell vs the contract

Cell 13 (drawing helpers) is tagged though it's a "helper" cell. Reconciliation: it's plotting-only scaffolding with no computational output → hidden as page-noise. The physics-helpers cell stays untagged because its sanity prints are teaching output. Refined rule: tag **plotting-only support cells**; leave **computation/reference cells** untagged.

### Tier B dispositions

**Closed — do not revisit:**
- ✅ **6.4(a) lens refactor — CLOSED.** The arc-based lens is the right shape for 6.4(a)'s clean symmetric construction; `draw_biconvex_lens` was tuned for 6.4(b)'s proportions. Two similar-looking call sites are not the same need.

**6.4(b) consolidation pass (final cleanup) — deferred, ONE job, explicit trigger:**
> **Trigger:** do this when re-rendering the whole notebook for final execution, after confirming byte-identity is no longer the constraint. Then loop + route-through-`draw_angle` **together**, verifying renders after.
- Loop the symmetric front/back surface blocks and the symmetric bracket blocks in 6.4(b).
- Route 6.4(b)'s ~10× `center + radius * torch.stack([cos, sin])` angle-draw idiom through the existing `draw_angle` helper. **Not** by reviving the removed global `point_from_angle` wrapper (that judgment stands) — these are angle-drawing call sites that belong inside `draw_angle`.
- Do **not** do piecemeal now: image-risky mid-build for modest payoff.

---

## 2026-06-23 — Standard adopted; audit findings logged as open issues

Source of these items: `workflow/audit-2026-06-23.md`. Nothing applied yet —
awaiting human direction on order.

### Faithfulness to the book

- 🔴 **Stale intro for Fig 6.4(b) (cell 14).** Markdown still describes "two
  coordinated views… an angle inset on the right," but that supplementary figure
  (`fig06_04b_angles.png`) was dropped — the cell now renders one labeled diagram.
  Rewrite to describe the single figure. Book ref: §6.2, Fig 6.4(b).
- 💬 **Intro (cell 0) over-promises unbuilt sections.** Names a depth-of-field
  section (Kornia blur, f/2-vs-f/8) and a telescope, neither present yet. Book
  §6.3.1 (Depth of Field) and the telescope material are still ⬜ in TODO.md.
  Decide: scope the intro to what exists, or treat as a forward promise.
- 🔴 **Sign-convention drift in markdown (cell 5).** The derivation cell still
  prints `1/f = (n-1)(1/R1 − 1/R2)` (signed/Hecht form), but the code now uses the
  book's magnitudes form `1/f = (n-1)(1/R1 + 1/R2)` (`focal_length`, cell 3). Book
  §6.2 uses magnitudes. Markdown and code disagree on sign — reconcile to the
  book. (Not in the original audit; noticed while re-reading §6.2.)

### Coherence as one document

- 🔴 **`hide-input` tag regression.** Figure cells 7 (6.3a) and 9 (6.4a) lost the
  tag; only 13 and 15 carry it. All pure-plotting cells must be tagged.
- 🔴 **First-person voice in 6 markdown cells** (0, 2, 5, 6, 12, 16): "we"/"our".
  Convert to evergreen/second-person.
- 🔴 **Empty markdown cell 11** — structural noise between cells 10 and 12.
- 💬 **Angle-drawing style is inconsistent across figures.** 6.3(a) uses the
  `draw_angle` helper; 6.4(a) hand-rolls an arc via `ax.plot`; 6.4(b) hand-rolls a
  `FancyArrowPatch` arc-arrow. One document, three idioms. Unifying is pixel-risky
  on completed figures — discuss.

### Code quality / bloat

- 🔴 **Dead helpers** in drawing-helpers cell (13): `visually_exaggerate_angle`,
  `draw_surface_slice` — never called anywhere (orphaned by the dropped angle
  inset). Remove. ⚠️ touching cell 13 → re-render 6.4(b) and byte-compare.
- 🔴 **Dead parameters** in 6.4(b) cell (15): `theta23_scale`,
  `theta23_target_min_deg`, `theta23_target_max_deg` — used 0×. Remove and verify
  PNG unchanged.
- 💬 **Fig 6.4(a) hand-rolls its lens shape** (circular arcs) instead of
  `draw_biconvex_lens`/`lens_curves`. Genuinely different shape — refactor WOULD
  change the PNG. Only with explicit sign-off to re-bless the figure.
- 💬 **Repeated idioms** worth a loop/helper but pixel-risky: 6.4(a) `a`/`b`
  bracket triplets (6× `ax.plot`); 6.4(b) front/back surface blocks and the ~10×
  `center + len*stack([cos,sin])` idiom (the previously-removed `point_from_angle`).

### Clean / confirmed good (2026-06-23)

- ✅ Zero NumPy anywhere.
- ✅ Inline code comments: no toolchain/voice violations.
- ✅ `images/` holds exactly `fig06_03a.png`, `fig06_04a.png`, `fig06_04b.png`;
  no stray/versioned files.
- ✅ Branch `mit-book-chapter-6-1` checked out.

### Book-coverage snapshot (per TODO.md)

Built: 6.3(a), 6.4(a), 6.4(b). Deliberately skipped (photographic, acknowledged
in prose): 6.3(b), 6.7. Not yet started: 6.1, 6.2-intro figs, 6.5, 6.6, 6.8(a–c),
6.9(a–e), and the §6.3.1 depth-of-field + telescope material the intro promises.
