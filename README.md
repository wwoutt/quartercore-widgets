# Quartercore widgets

A free catalog of own widgets for the XENEON EDGE kiosk of
[Quartercore](https://github.com/wwoutt/quartercore), a native KDE/Qt program for
Corsair devices on Linux.

> Community project. Not an official Corsair product. Quartercore, the store and
> this catalog were written by Claude (Anthropic's AI model, in Claude Code) for
> [wwoutt](https://github.com/wwoutt). Quartercore builds on
> [OpenLinkHub](https://github.com/jurkovic-nikola/OpenLinkHub) by
> [Nikola Jurković](https://github.com/jurkovic-nikola).

The widget format is the same as the custom widgets of the fork
[wwoutt/OpenLinkHub](https://github.com/wwoutt/OpenLinkHub), so these widgets
also work there.

## Install a widget
Open **XENEON EDGE layout** in Quartercore and click **Widget store**. The
**Reviewed** tab shows the widgets in this catalog; every widget here was
reviewed before it was added, and Quartercore checks every file against the
SHA-256 in `index.json`.

The **Community** tab shows GitHub repositories with the topic
[`quartercore-widget`](https://github.com/topics/quartercore-widget). Those are
**not reviewed**: read the code before installing them.

## Widgets
| Widget | Source | Runs code |
|---|---|---|
| [Home Assistant](widgets/home-assistant) | your Home Assistant (script), with actions | yes |
| [Systeemstatus](widgets/systeemstatus) | Linux script | yes |
| [Wisselkoers EUR](widgets/wisselkoers) | internet | no |

## Make a widget
- **With AI:** copy the
  [AI prompt](https://github.com/wwoutt/quartercore/blob/main/docs/WIDGETS.md#ai-prompt)
  into an AI assistant and describe what you want. It contains the complete
  widget format.
- **By hand:** see the
  [widget guide](https://github.com/wwoutt/quartercore/blob/main/docs/WIDGETS.md#make-a-widget).
  The widgets in [`widgets/`](widgets) are small working examples.

## Share your widget
- **Reviewed:** add it to this catalog with a pull request, see [CONTRIBUTING.md](CONTRIBUTING.md).
- **Community:** put the widget files in the root of your own public GitHub
  repository and add the topic `quartercore-widget`.

## License
The tools and index of this catalog are GPL-3.0-or-later. Every widget states its
own license in its `widget.json`; only GPL-compatible licenses are accepted.
