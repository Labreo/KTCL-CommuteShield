# KTCL CommuteShield: Three-Minute Video Demo Script
*Optimized for ElevenLabs Text-to-Speech (TTS) & Video Walkthrough Production*
*Hacktoberfest Weekend Challenge: Build for a Friend*

- **Target Completion**: **2:52** (172 seconds)
- **Hard Ceiling**: **3:00** (180 seconds)
- **Recorded Pacing**: ~2.1 words per second (~126 words per minute)
- **Total Word Budget**: **362 words**
- **Pronunciation Guide**:
  - `KTCL` → `K-T-C-L`
  - `TabPFN` → `Tab-P-F-N`
  - `SerpApi` → `Serp-A-P-I`
  - `IST` → `I-S-T`
  - `NH66` → `N-H sixty-six`
  - `₹` → `rupees`
  - `P_stranded` → `stranded probability`

---

## Full ElevenLabs Voiceover (Single-Take Audio Track)

*Copy and paste the exact text block below directly into ElevenLabs:*

```text
In Goa, thousands of college students rely on K-T-C-L smart cards for daily bus transit.

Bus depot servers update card balances on a nightly batch schedule.

The central server closes batch processing at eleven fifty-nine P-M I-S-T.

Recharges made after midnight fail to reach depot turnstiles until the following evening.

My friend Kanak studies at Farmagudi campus and plays evening football matches at Wadi turf.

An unplanned match exhausts his bus balance.

Next morning at seven-thirty A-M, his card gets declined at the Margao turnstile, stranding him before morning exams.

I built K-T-C-L CommuteShield to solve this dilemma for Kanak.

CommuteShield runs locally on his laptop every evening at eight P-M I-S-T.

It queries the live K-T-C-L portal, checks his timetable, and pulls highway conditions through Serp-A-P-I.

Then it passes these features into Prior Labs Tab-P-F-N.

Tab-P-F-N is a tabular foundation model that performs in-context Bayesian inference in a single forward pass.

It excels on small personal transit tables where standard models overfit.

Let us test a live scenario.

Kanak has eighteen rupees remaining on Friday evening, with a scheduled football match at Wadi turf tomorrow.

A simple rule might ignore this balance.

Tab-P-F-N evaluates his seven-factor transit history and calculates a stranded probability of eighty-two percent.

The engine projects a sixty-four rupee shortfall.

Instantly, CommuteShield delivers an emergency alert to Kanak's phone on Telegram.

The alert explains the Wadi turf detour and prompts him to recharge one hundred rupees before the midnight cutoff.

Next, watch how CommuteShield defeats notification fatigue on light days.

On Tuesday, Kanak has twenty-five rupees and only one morning lecture.

A naive alert would spam his phone.

Tab-P-F-N recognizes twenty-five rupees covers the single seventeen rupee fare, keeping his notifications clear.

Serp-A-P-I grounds the agent with live road advisories.

When monsoon flooding prompts diversions along N-H sixty-six, the agent applies an elevated fare multiplier.

Personal travel logs contain sensitive daily movements.

Running Tab-P-F-N locally protects Kanak's privacy, requires zero cloud subscriptions, and prevents stranded mornings.

Thank you for reviewing K-T-C-L CommuteShield.
```

---

## Scene-by-Scene Visual Choreography & Calibrated Timestamps

---

### [0:00 - 0:31] SCENE 1: The Commuter Dilemma (The Narrative Hook)

**On-Screen Action**:
- Open with a clean split view: a photo of the Goa KTCL Kadamba student smart card alongside an authentic WhatsApp chat showing the 7:30 AM turnstile decline message.
- Transition smoothly to the KTCL Cashless web portal showing the warning banner: *Depot server sync cutoff at 11:59 PM IST*.
- Highlight Margao bus terminal and Farmagudi campus route on a stylized map.

**Voiceover Audio** (59 words, ~28 seconds):
> "In Goa, thousands of college students rely on K-T-C-L smart cards for daily bus transit.
> 
> Bus depot servers update card balances on a nightly batch schedule.
> 
> The central server closes batch processing at eleven fifty-nine P-M I-S-T.
> 
> Recharges made after midnight fail to reach depot turnstiles until the following evening."

---

### [0:31 - 1:00] SCENE 2: Kanak's Routine & Introducing KTCL CommuteShield

**On-Screen Action**:
- Pan to student calendar showing college lectures and Friday evening football matches at Wadi turf near Ponda.
- Launch terminal window displaying the rich ASCII banner of KTCL CommuteShield.
- Show the local project repository structure (`commuteshield/` modules, local `.env`, and `friend_commute_history.csv`).

**Voiceover Audio** (59 words, ~28 seconds):
> "My friend Kanak studies at Farmagudi campus and plays evening football matches at Wadi turf.
> 
> An unplanned match exhausts his bus balance.
> 
> Next morning at seven-thirty A-M, his card gets declined at the Margao turnstile, stranding him before morning exams.
> 
> I built K-T-C-L CommuteShield to solve this dilemma for Kanak."

---

### [1:00 - 1:36] SCENE 3: Demo 1 — Evening Assessment & TabPFN Bayesian Inference

**On-Screen Action**:
- In the terminal, execute:
  ```bash
  python cli.py run --balance 18.0 --turf 1
  ```
- Terminal logs show:
  1. KTCL balance fetched: ₹18.00.
  2. Scheduled trips: 3 (lectures + Wadi turf).
  3. Model loading: `tabpfn-v3.5-20260909.safetensors` active.
- Red alert panel appears:
  - `Stranded Probability: CRITICAL RISK: 82.7%`
  - `Projected Shortfall: ₹64.50`
  - `Recommended Top-Up: ₹100`

**Voiceover Audio** (77 words, ~36 seconds):
> "CommuteShield runs locally on his laptop every evening at eight P-M I-S-T.
> 
> It queries the live K-T-C-L portal, checks his timetable, and pulls highway conditions through Serp-A-P-I.
> 
> Then it passes these features into Prior Labs Tab-P-F-N.
> 
> Tab-P-F-N is a tabular foundation model that performs in-context Bayesian inference in a single forward pass.
> 
> It excels on small personal transit tables where standard models overfit."

---

### [1:36 - 2:06] SCENE 4: Demo 2 — Live Telegram Alert & Anti-Fatigue Filtering

**On-Screen Action**:
- Cut to phone screen capture showing real-time Telegram notification from `@ktcl_commuteshield_bot`.
- Cursor zooms in on message text:
  - *Card Balance: ₹18.00*
  - *Risk: 82.7%*
  - *Action Required: Top up at least ₹100 online before midnight*.
- Back in terminal, run safe day evaluation:
  ```bash
  python cli.py run --balance 25.0 --turf 0 --trips 1
  ```
- Show green panel: `SAFE: 23.5%` with zero Telegram spam.

**Voiceover Audio** (69 words, ~30 seconds):
> "Let us test a live scenario.
> 
> Kanak has eighteen rupees remaining on Friday evening, with a scheduled football match at Wadi turf tomorrow.
> 
> A simple rule might ignore this balance.
> 
> Tab-P-F-N evaluates his seven-factor transit history and calculates a stranded probability of eighty-two percent.
> 
> The engine projects a sixty-four rupee shortfall.
> 
> Instantly, CommuteShield delivers an emergency alert to Kanak's phone on Telegram.
> 
> The alert explains the Wadi turf detour and prompts him to recharge one hundred rupees before the midnight cutoff."

---

### [2:06 - 2:34] SCENE 5: Demo 3 — SerpApi Highway Grounding & Anti-Fatigue Proof

**On-Screen Action**:
- Open SerpApi inspection CLI:
  ```bash
  python cli.py transit
  ```
- Display organic Google Search results for Goa NH66 flood diversions and KTCL route advisories.
- Show dynamic disruption multiplier adjusting from 1.0x to 1.35x.
- Show `cli.py simulate` showing all 3 scenarios verified.

**Voiceover Audio** (59 words, ~27 seconds):
> "Next, watch how CommuteShield defeats notification fatigue on light days.
> 
> On Tuesday, Kanak has twenty-five rupees and only one morning lecture.
> 
> A naive alert would spam his phone.
> 
> Tab-P-F-N recognizes twenty-five rupees covers the single seventeen rupee fare, keeping his notifications clear.
> 
> Serp-A-P-I grounds the agent with live road advisories.
> 
> When monsoon flooding prompts diversions along N-H sixty-six, the agent applies an elevated fare multiplier."

---

### [2:34 - 2:52] SCENE 6: Local Edge Sovereignty & Closing Punchline

**On-Screen Action**:
- Show terminal running offline with network disconnected to prove local TabPFN weight execution.
- Display `pytest` passing all 14 tests in the terminal.
- Return to GitHub repository page (`Labreo/KTCL-CommuteShield`) with closing title card and DEV challenge submission badge.

**Voiceover Audio** (39 words, ~18 seconds):
> "Personal travel logs contain sensitive daily movements.
> 
> Running Tab-P-F-N locally protects Kanak's privacy, requires zero cloud subscriptions, and prevents stranded mornings.
> 
> Thank you for reviewing K-T-C-L CommuteShield."

---

## Audio Production & Video Assembly Checklist

1. **Audio Generation**: In ElevenLabs, select an articulate narrator voice (e.g. *Adam*, *Brian*, or *George*) with stability at `65%` and clarity at `75%`.
2. **Timing Confirmation**: The raw audio runs at `2:52`, leaving an `8-second` safety margin before the 3:00 cutoff.
3. **Screen Recording**: Record the terminal commands and Telegram screen captures at `1080p60` with font zoom set to 125% for mobile clarity.
4. **Volume Levels**: Keep background music (ambient synth or low lo-fi) at `-22 dB` beneath the voiceover at `-1 dB`.
