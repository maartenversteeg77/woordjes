# Woordjes

Oefenapp voor Pelle: woordjes in rondes van 10, met de lijsten Onbekend, Lastig, Verkeerd gespeld en Bekend. Daarnaast zinnen vertalen (Latijn, Grieks, Duits) en naamvallen (Grieks, meerkeuze).

- `public/index.html` is de site. Cloudflare zet hem online bij elke push naar `main`.
- `bron/` bevat de bouwstenen: `words.json` (Latijn, StudyGo), `zinnen.json` (Latijnse vertaalzinnen), `duits.json` (Na Klar! Kapitel 4, StudyGo), `grieks.json` (Grieks les 3: woorden, vertaalzinnen en naamvaloefeningen, overgenomen uit het werkboek), `match.js` (antwoordcontrole), `template.html` (opmaak) en `build.py`.
- Opnieuw bouwen: `python3 bron/build.py`.

Voortgang staat in de browser van wie oefent (localStorage), gekoppeld aan het adres van de site.

Automatisch online via Cloudflare Workers Builds (Worker: shiny-frost-815e).
