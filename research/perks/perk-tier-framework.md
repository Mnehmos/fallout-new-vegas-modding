# Perk Tier Framework — FNV Perk Overhaul

## What Makes a Perk Good in FNV?

FNV is a build-optimization game. Perks compete against each other for limited level-up slots (every 2 levels, ~15 perks total for a normal playthrough). A perk is only as good as its **opportunity cost**.

---

## Tier Definitions

### S Tier — Build-Defining
These perks are the reason you built the way you did. Taking them fundamentally changes how you play. Missing them feels like a genuine sacrifice.

Examples (vanilla): Jury Rigging, Grunt, Hand Loader, Chemist, Comprehension

### A Tier — Always Worth It
Strong perks with broad utility. You'd take these on almost any build that qualifies. Clear, reliable benefits.

Examples (vanilla): Finesse, Better Criticals, Sniper, Ninja, Nerves of Steel

### B Tier — Situationally Strong
Good perks on the right build. Weaker on a general build, but synergize well with specific playstyles.

Examples (vanilla): Commando, Gunslinger, Adamantium Skeleton

### C Tier — Filler
Marginal benefit. You'd take these only after exhausting better options. Often outclassed by their opportunity cost.

Examples (vanilla): Light Touch, Toughness (Rank 1), Here and Now

### D Tier — Trap Picks
Perks that feel good on paper but are mechanically weak, poorly scaled, or actively harmful to your build.

Examples (vanilla): Swift Learner, Retention, Explorer (wastes a slot)

---

## Evaluation Criteria

For each perk, score 1-5 on each axis:

| Criterion | Description |
|-----------|-------------|
| **Damage Impact** | Does it directly improve combat effectiveness? |
| **Utility Breadth** | Is it useful in many situations or just one? |
| **Build Synergy** | Does it enable or amplify other perk choices? |
| **Opportunity Cost** | Is the level/SPECIAL requirement fair for what it gives? |
| **Scaling** | Does it stay relevant from early to late game? |

**Total score → Tier:**
- 21-25: S
- 16-20: A
- 11-15: B
- 6-10: C
- 1-5: D

---

## Our Overhaul Goal

**All player-facing perks must be A or B tier.**

This means:
- D and C perks get **buffed** (increased effect, reduced requirements, or new secondary effects added)
- S perks may get **slight nerfs** if they're crowding out other choices
- Perks that are fundamentally unfixable get **merged** into other perks or **converted** to passive traits

---

## Buff Strategies by Category

### Underpowered % bonuses
Increase the percentage. Swift Learner's 10% XP → 25% XP still isn't exciting but at least it's noticeable.

### One-dimensional perks
Add a secondary effect. "Explorer" revealing all map markers is boring → also grant +5 Survival.

### Requirements too high
Reduce level requirement or SPECIAL minimums to match the perk's actual power.

### Gimmick perks (Here and Now)
Redesign entirely. "Here and Now" granting an instant level-up is a novelty, not a build choice. Replace with something meaningful.

---

## Perks to Analyze

See `research/perks/perk-database.md` for the full list with current stats and tier ratings.
