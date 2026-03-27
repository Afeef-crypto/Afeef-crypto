# Profile assets

This folder holds **static assets** for [`Afeef-crypto/Afeef-crypto`](https://github.com/Afeef-crypto/Afeef-crypto) (the special GitHub profile repository).

| Path | Purpose |
|------|--------|
| `banners/` | **`profile-peek-banner.gif`** — animated peek loop (bob motion). The build script recolors the PNG’s teal/navy backdrop to **black + dark red** to match the profile README, then quantizes to GIF. |
| `cards/` | **LeetCode** stats: `*.svg` generated in Python, then **`rsvg-convert` → `*.png`** in CI (README `<img>` uses **PNG** — GitHub blocks many SVG loads). [**Update LeetCode stats**](https://github.com/Afeef-crypto/Afeef-crypto/actions/workflows/update-stats.yml). |
| `snake/` | **Contribution snake** from [`.github/workflows/snake.yml`](../.github/workflows/snake.yml): **SVG** from **`Platane/snk/svg-only@v3`**, then **`github-contribution-grid-snake-dark.png`** via `rsvg-convert` for README. **Workflow permissions** → **Read and write**. |

### Peek banner GIF

When you replace **`profile-peek-banner.png`**, run [**Build profile peek GIF**](https://github.com/Afeef-crypto/Afeef-crypto/actions/workflows/build-peek-gif.yml) (or let the workflow run on push). It runs [`scripts/build_peek_gif.py`](../scripts/build_peek_gif.py) (backdrop recolor + bob) and commits the updated **`.gif`**.
