# Milestone 1: calculation foundation

## Delivered source

FastAPI backend, Vite frontend, profile setup, paired natal chart renderers, live sky data, Western transit geometry, future event search and birth time sensitivity sampling. Personal preview configuration is excluded from the repository.

## Verified locally

* Eight backend tests pass: time conversion, Lahiri offset, whole sign cusps, opposing lunar nodes, classical planet selection, aspect wrapping and motion, uncertainty endpoints, eclipse and lunation geometry, API persistence, validation and origin handling.
* Frontend production build passes.
* Both servers start successfully.
* A real HTTP request through the frontend proxy returns the saved profile, both calculated natal charts, 17 uncertainty samples across a four hour window, sky positions and events.
* HTTP documents for `/`, `/chart`, `/transits`, `/calendar`, `/chat` and `/profile` return successfully. `/chat` explicitly states that AI is not connected.
* Public source audit excludes personal birth configuration, generated output, dependencies and caches.

## Visual review limitation

Continuation verification on 1 October 2026 repeated all eight backend tests and the frontend production build successfully. A fresh pair of servers returned HTTP 200 through the frontend proxy with both chart systems and 17 uncertainty samples. The six documented page URLs returned HTML successfully; that is transport verification, not browser rendering acceptance. Use `python -m uvicorn` so the server uses the same Python environment as the installed dependencies.

The available browser rejected both the local preview address and the supported internal preview address with `net::ERR_BLOCKED_BY_CLIENT`. No screenshot or browser rendered acceptance result is claimed. The frontend compiles, but chart legibility, glyph rendering, mobile layout and controls still require browser review before this milestone can be fully accepted.

## Calculation limitations

* Whole sign houses and Lahiri are the initial conventions, pending traditional method review.
* Moshier calculations are explicitly selected. This does not represent an external ephemeris file installation.
* The current aspect engine is Western geometric aspects only. It is not a Vedic aspect interpretation engine.
* Cazimi uses the displayed 17 arcminute convention. Traditional rule review remains outstanding.
* Calendar scanning uses half day brackets and numerical refinement, not a guarantee of every possible rapid event. Solar conjunctions include Mercury through Saturn; combustion, visibility and longitude versus three dimensional proximity rules are not implemented.
* Events are prospective over 45 days from the selected date. Earlier dates can be explored through the transits date control. Calendar event to natal chart personalised interpretations remain unfinished.
* Eclipse maxima are global, not local visibility estimates.
* Birth time stability is sampled every 15 minutes, not continuously verified. Ascendants and houses remain provisional for estimated times.
* Dasha, knowledge retrieval, AI providers, friends, compatibility, unknown birth times, life areas, remedies, authentication and production hosting are not implemented.

## Stack decision

No original frontend or backend existed. The first foundation uses plain JavaScript with Vite and SVG rather than introducing Next.js and React before calculation and chart behaviour have been established. This is an explicit departure from the assumed framework in the original diagnosis brief. FastAPI and pyswisseph remain the calculation backend. The complete agreed scope is retained in `ACCEPTANCE.md`.

## Next review gate

Review both charts visually before expanding into the knowledge and AI stage. Inspect rising sign sensitivity and the disclosed calculation conventions. Do not mark the complete acceptance checklist done from this foundation.
