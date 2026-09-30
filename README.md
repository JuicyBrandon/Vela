# Vela

Two traditions. Your sky.

Vela is a local astrology app foundation with a FastAPI calculation service and a Vite browser interface. This first milestone connects real calculations to Western and Vedic chart renderers. It does not yet provide AI interpretations.

## Run locally

Requires Python 3.11 or later and Node 20.19 or later. On systems without a compatible pyswisseph wheel, install C and C++ compilers before installing the Python dependencies.

From the repository root:

```sh
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
cd backend
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

In a second terminal, from the repository root:

```sh
cd frontend
npm ci
npm run dev
```

Open http://localhost:3000 and enter your birth profile once. The frontend proxies requests to the local backend. No AI credentials are needed for this milestone.

## Included

* Western tropical SVG wheel, whole sign houses, exact longitude placement, major natal aspects, degrees, planetary motion and ascendant marker.
* South Indian fixed sign chart with Lahiri sidereal positions, the seven classical planets, mean Rahu and Ketu, Sanskrit names and provisional lagna.
* Current positions and speeds, Western transit aspects to natal planets within 3 degrees, approaching and separating indicators, and a current cazimi proximity check.
* Natal and current tropical positions on a shared wheel.
* Calendar search for global solar and lunar eclipses, new and full moons, stations, tropical and sidereal sign ingresses, and exact planetary solar conjunctions over 45 days.
* Local birth profile storage and birth time sensitivity samples at 15 minute intervals.
* Date exploration, refresh, loading and error states, responsive dark interface.

## Deliberately unfinished

Curated traditional knowledge, independently validated interpretations, AI chat, dasha periods, friends, compatibility, unknown birth time support, user accounts, durable hosted storage and production deployment. Their complete requirements remain in [the acceptance checklist](docs/ACCEPTANCE.md).

## Privacy and calculation conventions

Birth data lives in `backend/.local/profile.json`, excluded from git. The public source contains no personal birth profile. This is a single user local preview: bind the backend to localhost. It is not a production authentication system.

The engine uses Swiss Ephemeris through pyswisseph with the bundled Moshier calculation model. No ephemeris data files are bundled. The calculation response identifies the engine, model, node convention and house system. Time zone conversion uses Python IANA time zones. Whole sign houses are a documented starting convention, not a claim that all Western or Vedic schools use them.

Birth time sensitivity is sampled, not a continuous proof of stability. An approximate time is carried into the UI. Current sidereal transit houses are counted from the provisional natal lagna. Western geometric aspects are not presented as Vedic graha drishti. Eclipse times are global maxima and do not imply visibility at the birth location. The cazimi check uses a configurable implementation convention of 17 arcminutes in longitude; traditional rule validation remains pending.

Reference: [Swiss Ephemeris programmer documentation](https://www.astro.com/swisseph/swephprg.htm). Chart layout reference: [Himalayan Academy, Jyotiṣa](https://www.himalayanacademy.com/planets/). The conventional South Indian grid places Pisces at the upper left and Aries immediately to its right; the earlier draft's Aries corner description is corrected here.

## Verification

```sh
cd backend
python -m unittest discover -s tests -v
```

```sh
cd frontend
npm ci
npm run build
```

See [milestone validation](docs/MILESTONE_1.md) for actual checked outcomes and limitations.

## Commercial release

No project licence has been assigned on the owner's behalf. Swiss Ephemeris is separately licensed. Before distributing a combined application or operating a public service, choose the applicable Swiss Ephemeris licence and meet its terms. The dependency is not vendored into this repository. See [Astrodienst's licensing terms](https://www.astro.com/swisseph/swephprg.htm) and [release decisions](docs/RELEASE_DECISIONS.md).
