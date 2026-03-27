# Profile assets

This folder holds **static assets** for [`Afeef-crypto/Afeef-crypto`](https://github.com/Afeef-crypto/Afeef-crypto) (the special GitHub profile repository).

| Path | Purpose |
|------|--------|
| `banners/` | **`profile-peek-banner.gif`** — animated peek loop (bob motion). The build script recolors the PNG’s teal/navy backdrop to **black + dark red** to match the profile README, then quantizes to GIF. |
| `cards/` | **LeetCode** SVGs (`lc_main.svg`, `lc_contests.svg`). README embeds them via **`raw.githubusercontent.com/.../main/assets/cards/...`** so the blob preview shows images. Refreshed by [**Update LeetCode stats**](https://github.com/Afeef-crypto/Afeef-crypto/actions/workflows/update-stats.yml). |
| `snake/` | **Contribution snake** animated **SVGs** from [`.github/workflows/snake.yml`](../.github/workflows/snake.yml) (**`Platane/snk/svg-only@v3`** — avoids Docker GIF failures). README embeds **`.../github-contribution-grid-snake-dark.svg`** via `raw.githubusercontent.com`. **Workflow permissions** → **Read and write**. |

### Peek banner GIF

When you replace **`profile-peek-banner.png`**, run [**Build profile peek GIF**](https://github.com/Afeef-crypto/Afeef-crypto/actions/workflows/build-peek-gif.yml) (or let the workflow run on push). It runs [`scripts/build_peek_gif.py`](../scripts/build_peek_gif.py) (backdrop recolor + bob) and commits the updated **`.gif`**.
