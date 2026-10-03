---
title: "KTCL CommuteShield: Protecting College Friends from Getting Stranded with TabPFN & SerpApi"
published: true
tags: devchallenge, weekendchallenge, hf26challenge
cover_image: https://raw.githubusercontent.com/Labreo/KTCL-CommuteShield/main/assets/cover.png
---

*This is a submission for the [Hacktoberfest Weekend Challenge: Build for a Friend](https://dev.to/challenges/hacktoberfest-weekend-2026-10-01)*

## What I Built

I built **KTCL CommuteShield** for my friend Tejas, an engineering classmate who commutes daily across Goa between Margao and the Farmagudi campus. 

College commuters in Goa rely on the Kadamba Transport Corporation (KTCL) RFID smart card for bus travel. KTCL updates smart card balances across depot ticket machines on a nightly batch schedule. The server closes batch processing at **11:59 PM IST**. Any top-up made after midnight fails to reach depot turnstiles until the following evening.

Tejas often attends evening football matches at Wadi turf near Ponda after college lectures. These detours cost extra bus fare. When his card balance dips below thirty rupees, he risks card rejection at the 7:30 AM morning depot line. Simple alerts like "balance under fifty rupees" trigger notification fatigue on days with a single lecture. 

KTCL CommuteShield runs locally on Tejas's machine every evening at 8:00 PM IST. The agent checks his live card balance from the KTCL portal. It inspects tomorrow's class schedule and scheduled turf matches. It grounds travel costs with live highway road conditions using SerpApi. Finally, it passes these features into Prior Labs TabPFN to calculate the true stranded probability. When risk is elevated, it delivers a direct Telegram warning to Tejas before the midnight sync cutoff.

### What Tejas Said

> *"The 11:59 PM cutoff caught me out twice last semester during monsoon exams. CommuteShield pinged my Telegram at 8:15 PM on Friday warning me about the Wadi turf detour and gave me the exact recharge amount. That saved me from standing stranded at Margao depot at 7:30 AM."*

## Demo

- **Interactive CLI & Telemetry**: CommuteShield renders a terminal display showing card balance, highway status, and TabPFN stranded risk.
- **Direct Telegram Push**: High-risk forecasts dispatch actionable alerts to Tejas's phone via `@ktcl_commuteshield_bot`.
- **Live Terminal Simulation**:

```bash
# Run live evaluation for Tejas
python cli.py run


# Test critical risk alert with Wadi turf match detour
python cli.py run --balance 18.0 --turf 1

# Contrast real commuter scenarios against naive threshold rules
python cli.py simulate
```

## Code

The project source code is hosted on GitHub:
{% github Labreo/KTCL-CommuteShield %}

Repository: [https://github.com/Labreo/KTCL-CommuteShield](https://github.com/Labreo/KTCL-CommuteShield)

The agent runs completely on open software dependencies: Python 3.12, TabPFN, PyTorch, SerpApi, Requests, and Rich.

## How I Built It

CommuteShield links three open modules into an automated evening agent:

### 1. Prior Labs TabPFN Foundation Model
Commuter logs contain small table sizes where standard neural networks and tree models overfit. TabPFN processes Tejas's sixty-row travel table in a single forward pass using in-context Bayesian inference. The model evaluates seven inputs:
- Day of the week
- Current card balance
- Scheduled lecture trips
- Turf sports match indicator
- Days since previous recharge
- SerpApi highway disruption index
- Moving average daily fare burn

TabPFN calculates a calibrated stranded risk probability ($P_{\text{stranded}}$) without requiring iterative training or weight fine-tuning.

### 2. Live Transit Grounding via SerpApi
Goa bus schedules face monsoon flooding, fuel surcharges, and NH66 highway bridge repairs. The SerpApi tool executes automated Google Search queries for Kadamba routes between Margao, Panaji, and Farmagudi. The parser extracts regional notices and adjusts the travel cost multiplier from 1.0x to 1.35x when detours occur.

### 3. Headless Alert Dispatcher
The agent operates headlessly in the background. If TabPFN flags critical risk ($P_{\text{stranded}} \ge 0.60$ or an expected shortfall), the dispatcher transmits a Telegram alert to Tejas's chat ID. The notification lists the exact shortfall and recommends an optimal recharge sum before depot servers shut down at midnight.

## Why Does Open Innovation Matter?

Open-weight AI makes CommuteShield safe, trustworthy, and accessible for students:

1. **Student Location Sovereignty**: Transit logs record personal life patterns, including home locations, campus lecture timings, sports venues, and travel hours. Commercial cloud language models ingest prompts on external servers. Open-weight TabPFN executes locally on a laptop, keeping Tejas's travel logs private.

2. **Deterministic Arithmetic Grounding**: Generative text models struggle with tabular balance math. TabPFN delivers principled Bayesian probability distributions over structured tabular records.
3. **Zero Operating Cost**: The entire inference pipeline runs on a standard CPU. Students run CommuteShield for zero recurring cost.
4. **Resilient Local Execution**: When local internet drops, CommuteShield evaluates risk using cached weights (`tabpfn-v3.5-20260909.safetensors`) and stored regional travel ledgers.

## My Agent Session

We built and validated CommuteShield using our agent harness and DevRelay MCP tooling. 

{% agent_session Labreo/KTCL-CommuteShield %}

You can inspect the complete agent session logs, test verification traces, and git commits via DevRelay.

## Prize Categories

- **Best Use of TabPFN ($200 USD)**: CommuteShield uses the official Prior Labs TabPFN foundation model for in-context Bayesian tabular inference, forecasting student transit card exhaustion from small personal commute tables.
- **Best Use of SerpApi ($200 USD)**: SerpApi grounds TabPFN with real-time Goa road advisories, weather warnings, and KTCL Kadamba transit updates to adjust daily fare forecasts dynamically.
