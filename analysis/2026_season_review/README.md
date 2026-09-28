# Goal Square 2026 season review

The short version: Goal Square v5.2 did not beat its own input. The Squiggle weighted consensus it starts from tipped 138 of 190 games. Goal Square's final tips got 137. Goal Square's margin error was also worse (MAE 25.07 vs 24.92). The rule layer added noise. The one exception is the form rule (Rule 49), which has real signal, but its adjustments are about twice as big as they should be.

On clearances: across 2,643 AFL games from 2012 to 2024, the team that wins the clearance count wins only 62% of the time. A team's clearance form going into a game tells you almost nothing about the result once you already know its recent margins. Inside 50s and scoring shots matter far more.

---

## 1. How Goal Square went in 2026

Source: `prediction_history.json` (211 unique scored games) plus the last pre-game snapshot of every `predictions.json` commit (496 snapshots in git history).

| Split | Games | Tip % | MAE |
|---|---|---|---|
| All scored games | 211 | 74.4% | 24.3 |
| Tier 1 "Lock" | 92 | 88.0% | 24.7 |
| Tier 2 "Strong" | 62 | **64.5%** | 27.7 |
| Tier 3 "Lean" | 45 | **64.4%** | 19.2 |
| Tier 4 | 12 | 58.3% | 22.8 |
| Rounds 0–6 | 47 | 87.2% | 21.2 |
| Rounds 7–15 | 74 | 67.6% | 26.6 |
| Rounds 16–24 | 79 | 73.4% | 24.7 |
| Finals (incl. wildcard) | 11 | 72.7% | 19.5 |
| Tipped the home team | 120 | 79.2% | 23.1 |
| Tipped the away team | 91 | 68.1% | 25.9 |

What this shows:
- **Tiers 2 and 3 are the same thing.** "Strong" and "Lean" both hit 64%. The tier label tells users nothing below Tier 1.
- **The win probabilities are overconfident.** In games where we said 70–80%, we were right 59% of the time. At 80–90%, we were right 68%. Only the 90%+ bucket held up (96% stated, 92% hit).
- **The model under-predicts margins.** The average predicted margin was 24.5 points and the average actual margin was 32.0. This matters for MAE, but scaling margins up did not help (see below), so the bigger misses are mostly unpredictable blowouts, not a fixable bias.

## 2. Did our rules add anything on top of Squiggle?

For each game (190 games, rounds 2–29, excluding the round-1 regeneration described in §5), I read the "Squiggle base / weighted consensus" number from `key_factors` and compared it with Goal Square's final number.

| Predictor | Tips | MAE |
|---|---|---|
| Squiggle consensus (our input) | **138/190 (72.6%)** | **24.92** |
| Goal Square final | 137/190 (72.1%) | 25.07 |
| Consensus + 50% of our total adjustment | 138/190 | 24.65 |
| Consensus + 50% of Rule 49 (form) only | 140/190 (73.7%) | 24.53 |
| Consensus + 100% of Rule 49 only | 142/190 (74.7%) | 24.83 |

- Our adjustments pointed the right way 97 times out of 176 (55%). That is close to a coin flip.
- The correlation between our adjustment and what the consensus got wrong is 0.08, which is effectively zero.
- There were 23 games where we tipped against the consensus. We got 11 right and 12 wrong. The finals flips went 3–0 and made the season look better than it was.
- The MAE gap between Goal Square and the consensus was +0.15 points, with a 95% bootstrap interval of −1.1 to +1.4. There is no evidence the rules help.
- **Rule 49 (form trajectory)** was the only rule with a usable signal. It pointed the right way 60% of the time (54 of 90). Its average push was 13.5 points, but results only moved about 6 points in that direction. **Rule 50 (power gap)** pointed the right way 55% of the time, with an average push of 5.6 points and about 3.7 points of real movement.
- Caveat: these weights are fitted on the same 190 games they are scored on. A gain of 2–4 tips is within noise, so treat the weights as a direction, not a result.

## 3. Which match stats go with winning (2012–2024, 2,643 games)

Source: player-level stats summed to team totals per game, from [akareen/AFL-Data-Analysis](https://github.com/akareen/AFL-Data-Analysis). That dataset stops early in 2025, so it has no 2026 data. Squiggle, AFL Tables and Footywire were blocked by this environment's network policy.

**In-game: if you win this stat, how often do you win the game?**

| Stat | Win % when you win it | Correlation with winning |
|---|---|---|
| Scoring shots | 88.1% | 0.72 |
| Kicks | 78.1% | 0.61 |
| Marks inside 50 | 77.7% | 0.58 |
| Inside 50s | 72.7% | 0.53 |
| Disposals | 71.8% | 0.52 |
| Contested possessions | 70.4% | 0.47 |
| Uncontested possessions | 68.4% | 0.44 |
| **Clearances** | **62.4%** | **0.28** |
| Tackles | 55.6% | 0.16 |
| Free kicks | 54.4% | 0.10 |
| Hit-outs | 51.6% | 0.04 |
| Rebound 50s | 40.2% | −0.20 (a sign you were under siege) |
| Clangers | 38.1% | −0.28 |

**Clearances only matter when the team then uses the ball well:**

| Situation | Games | Win % |
|---|---|---|
| Won clearances, lost inside 50s | 879 | **35.6%** |
| Lost clearances, won inside 50s | 879 | **64.4%** |
| Won both | 1,584 | 77.3% |
| Won clearances, lost contested possessions | 769 | 37.3% |
| Clearance differential +10 or more | 811 | 71.6% |
| Clearance differential −10 or worse | 681 | 28.3% |

**The question that matters for a tipping model: does a team's stat form going into a game predict the result?**

This uses the average over each team's last 6 games (team minus opponent). The "beyond margin form" column shows what the stat adds once you already know recent margins.

| Pre-game form stat | Correlation with next margin | Adds beyond margin form | Tip % on its own |
|---|---|---|---|
| Scoring shots differential | 0.450 | +0.034 | 63.3% |
| Margin | 0.441 | — | 63.7% |
| Inside 50 differential | 0.401 | **+0.061** | 63.6% |
| Marks inside 50 | 0.389 | +0.033 | 61.9% |
| Contested possessions | 0.290 | +0.029 | 58.5% |
| **Clearances** | 0.148 | **+0.007** | 54.0% |
| Goal accuracy | 0.095 | **−0.097** | 53.3% |
| Tackles | 0.047 | −0.015 | 53.0% |
| Hit-outs | 0.037 | −0.001 | 49.9% |
| Rebound 50s | −0.278 | −0.091 | 40.0% |

Out-of-sample test (trained on 2013–2020, tested on 2021–2024):
- Margin form alone: MAE 28.14.
- Margin form plus inside 50s: MAE 27.91.
- Margin form plus clearances: MAE 28.16, slightly worse than margin alone.

**Accuracy is luck.** Teams that have been kicking straight get overrated by their recent margins, and teams that have been kicking poorly get underrated. This is why scoring-shot form beats margin form.

## 4. What to change for 2027 (in priority order)

1. **Remove the rule stack, or bring it back only through a backtest.** Default to the Squiggle consensus. Allow a rule to move the number only if it improves MAE when tested on games it wasn't fitted to (for example, fit on rounds 1–12 and test on rounds 13–24). Right now 60+ rules are costing tips.
2. **Keep Rule 49 (form) at about half its current strength.** Build it on scoring shots and inside 50s rather than raw margins, because shot-based form strips out the luck of goal accuracy.
3. **Don't build rules around clearances, tackles, hit-outs or free kicks.** They add close to nothing once form is known.
4. **Fix the tiers and the probabilities.** Tie each tier to the consensus margin (for example, Lock is 30+ points), not to a rule budget. Recalibrate the win probabilities so each stated 75% is right about 75% of the time. A logistic fit on consensus margin will do this.
5. **Publish a benchmark line.** Show "Goal Square vs Squiggle consensus" on the site every round. If we can't beat our input, users should know, and so should we.

## 5. Pipeline bugs found along the way

- **Round 1 got re-predicted after the Grand Final.** On 2026-09-26 the pipeline rolled back to "round 1" and regenerated predictions using end-of-season form ("RECENT COLLAPSE", "BLEEDING"). `live_scores.json` now shows "Round 1: 88.9%" from predictions made with hindsight. This should be frozen or removed before anyone quotes it.
- **The two files use different game ids for the same fixture.** For example, Carlton v Richmond is 38499 in `predictions.json` and 38506 in `prediction_history.json`. The history also has 7 duplicated ids (38522–38528).
- **GWS appears under two names**, "Greater Western Sydney" and "GWS Giants", so per-team statistics are split.
- **8 predictions changed after kickoff** (rounds 4, 5 and 7). None of them flipped the tip, but several moved toward the final result, and the scored record uses the post-kickoff number. One `key_factors` entry says "GAME COMPLETED — Result known". The prediction should be locked at the bounce.
- **The model code isn't in either repo.** `goal-square-v5-2/goal_square_v5_2.py` only contains hardcoded Round 4 data. The code that actually generates the rules is somewhere else, so none of the fixes above can be made from these repos.

## Reproducing

The scripts in `scripts/` point at a scratch directory. Running them takes these steps:
1. Clone `akareen/AFL-Data-Analysis` as `afl/`.
2. Run `build.py` to create the team-game table.
3. Run `an1.py` for the in-game stats and `an2.py` for the pre-game form tests.
4. Run `base.py` to parse the consensus baseline from `predictions.json` snapshots taken from git history (`git log -- predictions.json`).
