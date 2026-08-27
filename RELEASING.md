# Releasing PipSpool

PipSpool publishes to Orca Cloud through GitHub Actions and GitHub's short-lived OIDC identity. No repository secret or permanent Orca Cloud token is required.

## One-time Orca Cloud connection

1. Sign in to [Orca Cloud](https://cloud.orcaslicer.com/).
2. Open **Plugins → Shared Plugins**.
3. Create or open the PipSpool plugin listing.
4. Choose **Edit plugin**.
5. Under **GitHub publishing**, enter `Gadonk/pipspool-orcaslicer`.
6. Click **Connect**.

One GitHub repository can publish to one Orca Cloud plugin.

## Publish a new version

1. Confirm the plugin works in OrcaSlicer.
2. Use a stable semantic version in the plugin metadata, without `-dev`.
3. Commit exactly one current release artifact matching:
   `pipspool_v<major>_<minor>_<patch>_win_x86_64.py`
4. Remove the superseded release artifact from the repository.
5. Confirm the public file uses `http://localhost:7912` and contains no private network address.
6. Update `README.md`, `CHANGELOG.md`, and `tests/test_pipspool.py`.
7. Publish a GitHub Release using a matching tag, such as `v2.0.7`.
8. Put the user-facing change summary in the GitHub Release notes.

Publishing the GitHub Release triggers `.github/workflows/publish-orcacloud.yml`. The workflow verifies that exactly one Windows x86-64 plugin file exists, its metadata matches the release tag, the public URL is safe, and no development marker remains. It then uploads the plugin and release notes to Orca Cloud.

Ordinary commits and pushes do not publish to Orca Cloud.
