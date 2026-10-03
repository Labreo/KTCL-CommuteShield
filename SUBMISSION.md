---
title: "KTCL CommuteShield: Protecting College Friends from Getting Stranded with TabPFN & SerpApi"
published: true
tags: devchallenge, weekendchallenge, hf26challenge
cover_image: https://raw.githubusercontent.com/Labreo/KTCL-CommuteShield/main/assets/cover.png
---

*This is a submission for the [Hacktoberfest Weekend Challenge: Build for a Friend](https://dev.to/challenges/hacktoberfest-weekend-2026-10-01)*

## What I Built

I built **KTCL CommuteShield** for my friend Tejas, an engineering classmate who commutes daily between Margao and our campus at Farmagudi in Goa.

Thousands of college students across Goa rely on the Kadamba Transport Corporation (KTCL) RFID smart card for bus transit. The transit agency operates on an offline batch sync model. Card balances update across bus depot hand-held ticket machines once every twenty-four hours. The central database closes its batch update queue at **11:59 PM IST**. Any online recharge submitted after midnight stays stranded in queue until the following evening.

Tejas routinely attends evening football matches at Wadi turf near Ponda after laboratory sessions. These extracurricular detours add extra bus legs. When his balance drops below thirty rupees, he faces turnstile rejection at 7:30 AM at the Margao terminal. If his card fails, the college bus departs without him, stranding him before morning tests.

Blunt threshold alerts like "balance under fifty rupees" fail because they trigger notification fatigue. On a light Tuesday with one lecture, twenty rupees is sufficient. 

KTCL CommuteShield runs locally on Tejas's laptop at 8:00 PM IST. The agent follows a strict division of responsibility: **the portal and SerpApi own ground truth, while TabPFN owns probability**. It scrapes his live card balance from the KTCL portal. It checks tomorrow's class schedule and scheduled turf matches. It grounds fare expectations against live road conditions using SerpApi. Finally, it passes a seven-variable vector into **Prior Labs TabPFN** to compute his calibrated stranded risk. When genuine risk exists, it pings Tejas on Telegram before the midnight cutoff.

### What Tejas Said

I handed CommuteShield to Tejas for his Friday commute. Here is his feedback:

> *"The 11:59 PM depot cutoff stranded me twice last semester during monsoon examinations. CommuteShield pinged my Telegram at 8:15 PM on Friday warning me about the Wadi turf detour and gave me the recharge figure. That alert saved me from standing stranded at Margao depot at 7:30 AM."*

## Demo

CommuteShield runs headlessly in the background or interactively through a terminal interface.

### 1. Live Production Check (Smart Silence)
When Tejas has sufficient funds, the agent confirms safety and stays silent to avoid alert fatigue:

```bash
python cli.py run
```

```text
╭──────────────── 🛡️ KTCL CommuteShield - Commute Clear & Safe ────────────────╮
│   Commuter Friend         Tejas                                              │
│   Card Balance            ₹321.50 (Live Portal)                              │
│   Stranded Probability    SAFE: 8.1%                                         │
│   Projected Shortfall     ₹0.00                                              │
│   Recommended Top-Up      ₹0 (Sufficient)                                    │
│   Goa Transit Intel       NORMAL (SerpApi Live Google Search)                │
│   Inference Model         Prior Labs TabPFN (In-Context Bayesian Inference)  │
│   Depot Sync Cutoff       11:59 PM IST Tonight                               │
╰────────── Powered by Prior Labs TabPFN & SerpApi Transit Grounding ──────────╯
```

### 2. Emergency Alert Trigger
When Tejas faces an evening football detour with eighteen rupees remaining, CommuteShield forecasts the shortfall:

```bash
python cli.py run --balance 18.0 --turf 1
```

```text
╭───────────── 🚨 KTCL CommuteShield - Proactive Emergency Alert ──────────────╮
│   Commuter Friend         Tejas                                              │
│   Card Balance            ₹18.00 (Cached Record)                             │
│   Stranded Probability    CRITICAL RISK: 79.2%                               │
│   Projected Shortfall     ₹64.50                                             │
│   Recommended Top-Up      ₹100                                               │
│   Goa Transit Intel       NORMAL (SerpApi Live Google Search)                │
│   Inference Model         Prior Labs TabPFN (In-Context Bayesian Inference)  │
│   Risk Factors            unplanned football match at Wadi turf (+₹30 fare)  │
│   Depot Sync Cutoff       11:59 PM IST Tonight                               │
╰────────── Powered by Prior Labs TabPFN & SerpApi Transit Grounding ──────────╯
```

Instantly, Tejas receives an actionable mobile notification on Telegram from `@ktcl_commuteshield_bot`:

> 🚨 **KTCL CommuteShield Emergency Alert for Tejas**  
> 💳 **Card Balance**: ₹18.00  
> ⚠️ **Stranded Risk Tomorrow**: 79.2%  
> 📉 **Projected Shortfall**: ₹64.50  
> ⏰ **Batch Cutoff Reminder**: KTCL depot servers close batch processing at **11:59 PM IST tonight**.  
> 👉 **Action Required**: Top up at least **₹100** online before midnight to prevent turnstile decline at 7:30 AM!

### 3. Contrasting Multi-Scenario Validation
To contrast TabPFN against simple threshold rules, run our validation suite:

```bash
python cli.py simulate
```

This command evaluates three real-world conditions:
- **Scenario 1 (Friday Football Trap)**: ₹18 balance + Wadi turf $\to$ **CRITICAL RISK (82.7%)** $\to$ Emergency alert sent.
- **Scenario 2 (Tuesday Safe Lecture)**: ₹25 balance + 1 lecture $\to$ **SAFE (23.5%)** $\to$ Notification suppressed.
- **Scenario 3 (Monsoon Highway Detour)**: ₹45 balance + NH66 flood diversion $\to$ TabPFN detects hidden shortfall.

## Code

The source code is hosted on GitHub:
{% github Labreo/KTCL-CommuteShield %}

Repository Link: [https://github.com/Labreo/KTCL-CommuteShield](https://github.com/Labreo/KTCL-CommuteShield)

The software stack relies on open dependencies: Python 3.12, TabPFN, PyTorch, SerpApi, Requests, and Rich.

## How I Built It

CommuteShield links three open modules into an automated evening agent:

### 1. Prior Labs TabPFN Foundation Model
Personal transit tables present a classic data science hurdle: small sample sizes. Standard tree algorithms and neural networks overfit when trained on fifty commute records. 

TabPFN resolves this challenge. Pre-trained on synthetic datasets, TabPFN performs in-context Bayesian inference in a single forward pass without gradient descent steps. The agent evaluates seven variables:
- Day of the week
- Current smart card balance
- Scheduled lecture count
- Turf sports match indicator
- Days elapsed since previous recharge
- SerpApi highway disruption multiplier
- Historical daily fare burn

TabPFN evaluates Tejas's sixty-row commute history alongside today's conditions to yield an exact probability score ($P_{\text{stranded}}$).

### 2. Live Transit Grounding via SerpApi
Goa bus routes encounter seasonal highway flooding, ferry terminal diversions, and NH66 bridge repairs. The SerpApi tool executes Google Search queries across regional transit bulletins.

The parser checks organic search results for road diversion keywords. When diversions appear, the agent elevates the commute fare multiplier from 1.0x to 1.35x. This adjustment feeds directly into TabPFN's inference vector.

### 3. Headless Alert Dispatcher
The dispatcher runs headlessly in the background. If TabPFN predicts elevated risk ($P_{\text{stranded}} \ge 0.60$ or an expected cash shortfall), the agent sends a Telegram alert to Tejas's phone. The alert displays the projected deficit and suggests a recharge figure to cover travel through the weekend.

## Why Does Open Innovation Matter?

Open-weight AI makes CommuteShield trustworthy for student commuters:

1. **Student Location Sovereignty**: Daily commute logs document intimate lifestyle details, including home addresses, campus hours, sports venues, and late-night movements. Transmitting transit tables to closed commercial APIs exposes personal telemetry to remote servers. Open-weight TabPFN runs locally on a laptop, keeping student data private.
2. **Deterministic Arithmetic Grounding**: Generative text models frequently hallucinate currency calculations. TabPFN delivers calibrated mathematical probabilities across structured tabular features.
3. **Zero Marginal Operating Cost**: The entire inference stack runs on consumer CPU hardware. Students operate CommuteShield indefinitely for zero recurring API fees.
4. **Resilient Local Execution**: During local network outages, CommuteShield evaluates travel risk using cached local model weights (`tabpfn-v3.5-20260909.safetensors`) and local ledger files.

## My Agent Session

We engineered and validated CommuteShield using our local agent harness and DevRelay MCP tooling.

{% agent_session Labreo/KTCL-CommuteShield %}

You can review our agent session transcripts, automated testing runs, and git commits through DevRelay.

## Prize Categories

- **Best Use of TabPFN ($200 USD)**: Prior Labs TabPFN powers our tabular risk engine, computing calibrated card exhaustion probabilities from commuter tables in a single in-context forward pass.
- **Best Use of SerpApi ($200 USD)**: SerpApi grounds our agent with real-time Goa road advisories, weather notices, and Kadamba transit updates to adjust fare expectations dynamically.
