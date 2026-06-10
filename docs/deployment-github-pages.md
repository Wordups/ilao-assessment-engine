# GitHub Pages Deployment Notes

## What ships to Pages

The repository includes a static public-facing site in `docs-site/`. It is separate from the React application and is intended for:

- framework explanation
- public project overview
- roadmap and use cases
- linking back to the source repository

## Recommended GitHub Pages setup

1. Push the repository to GitHub.
2. In the repository settings, open `Pages`.
3. Set the source to `GitHub Actions`.
4. Ensure the workflow in `.github/workflows/pages.yml` is enabled.
5. Update the placeholder repository link in `docs-site/index.html`.

## Publishing behavior

- Any push to `main` or `master` that changes `docs-site/**` can trigger a Pages deploy.
- You can also trigger the workflow manually from the Actions tab.

## Optional next step

If you want the marketing site and app to share branding later, you can migrate the static site into a Vite landing page build. For this public-ready MVP, the plain static site keeps deployment simple and reliable.
