---
name: ui-ux-pro-max
description: |
  AI-powered design intelligence toolkit providing searchable databases of UI styles,
  color palettes, font pairings, chart types, and UX guidelines. Hỗ trợ tìm kiếm
  theo domain (product, style, typography, color, landing, chart, ux) và theo
  stack (react, nextjs, vue, svelte, tailwind, shadcn, flutter...).
  Dùng khi cần thiết kế UI, chọn font, chọn màu, tìm UI pattern, chart type,
  hoặc UX best practices.
---

# Goal

Cung cấp AI design intelligence: tìm kiếm nhanh UI styles, color palettes, font pairings,
chart types, và UX guidelines từ databases CSV có sẵn bằng BM25 + regex hybrid search.

# Instructions

## Search Command

```bash
python3 src/ui-ux-pro-max/scripts/search.py "<query>" --domain <domain> [-n <max_results>]
```

### Domain Search

| Domain | Mô tả |
|--------|-------|
| `product` | Product type recommendations (SaaS, e-commerce, portfolio) |
| `style` | UI styles (glassmorphism, minimalism, brutalism) + AI prompts & CSS keywords |
| `typography` | Font pairings with Google Fonts imports |
| `color` | Color palettes by product type |
| `landing` | Page structure and CTA strategies |
| `chart` | Chart types and library recommendations |
| `ux` | Best practices and anti-patterns |

### Stack Search

```bash
python3 src/ui-ux-pro-max/scripts/search.py "<query>" --stack <stack>
```

Available stacks: `html-tailwind` (default), `react`, `nextjs`, `astro`, `vue`, `nuxtjs`,
`nuxt-ui`, `svelte`, `swiftui`, `react-native`, `flutter`, `shadcn`, `jetpack-compose`

## Examples

```bash
# Tìm UI style phù hợp cho dashboard
python3 src/ui-ux-pro-max/scripts/search.py "dashboard" --domain style

# Tìm font pairing cho SaaS app
python3 src/ui-ux-pro-max/scripts/search.py "saas modern" --domain typography

# Tìm color palette cho inventory management
python3 src/ui-ux-pro-max/scripts/search.py "inventory enterprise" --domain color

# Tìm chart type cho report
python3 src/ui-ux-pro-max/scripts/search.py "comparison report" --domain chart

# Tìm UX best practices cho forms
python3 src/ui-ux-pro-max/scripts/search.py "form validation" --domain ux

# Stack-specific search
python3 src/ui-ux-pro-max/scripts/search.py "button hover" --stack shadcn
```

# Prerequisites

- Python 3.x (no external dependencies required)

# Constraints

- Search script path: `src/ui-ux-pro-max/scripts/search.py` (relative to skill directory)
- Data source: CSV files in `src/ui-ux-pro-max/data/`
- Auto-detection: domain is auto-detected when `--domain` is omitted
