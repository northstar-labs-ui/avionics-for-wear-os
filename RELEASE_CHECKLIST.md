# Release checklist

Use this checklist for each watch face included in a release.

## Scope and metadata

- [ ] Confirm the release scope and version number.
- [ ] Update user-facing documentation and screenshots for changed behavior.
- [ ] Review third-party notices, asset origins, and license compatibility.
- [ ] Confirm package IDs, version codes, version names, minimum SDKs, and
      target SDKs are correct.
- [ ] Confirm the working tree contains no credentials, signing material,
      `local.properties`, APKs, app bundles, or generated build directories.

## Validation

- [ ] Run the debug build for every changed project.
- [ ] Run the release build with the maintainer's private signing setup kept
      outside the repository.
- [ ] Run lint and any available Watch Face Format validation tools.
- [ ] Test installation or upgrade on a supported physical Wear OS device.
- [ ] Verify the watch-face picker name and preview.
- [ ] Verify hour, minute, second, date, complication, and customization
      behavior as applicable.
- [ ] Verify active, ambient, and low-bit/burn-in behavior as applicable.
- [ ] Check multiple display sizes and round-screen edge clipping.
- [ ] Review battery use and confirm no unexpected rendering errors appear.

## GitHub release

- [ ] Review the final commit range and staged content for secrets or binaries.
- [ ] Create an annotated version tag from the intended commit.
- [ ] Write release notes with highlights, compatibility, known issues, and
      installation guidance.
- [ ] Attach only approved release artifacts; never attach debug builds,
      keystores, credentials, mapping files, or local configuration.
- [ ] Publish the GitHub release and verify its links and downloadable assets.
- [ ] Install the published artifact once as a final smoke test, if artifacts
      are distributed.
