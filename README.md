# Woordjes

Oefenapp voor Pelle: woordjes in rondes van 10, met de lijsten Onbekend, Lastig, Verkeerd gespeld en Bekend.

- `public/index.html` is de site. Cloudflare zet hem online bij elke push naar `main`.
- `bron/` bevat de bouwstenen: `words.json` (woordenlijsten uit StudyGo), `match.js` (antwoordcontrole), `template.html` (opmaak) en `build.py`.
- Opnieuw bouwen: `python3 bron/build.py`.

Voortgang staat in de browser van wie oefent (localStorage), gekoppeld aan het adres van de site.
