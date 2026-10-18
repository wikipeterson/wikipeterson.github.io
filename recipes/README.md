# Recipe format

The public site reads `recipes.json`. PDF downloads are prebuilt files in
`pdf/kindle`, `pdf/paperwhite`, and `pdf/letter`. Google Docs are the editorial
source, but this repository currently has no automatic Docs sync or build job.
Publishing a repository update deploys the saved site snapshot through GitHub Pages.

All 136 recipes on the website use the approved preparation-group format.
The wider Recipe Index may include additional recipes that are not yet on this website.

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

Recipe records use `prepGroups` (letter to readable bowl description) and
`ingredients[].prepGroup`. The UI retains the existing checkbox storage keys and
adds both a visible letter and an accessible bowl description.

After intentionally updating recipe records from their Docs, run
`python3 build-pilot-pdfs.py` from the repository root with ReportLab, pypdf, and
pdfplumber installed. This updates every recipe PDF in each format and reassembles each whole cookbook. Contents links and recipe bookmarks are included.

Verify recipe substance, Doc stage headings, page checkmarks and mobile layout,
and rendered PDF pages before publishing. Automatic Docs-to-site synchronization
is a separate integration, not part of this formatting work.

Temperature-guide entries use `informational: true`; they render as reference text, not ingredient checkboxes. Recipes with no shared prep bowl use an empty `prepGroups` object and charcoal checkboxes.

## Categories

Every recipe has one primary category, chosen by its main use at the table,
not by protein or equipment. The sidebar order follows a meal: Breakfast,
Appetizers & snacks, Main dishes, Soups, Salads, Side dishes, Breads,
Sauces & dips, Desserts, Drinks. Cooking method remains a separate filter.

Use Main dishes for meal-sized sandwiches, wraps, pasta, pizza, casseroles,
and meat or fish plates. Use Salads for chicken salads as well as pasta and
green salads. Rice and vegetable accompaniments go in Side dishes.
Corn bread and garlic knots go in Breads; jerky is a snack. Bacon belongs
in Breakfast. Gorgonzola Cream Sauce for Filet stays in Main dishes because
the recipe includes cooking two steaks, not just making a standalone sauce.

## Linked recipe import — October 18, 2026

Added 69 recipe pages from 67 previously omitted linked files. The hummus file contains three distinct recipes; the two breakfast-sausage-casserole files are duplicates. Ten linked files remain on the local exception list (nine incomplete recipe/reference notes and one permission-denied Doc). Menu/planning documents and entries without linked files are excluded. Original Docs and Word files remain preserved; site entries link to their source files. Conflicting amounts and missing preparation details are flagged in recipe notes.

## Recipe card photos

The collection is a plain searchable directory with green photo cards. The Sicilian Pizza feature and promotional headings have been removed. All 136 cards have representative food photos stored in `images/`; `photos.json` maps recipe IDs to assets and source/license metadata. These are illustrative food photos, not photos of the exact saved recipes. Full author, source, and license credits are in `photo-credits.html`, linked from the collection footer. Photos load lazily; recipes and PDF contents are unchanged.
