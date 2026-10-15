# Maintaining this profile

This public repository must have exactly the same name as the GitHub username and contain a root README.md to appear on the profile.

- Edit biography, skills, project links, and contact links in `README.md`.
- Local SVGs in `assets/` provide the hero, clickable project cards, and process animation. They contain no scripts or tracking pixels.
- GitHub renders Markdown, links, images, and expandable `<details>` sections. The profile does not require JavaScript or an external badge/stats service.
- `scripts/update_profile.py` reads only public GitHub data and generates `assets/github-snapshot.svg` and `data/public-snapshot.json`.
- The scheduled workflow runs daily and can also be started manually from Actions. It uses only the repository's built-in `GITHUB_TOKEN` with contents-write permission to commit generated changes.
- Local refresh: `python scripts/update_profile.py`. Python 3.11+ is recommended; there are no pip dependencies.
- Preserve attribution and review notes inside linked project repositories. No job title, degree, employment history, or accuracy/performance claims are invented here.

The provided LinkedIn URL was corrected to `https://www.linkedin.com/in/sheikh-muhammed-abdullah/`. It was supplied by the profile owner; external account ownership is not independently verified.
