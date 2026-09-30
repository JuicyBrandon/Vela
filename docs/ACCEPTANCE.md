# Vela acceptance checklist

This is the agreed product scope. A feature is complete only when demonstrated with real data. Milestone 1 is the calculation foundation, not the entire app.

## Natal charts and live sky

- [ ] Own profile loads automatically after a single setup, with Western tropical and Vedic Lahiri sidereal charts.
- [ ] Western SVG has 12 signs, 12 houses, accurate planetary longitude placement, glyphs, degree labels, ascendant and coloured major aspects.
- [ ] Authentic South Indian fixed sign chart includes the classical planets, Rahu and Ketu, Vedic and Sanskrit names, degrees, motion and lagna.
- [ ] Dashboard shows current positions, retrogrades, stations, cazimi, sign ingresses, major aspects, lunations and solar and lunar eclipses.
- [ ] Events relate to the selected natal chart, including approaching, exact and separating contacts.
- [ ] Current transit planets can be overlaid on the natal Western wheel.
- [ ] Sidereal transits are counted against natal houses, with tradition appropriate interpretation.
- [ ] Calendar supports future exploration and past reflection, with explicit time zone and visibility distinctions.
- [ ] Refresh recalculates the current moment and labels its calculation timestamp.
- [ ] Vedic dasha periods are calculated, shown and supplied to AI context, with method and uncertainty identified.

## Traditional knowledge

- [ ] Separate Western and Vedic skills retrieve relevant material from curated sources.
- [ ] Each source has an identifiable text, author or translator, edition, locator, tradition, permitted use and verification status.
- [ ] Texts and teachings, calculated geometry and AI inference stay separate.
- [ ] Readings stand independently within each tradition before synthesis.
- [ ] Synthesis explains agreement and disagreement without forced reconciliation.
- [ ] School and method are disclosed with plain language explanations.
- [ ] Asking for the basis of a statement returns actual placements, method and source.
- [ ] Missing evidence produces explicit uncertainty, not invented teaching or certainty.
- [ ] Practising astrologers from both traditions review sample readings before claims of fidelity.

## AI conversation

- [ ] Natural conversation references the selected profile and the user's actual question.
- [ ] Each call receives both natal charts, current positions, active aspects and events, dasha context and birth time uncertainty.
- [ ] Chart calculations come from the engine, never model generated coordinates.
- [ ] Streaming, session history, typing state and useful failure handling are demonstrated.
- [ ] Optional memory can be inspected, edited and deleted.
- [ ] Generic advice is not presented as traditional teaching. Interpretations remain possibilities.

## Friends and compatibility

- [ ] Separate profiles offer the same interpretation depth and display the selected names.
- [ ] Any pair can be compared for romance, friendship or work.
- [ ] Comparisons explain possible strengths, tensions and communication patterns through both traditions.
- [ ] No single score or definitive relationship verdict replaces the explanation.
- [ ] Unknown and approximate times work with explicit limitations in calculations, chat and compatibility.
- [ ] Consent, separate histories, privacy and deletion controls work.

## Experience

- [ ] Dark luxury palette with gold and teal, readable typography, responsive charts and accessible controls.
- [ ] Navigation: dashboard, charts, transits, chat, life areas and remedies. Calendar and profiles are also required.
- [ ] Dashboard includes today's sourced summary, current dasha, significant transit and feature links.
- [ ] Consistent loading, empty and error states. No raw JSON shown to users.
- [ ] Final visual and functional review demonstrates all features rather than claiming completion from source inspection.

## Birth uncertainty

Use a provisional time and the user's estimated window. Source data belongs in private configuration, not the public repository. Compare placements and rising signs across the window, document sample spacing, and qualify every dependent reading. Do not describe sampled stability as guaranteed stability.

## Stage gates

1. Demonstrate local startup, saved profile, calculated charts, sky and calendar. Stop for review.
2. Connect reviewed knowledge, dasha calculations and grounded AI. Demonstrate traceable evidence. Stop for review.
3. Add friends, compatibility, unknown time support and memory controls. Stop for review.
4. Complete life areas, remedies and final visual polish, then perform functional review.

Original constraints on an existing database and existing requirements cannot apply to absent files. The new foundation introduces its initial dependency manifest and private file storage; it does not invent an existing schema, authentication service or Anthropic integration.
