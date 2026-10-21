# Publishing this companion repository

Suggested repository name: `perovskite-thermal-expansion-mlff`.

Suggested description: Analysis tools and validation data for MLFF molecular dynamics of thermal expansion in perovskite oxides, accompanying PRX Energy DOI 10.1103/xwd4-x84g.

1. Select the GitHub owner and repository visibility. The local repository has a `main` branch but no remote or initial commit yet.
2. Select a code license and determine the terms for the included numerical data. No license is granted by this draft package.
3. Create an empty GitHub repository under the selected account. Avoid generating a second README there.
4. From this directory, stage the files and create the initial commit with your own Git identity. Review `git diff --cached --stat` before committing.
5. Add the remote URL shown by GitHub and push `main`.
6. Check the GitHub Actions result. Local tests have passed; hosted CI has not run yet.
7. Add the repository URL to CITATION.cff and the Figshare record when appropriate.

Use requirements-tested.txt for the exact dependency versions used during local verification (Python 3.12); requirements.txt gives the broader intended range. Other Python/package combinations have not been verified locally.
