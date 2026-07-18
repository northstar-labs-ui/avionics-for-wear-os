# Contributing

Contributions that improve compatibility, accessibility, documentation, and
the aviation-inspired designs are welcome.

## Before starting

1. Search existing issues before opening a new one.
2. For a substantial design or behavior change, open an issue first so the
   approach can be discussed.
3. Work in the directory for the watch face you are changing. Each watch face
   is a separate Gradle project.

## Development workflow

1. Fork the repository and create a focused branch.
2. Open the affected project directory in Android Studio.
3. Keep runtime artwork compatible with the project's Watch Face Format
   version and minimum SDK.
4. Build the affected watch face:

   ```powershell
   .\gradlew.bat :watchface:assembleDebug --console=plain
   ```

5. Test active and ambient modes on an emulator or physical Wear OS device.
6. If the visual design changes, update the project picker preview and add a
   representative device capture under `screenshots/`.
7. Submit a pull request that explains the change and how it was verified.

## Pull request expectations

- Keep changes limited to one concern where practical.
- Preserve original artwork sources and document how generated visual assets
  can be reproduced.
- Include accessibility text for user-facing options and complications.
- Do not commit APKs, app bundles, build directories, `local.properties`, IDE
  state, environment files, credentials, passwords, or signing keys.
- Do not include artwork, fonts, or code unless you have the right to license
  them for redistribution. Add attribution and license notices when required.
- Run the relevant Gradle build and describe device or emulator testing in the
  pull request.

## Reporting bugs

Use the GitHub bug report form and include the watch model, Wear OS version,
affected watch face, reproduction steps, and screenshots when useful. Remove
serial numbers, network addresses, account details, and other personal data
from logs and screenshots before uploading them.

## License

By contributing, you agree that your contribution is licensed under the GNU
General Public License v3.0. You must have the right to submit all included
code and assets under compatible terms.
