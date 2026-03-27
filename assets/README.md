# Profile assets

This folder holds **static assets** for [`Afeef-crypto/Afeef-crypto`](https://github.com/Afeef-crypto/Afeef-crypto) (the special GitHub profile repository).

| Path | Purpose |
|------|--------|
| `banners/` | Optional local images or SVGs you reference from `README.md` with **relative** paths (e.g. `assets/banners/your-banner.svg`). |
| `cards/` | Reserved for generated or hand-made stat cards (e.g. SVG widgets). Commit files here and link them from the README. |

## Generated on another branch

The **contribution snake** animations are **not** stored on `main`. They are produced by [`.github/workflows/snake.yml`](../.github/workflows/snake.yml) and deployed to the **`output`** branch. The README loads them from:

`https://raw.githubusercontent.com/Afeef-crypto/Afeef-crypto/output/github-contribution-grid-snake.svg`  
`https://raw.githubusercontent.com/Afeef-crypto/Afeef-crypto/output/github-contribution-grid-snake-dark.svg`

After the first workflow run, open **Actions → Generate contribution snake** and confirm it succeeded. If pushes fail, set **Settings → Actions → General → Workflow permissions** to **Read and write**.
