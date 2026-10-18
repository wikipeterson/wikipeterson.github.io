# Recipe pilot

The public site reads `recipes.json`. PDF downloads are prebuilt files in
`pdf/kindle`, `pdf/paperwhite`, and `pdf/letter`. Google Docs are the editorial
source, but this repository currently has no automatic Docs sync or build job.
Publishing a repository update deploys the saved site snapshot through GitHub Pages.

Only tomato soup, fried rice, and corn bread use the preparation-group pilot.
All other recipe records and individual PDFs retain their existing content.

## Editorial format

- TITLE: recipe name.
- HEADING_1: At a glance, Ingredients, Directions, optional Notes, Source.
- One ingredient paragraph per item, starting with a literal marker.
- HEADING_2 under Directions: numbered cooking-stage name.
- Native numbered paragraphs under each stage: instructions in cooking order.
- Source: original URL and archival attribution. Keep prep questions in Notes.

Marker mapping is semantic; emoji shades are not the website palette:

| Doc marker | Data group | Website/PDF color |
| --- | --- | --- |
| 🟡 | a | Olive `#657344` |
| 🟢 | b | Terracotta `#a0503b` |
| 🔵 | c | Ochre `#886522` |
| 🟣 | d | Slate blue `#526b7a` |
| ⚫ | separate | Charcoal `#35413b` |

Groups are local to each recipe. Ingredients share a letter only when they can
share a prep container. Divided ingredients retain explicit amounts and timing;
separate ingredients do not share a container simply because both are charcoal.

## Data and downloads

Pilot records add `prepGroups` (letter to readable bowl description) and
`ingredients[].prepGroup`. The UI retains the existing checkbox storage keys and
adds both a visible letter and an accessible bowl description.

After intentionally updating pilot records from their Docs, run
`python3 build-pilot-pdfs.py` from the repository root with ReportLab, pypdf, and
pdfplumber installed. This updates the three pilot PDFs in each format, then
reassembles each whole cookbook using the unchanged individual PDFs for the other
62 recipes. Contents links and recipe bookmarks are included.

Verify recipe substance, Doc stage headings, page checkmarks and mobile layout,
and rendered PDF pages before publishing. Automatic Docs-to-site synchronization
is a separate integration, not part of this formatting pilot.
