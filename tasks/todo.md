# Blue Copper Labs Shopify Theme — Implementation Plan

## Phase 1: Fork Dawn
- [ ] Clone latest Shopify/Dawn theme into repo root (preserve git history of this branch)
- [ ] Verify standard Dawn directory layout intact

## Phase 2: Brand Tokens & Settings
- [ ] Extend `config/settings_schema.json` with brand color tokens (cobalt, ice blue, off-white, graphite) + hero copy + product subtitle
- [ ] Add brand CSS custom properties via base.css extension or theme.liquid inline tokens

## Phase 3: Custom Homepage Sections (6 total, in order)
- [ ] `sections/bcl-hero.liquid` — hero with headline/subhead/CTA
- [ ] `sections/bcl-science.liquid` — GHK-Cu/AHK-Cu explainer with mono-styled ingredient codes
- [ ] `sections/bcl-product-grid.liquid` — two-product showcase
- [ ] `sections/bcl-how-it-works.liquid` — appearance-only language steps
- [ ] `sections/bcl-ingredients.liquid` — ingredient transparency block
- [ ] `sections/bcl-faq.liquid` — collapsible FAQ
- [ ] Register all sections with presets so they appear in "Add section"

## Phase 4: Homepage Template
- [ ] Update `templates/index.json` to wire sections in order

## Phase 5: Product Template
- [ ] Custom `templates/product.bcl.json` or modify product sections — hero image, key ingredient card, how to use, full INCI list, cosmetic-claims-only benefits

## Phase 6: Compliance Footer
- [ ] `snippets/bcl-compliance-disclaimer.liquid` with exact FDA disclaimer
- [ ] Wire into global footer

## Phase 7: Verification
- [ ] Grep templates/ and sections/ for forbidden drug claim verbs — must return zero in default copy
- [ ] Visual inspection of section schemas valid JSON
- [ ] Commit + push to claude/custom-shopify-theme-TpBcj

## Constraints Recap
- Vanilla Liquid/CSS/JS only
- Extend Dawn's CSS custom properties, don't replace
- Preserve a11y patterns
- No drug claims: avoid treat/cure/heal/stimulate/regrow/reverse/clinically proven to
- FDA cosmetic disclaimer must appear in footer
