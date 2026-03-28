# Profile assets

This folder holds **static assets** for [`Afeef-crypto/Afeef-crypto`](https://github.com/Afeef-crypto/Afeef-crypto) (the special GitHub profile repository).

| Path | Purpose |
|------|--------|
| `banners/` | **`profile-peek-banner.gif`** — animated peek loop (bob motion). The build script recolors the PNG’s teal/navy backdrop to **black + dark red** to match the profile README, then quantizes to GIF. |
| `cards/` | **LeetCode** stats: `*.svg` from [`scripts/update_readme.py`](../scripts/update_readme.py) + **`lc_main.png` / `lc_contests.png`** rasterized in [**Profile README assets**](../.github/workflows/profile-readme-assets.yml) (`rsvg-convert`). README `<img>` uses **PNG on `main`**. |
| `snake/` | **Contribution snake** from [**Generate contribution snake**](../.github/workflows/snake.yml) ([Platane/snk](https://github.com/Platane/snk)): **dark red** grid + **red snake**; README uses the **GIF** (`github-contribution-grid-snake-dark.gif`) for reliable animation on the profile. |
| `pacman/` | Unused in the current README (optional; folder may be empty or leftover). |

### Peek banner GIF

When you replace **`profile-peek-banner.png`**, run [**Build profile peek GIF**](https://github.com/Afeef-crypto/Afeef-crypto/actions/workflows/build-peek-gif.yml) (or let the workflow run on push). It runs [`scripts/build_peek_gif.py`](../scripts/build_peek_gif.py) (backdrop recolor + bob) and commits the updated **`.gif`**.

### LeetCode PNGs + contribution snake

- [**Profile README assets**](https://github.com/Afeef-crypto/Afeef-crypto/actions/workflows/profile-readme-assets.yml) — LeetCode card PNGs (scheduled / manual).
- [**Generate contribution snake**](https://github.com/Afeef-crypto/Afeef-crypto/actions/workflows/snake.yml) — animated **GIF** + SVG on `main`.

The profile README uses `raw.githubusercontent.com/.../main/...`; keep the repo **public** so those URLs work on your GitHub profile.
