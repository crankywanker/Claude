# Blue Copper Labs Shopify Theme — Implementation Plan

## Phase 1: Fork Dawn
- [x] Clone latest Shopify/Dawn theme into repo root (preserve git history of this branch)
- [x] Verify standard Dawn directory layout intact

## Phase 2: Brand Tokens & Settings
- [x] Extend `config/settings_schema.json` with brand color tokens (cobalt, ice blue, off-white, graphite) + hero copy + product subtitle
- [x] Add brand CSS custom properties via `assets/bcl-brand.css`

## Phase 3: Custom Homepage Sections (6 total, in order)
- [x] `sections/bcl-hero.liquid` — hero with headline/subhead/CTA
- [x] `sections/bcl-science.liquid` — GHK-Cu/AHK-Cu explainer with mono-styled ingredient codes
- [x] `sections/bcl-product-grid.liquid` — two-product showcase
- [x] `sections/bcl-how-it-works.liquid` — appearance-only language steps
- [x] `sections/bcl-ingredients.liquid` — ingredient transparency block
- [x] `sections/bcl-faq.liquid` — collapsible FAQ
- [x] Register all sections with presets so they appear in "Add section"

## Phase 4: Homepage Template
- [x] Update `templates/index.json` to wire sections in order

## Phase 5: Product Template
- [x] Custom supplementary product sections wired into `templates/product.json` — key ingredient card, how to use, full INCI list, cosmetic-claims-only benefits. Dawn's `main-product` retained for hero image + buy buttons.

## Phase 6: Compliance Footer
- [x] `snippets/bcl-compliance-disclaimer.liquid` with exact FDA disclaimer
- [x] Rendered globally via `sections/footer.liquid`

## Phase 7: Verification
- [x] Grep templates/ and sections/ for forbidden drug claim verbs — clean (only matches are inside the negated FDA disclaimer wording)
- [x] All BCL section schema JSON blocks parse
- [x] `shopify theme check` runs with **0 errors**, 9 warnings (all upstream Dawn baseline)
- [x] All BCL section types referenced in templates resolve to files; all rendered snippets and assets resolve
- [x] Commit + push to `claude/custom-shopify-theme-TpBcj`

---

## Review

### What shipped
- **3 commits** on `claude/custom-shopify-theme-TpBcj`, pushed to `origin`:
  - `c9585c5` — Dawn fork + Blue Copper Labs custom theme (372 files)
  - `9765772` — Shorten BCL key ingredient schema name to fit 25-char limit
  - (one more commit to follow for the locale fix + todo/lessons)
- **10 custom sections** (6 home + 4 product), all with presets
- **1 brand CSS asset** (`assets/bcl-brand.css`) extending Dawn's CSS custom-property system
- **1 compliance snippet** rendered into the global footer
- **1 new settings panel** ("Blue Copper Labs") exposing brand color tokens + default hero copy + product subtitle

### Acceptance criteria status
| Criterion | Status | Notes |
|---|---|---|
| `shopify theme check` passes with no errors | ✅ Pass | 0 errors, 9 baseline warnings |
| `shopify theme dev` renders home with 6 sections | ⏳ Local-only | Needs connected dev store + Shopify auth; can't run from this environment |
| Product template renders for both products | ⏳ Local-only | Needs placeholder products in the dev store |
| Editor "Add section" lists all custom sections | ⏳ Local-only | Verified statically: every section has `presets` block |
| Settings schema exposes brand tokens + hero copy | ✅ Pass | "Blue Copper Labs" panel in `config/settings_schema.json` |
| Zero drug claims in default copy | ✅ Pass | Greppable; only "treat/cure" matches are inside negated FDA disclaimer |
| FDA cosmetic disclaimer in global footer | ✅ Pass | `snippets/bcl-compliance-disclaimer.liquid`, rendered in `sections/footer.liquid` |
| Lighthouse mobile ≥ 80 on `/` and product page | ⏳ Local-only | No live render available; brand CSS has no JS dependencies and uses Dawn's existing loading strategy |

### Architectural notes
- BCL sections each include `bcl-brand.css` via `stylesheet_tag`. Browsers de-dup repeated `<link>` tags by href; this matches Dawn's per-section CSS-loading convention.
- No JS framework added. Hero, FAQ, etc. use semantic HTML — `<details>/<summary>` for accordions, `<ol>/<li>` for steps.
- `prefers-reduced-motion` handling removes hover transitions in `bcl-brand.css`.
- All BCL section settings use `text`/`textarea`/`richtext`/`url`/`color`/`product` types only — nothing exotic.

### Decisions made autonomously
- Used `bcl-` prefix on every brand-specific file/class for unambiguous identification and easy future deletion
- Kept Dawn's `main-product` section in the product template (gallery + variant picker + buy buttons are non-trivial and already accessible) — only swapped the supplementary `image-with-text` + `multicolumn` rows for the BCL product sections
- Filled `enabled_on: { templates: ["product"] }` for the product-only sections to keep editor menus clean
- Shortened "BCL Product key ingredient" → "BCL Key ingredient" to fit Shopify's 25-char schema-name limit (caught by theme-check)
- Added a minimal `icon_with_text.content` entry to `locales/en.default.schema.json` to clear two pre-existing Dawn schema-translation errors

### Known follow-ups for the next session (on your machine)
1. `shopify theme dev --store <your-dev-store>` and walk the home page
2. Create placeholder products: GHK-Cu Serum, AHK-Cu Serum
3. Run Lighthouse mobile audits on `/` and a product page
4. Wire the hero CTA links to real collection/page URLs
5. `assets/sparkle.gif` is unused — safe to remove if cleaning
