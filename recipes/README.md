# Recipe format

The public site reads `recipes.json`. PDF downloads are prebuilt files in
`pdf/kindle`, `pdf/paperwhite`, and `pdf/letter`. Google Docs are the editorial
source, but this repository currently has no automatic Docs sync or build job.
Publishing a repository update deploys the saved site snapshot through GitHub Pages.

All 67 recipes on the website use the approved preparation-group format.
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
