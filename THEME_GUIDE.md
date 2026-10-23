# PipSpool themes

Choose a dashboard theme or create your own colour palette using a small JSON file. Themes change the PipSpool dashboard's colours and can add a local background image while keeping spool colours, identification and synchronization behaviour intact.

This guide describes **theme format version 1**, available in **PipSpool 2.2.16 and later**.

## Choose a theme

Use the **Theme** dropdown beside **Feedback** on the PipSpool dashboard.

| Theme | Appearance |
| --- | --- |
| PipSpool Classic | Original dark blue dashboard. |
| Light | Pale backgrounds, dark text and a blue primary action. |
| Forest | Dark green surfaces and green accents. |
| Rosewood | Rich oxblood-red surfaces, ruby-red actions and warm ivory text. |
| Bonus Treat | Purple surfaces, pumpkin-orange actions and an autumn night background. |
| Example theme (example.json) | Editable starter palette stored in your themes folder. |

Bonus Treat includes an embedded background and matching happy/sad Pip artwork; no extra files are needed.

Changes apply immediately and the selection is saved automatically. No synchronization or restart is needed to change themes. Themes affect the dashboard; OrcaSlicer's interface and the separate PipSpool Settings window keep their own appearance.

## Find the themes folder

Open the PipSpool dashboard once. PipSpool creates a `themes` folder and an editable `example.json` file when folder access is available. That file appears as **Example theme (example.json)** in the dropdown. Built-in themes live inside the plugin and have no JSON filename beside their name.

**Hover over the Theme dropdown to see the exact folder path for your installation.** The normal layout is:

```text
<OrcaSlicer data directory>/
└── pipspool/
    └── themes/
        ├── example.json
        ├── violet.json
        └── images/
            └── wallpaper.jpg
```

### Default installation paths

These examples cover all five supported PipSpool packages. CPU architecture does not change the folder location within the same operating system.

| Supported platform | Default themes folder |
| --- | --- |
| Windows x86-64 | `%APPDATA%\OrcaSlicer\pipspool\themes` |
| Linux x86-64 (AppImage/native) | `~/.config/OrcaSlicer/pipspool/themes` |
| Linux ARM64 (native) | `~/.config/OrcaSlicer/pipspool/themes` |
| macOS Intel (x86-64) | `~/Library/Application Support/OrcaSlicer/pipspool/themes` |
| macOS Apple Silicon (ARM64) | `~/Library/Application Support/OrcaSlicer/pipspool/themes` |

On Windows, press **Windows+R**, paste the following command, and press **Enter**:

```text
explorer.exe "%APPDATA%\OrcaSlicer\pipspool\themes"
```

This opens the themes folder in File Explorer.

For an account named `alex`, the folder normally expands to:

```text
C:\Users\alex\AppData\Roaming\OrcaSlicer\pipspool\themes
```

On Linux and macOS, `~` means your home folder. For an account named `alex`, examples are:

```text
Linux:  /home/alex/.config/OrcaSlicer/pipspool/themes
macOS:  /Users/alex/Library/Application Support/OrcaSlicer/pipspool/themes
```

In macOS Finder, press **Command+Shift+G** and paste the macOS path from the table to open it, including the normally hidden Library folder.

For **Linux Flatpak**, the host-side default is:

```text
~/.var/app/com.orcaslicer.OrcaSlicer/config/OrcaSlicer/pipspool/themes
```

These locations append `pipspool/themes` to [OrcaSlicer's documented configuration folders](https://www.orcaslicer.com/wiki/user_profiles/user_profiles). Portable installations, custom data directories and Linux configuration overrides can use a different location. Check the dropdown tooltip for PipSpool's actual path. You can also open Orca's configuration folder from its Help menu, then navigate to `pipspool/themes`.

Use your OrcaSlicer data directory, not its program installation directory. Avoid placing palettes beside downloaded plugin packages, which can be replaced during updates.

For a script installed outside a directory named `OrcaSlicer`, the fallback location is `<plugin script folder>/pipspool/themes`. The dropdown tooltip is the best way to check which path is being used.

If Orca requests folder access, check that the path matches the intended theme folder. Built-in themes remain available if custom theme files cannot be read.

## Create a theme

1. Copy `example.json` to a new file such as `violet.json` in the same folder.
2. Open the copy in a plain-text editor and save it as UTF-8 JSON.
3. Keep `version` set to `1`, set a display `name`, and edit the `colors` values. Set the optional `background_image` and `background_opacity` in this **same JSON file** if you want wallpaper.
4. Click **Refresh** on the PipSpool dashboard to scan the folder again.
5. Select your theme from the **Theme** dropdown.

Refresh also performs the normal dashboard refresh; it does not synchronize profiles. After editing the currently selected palette, click Refresh to apply the new colours. Reopening the page also reloads palettes.

### One complete theme file

Each theme needs **one JSON file** containing both its colours and optional wallpaper settings. You do not need a second wallpaper JSON file. `example.json` is a starter you can edit directly or copy; it is not a dependency of other themes.

Save the following as `violet.json`. For wallpaper, place your image at `themes/images/wallpaper.jpg`. Leave `background_image` empty (`""`) for a colour-only theme:

```json
{
  "version": 1,
  "name": "Violet",
  "colors": {
    "background": "#171222",
    "surface": "#241c35",
    "surface_alt": "#302441",
    "text": "#f3edf9",
    "muted": "#c4b5d4",
    "accent": "#bc95ef",
    "accent_text": "#21112f",
    "border": "#77578f",
    "heading": "#f5eaff",
    "highlight": "#d5bbff",
    "good": "#8dd6a5",
    "warning": "#f0c075",
    "danger": "#fa9696"
  },
  "background_image": "wallpaper.jpg",
  "background_opacity": 0.35
}
```

Custom themes appear as **Name (filename.json)**, so this example appears as **Violet (violet.json)**. The name comes from the JSON `name` field; the filename shows exactly which file to edit. New files use **Example theme** as the starter name. Older `example.json` files still named **My Theme** are displayed as **Example theme (example.json)** without rewriting the file or changing its colours.

## Add a background image

Image backgrounds are optional and are included in **PipSpool 2.2.16 and later**.

1. Put your PNG, JPEG or WebP image in the `images` subfolder inside your themes folder.
2. Open the theme JSON you already use, such as `example.json` or `violet.json`.
3. Set `background_image` to that image's filename and adjust `background_opacity` in the same file, alongside `colors`. If these properties are missing from an older file, add them using the complete example above.
4. Click **Refresh**. Keep the same theme selected; no separate wallpaper theme is needed.

New starter files include both properties. Existing theme files are preserved. For example, a Violet theme with wallpaper consists of only:

```text
themes/
├── violet.json               Colours and wallpaper settings together
└── images/
    └── wallpaper.jpg         The image referenced by violet.json
```

You can edit `example.json` directly instead; in that case it is your single theme JSON. Other JSON files in the folder represent independent themes, not layers that must be combined. Refresh also reloads the image after you replace its file.

| Property | Meaning |
| --- | --- |
| `background_image` | Image filename inside `themes/images`, such as `wallpaper.jpg`. Do not include a folder path or URL. |
| `background_opacity` | A number from `0` to `1`. Defaults to `0.35`. `0` hides the image behind the background colour; `1` shows it without a colour veil. |

The image fills the page background, stays centred while scrolling, and is cropped to cover the viewport. Cards retain solid surfaces so their controls and text remain readable. The palette's `background` colour provides the veil over the image, so adjust opacity for both header and footer readability.

Supported files are `.png`, `.jpg`, `.jpeg` and `.webp`, up to **4 MiB** each. Filenames must begin with a letter or digit, contain only letters, digits, dots, hyphens and underscores, and be no longer than 120 characters including the extension. Consecutive dots, paths, symbolic links, remote URLs and SVG files are not accepted.

Only the selected theme's image is read and displayed. A brief colour-only background during startup is normal while the local image loads. No image is uploaded or fetched from an external server. If the image is missing, inaccessible, too large or has an unsupported file signature, the theme uses its colours without the image. If a file cannot be decoded by the browser, the background colour remains underneath it. Invalid image properties are ignored without removing an otherwise valid palette.

To remove a background, set `background_image` to an empty string or remove it from the JSON and click Refresh, or select a theme without an image.

## Colour reference

| Key | Controls |
| --- | --- |
| `background` | Page background. |
| `surface` | Cards, table headings, empty gate/toolhead slots and secondary button hover backgrounds. |
| `surface_alt` | Inputs, dropdowns, secondary buttons, badges, menus, report areas and loaded gate/toolhead cards. |
| `text` | Main text and control labels. |
| `muted` | Secondary descriptions and labels. |
| `accent` | Primary actions, active tabs, selected filters and checkbox accents. |
| `accent_text` | Text on the accent background. |
| `border` | Card, control and table borders. |
| `heading` | Page and section headings. |
| `highlight` | Links and highlighted indicators. |
| `good` | Positive profile status indicators. |
| `warning` | Warning accents, including restart and low-stock accents. |
| `danger` | Error and conflicting or missing profile indicators. |

You may provide only some colour keys; omitted values use **Classic** defaults. For a light theme, supply the complete palette so light text inherited from Classic does not disappear on pale surfaces.

Spool swatches, artwork, inventory gauges and some specialised indicators retain their own content colours. Themes provide colour palettes and optional background images rather than complete layout replacements.

### Keep the dashboard readable

- Choose contrasting `text` and `surface`/`surface_alt` colours.
- Check `accent_text` against `accent`, including primary buttons and active tabs.
- Make `muted` text readable on both surfaces.
- Keep positive, warning and error states distinguishable.
- Check buttons when hovered, dropdown options, table headings, field checkboxes and expanded column menus.

## File format and limits

| Item | Requirement |
| --- | --- |
| File name | 1–48 characters before `.json`; lowercase letters, digits, hyphens and underscores; begin with a letter or digit. |
| `version` | Set to `1`. |
| `name` | 1–60 characters after trimming surrounding whitespace. |
| `colors` | An object containing at least one of the keys listed above. Unknown colour keys cause the file to be skipped. |
| Colour values | Exactly six hexadecimal digits prefixed with `#`, such as `#1269b0`. |
| File size | At most 16 KiB. |
| Discovery | Up to 100 JSON files, scanned in filename order. Symbolic-link files are skipped. |

Use double quotes. JSON does not allow comments or trailing commas. Theme names are displayed as text.

Palettes do not support raw CSS, HTML, scripts, remote URLs, external fonts, layout rules or synchronization settings. Local raster background images use the optional properties described above.

## Share a theme

Share the JSON palette, any referenced background image you have permission to share, and optionally a screenshot. To install a shared theme:

1. Copy its `.json` file into your own themes folder.
2. If supplied, copy the background image into the `images` subfolder.
3. Click **Refresh** on the dashboard.
4. Select the theme by its display name and filename.

Built-in themes are embedded in PipSpool. Custom palette filenames cannot replace them. Include the theme format version when sharing a palette so users can check compatibility.

## Troubleshooting

### A custom theme does not appear

Check the folder shown in the dropdown tooltip, then verify the filename, JSON syntax, colour keys, colour values, file size and access permissions. Click Refresh after saving. Invalid files are skipped.

### Colours are hard to read

Start with a complete palette and check the text/background pairs in the colour reference. A partial light palette inherits Classic's remaining dark-theme colours. Check hover states and selected controls as well as the page background.

### A selected theme disappeared

If a selected file is removed or becomes invalid, PipSpool falls back to Classic. Select another theme to save a replacement preference. Profile data and synchronization choices are unaffected.

### I want to restore the original dashboard

Select **PipSpool Classic**. You do not need to delete custom palette files.

## Theme testing checklist

Before sharing a palette:

- [ ] Check the header, dropdown, Feedback, Refresh and Synchronize buttons.
- [ ] Hover over buttons and inspect selected filters and active tabs.
- [ ] Inspect dropdown options, the column menu, table headings and field labels.
- [ ] Check normal, low-stock, error and conflict indicators when those states are available.
- [ ] If using an image, check header and footer contrast and scrolling.
- [ ] Switch to a colour-only theme and confirm the old background image clears.
- [ ] Switch to another theme and back.
- [ ] Restart Orca and confirm the selection is remembered.
- [ ] Edit the selected palette and click Refresh to confirm it reloads.
- [ ] Remove or temporarily invalidate a copy and confirm Classic provides a readable fallback.

Switching themes should never synchronize profiles or change your selected synchronization fields.
