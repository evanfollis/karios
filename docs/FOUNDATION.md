### KAIROS PROJECT—FOUNDATIONAL SYSTEM PROMPTS

*(Single source-of-truth for all human and AI contributors)*

---

## 1  Project Charter

| Item                            | Definition                                                                                                                                                                                                                                                                    |
| ------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Purpose**                     | Build a live, modular trading platform that (a) compounds the user’s own capital with disciplined, auditable processes and (b) demonstrates full-stack investment and risk-management competence required for a Portfolio Manager (PM) role.                                  |
| **Asset Scope (v0-v1)**         | Crypto spot pairs (BTC-USDT, ETH-USDT) only—chosen for 24/7 market access, zero employer trading restrictions, and low entry capital.  Design all modules to be asset-agnostic so that listed equities, REITs, and fixed-income ETFs can be onboarded later without refactor. |
| **Edge Hypothesis**             | Process edge, not signal novelty: rapid research-to-deployment loop, live-calibrated risk, and continuous validation will outpace static academic factors.                                                                                                                    |
| **Success Metrics**             | 1. Platform reliability ≥ 99 % uptime in live trading loop.  2. One-year live Information Ratio > 0 after costs and slippage.  3. Public (or internally verifiable) track record, code, and post-mortems sufficient to satisfy typical allocator due diligence.               |
| **Out-of-Scope (initial 6 mo)** | Options, leverage, HFT latencies, cross-exchange latency arbitrage, ML alpha discovery at scale.                                                                                                                                                                              |

---

## 2  Core Operating Principles

1. **Reality First** – Every idea must touch the market quickly; paper results without live confirmation carry no weight.
2. **Single Layer of Abstraction** – Add interfaces only when a second concrete implementation exists.
3. **Deterministic Logging** – All market data, decisions, and orders must be reproducible from raw logs.
4. **Risk Is a Feature** – Position sizing, circuit breakers, and kill-switch logic are treated as first-class software.
5. **Transparent Learning Loop** – Each release includes a concise devlog: hypothesis → experiment → outcome → adjustment.
6. **Compliance Ready** – Maintain clean audit trails and separation of personal vs. employer resources to support FINRA, MNPI, and outside-business-activity disclosures.
7. **Career Leverage** – Prioritise deliverables that demonstrate PM-level capabilities: portfolio construction, risk budgeting, and post-trade attribution.

---

## 3  Technical Architecture (v0.1)

```
kairos/
└── src/
    ├── data/          # market data adapters (REST/WebSocket)
    ├── research/      # backtest + walk-forward engine
    ├── signals/       # deterministic signal functions
    ├── risk/          # position limits, stop logic, portfolio budget
    ├── execution/     # exchange wrappers, order state machines
    ├── audit/         # immutable trade & decision logs
    └── reporting/     # CLI + optional Streamlit dashboard
```

**Run Loop (pseudo)**

```
while True:
    tick = data.get_latest()
    sig  = signals.calc(tick, history)
    risk_state = risk.evaluate(sig, positions)
    orders = execution.sync(risk_state)
    audit.log(tick, sig, risk_state, orders)
    reporting.update(audit.tail())
    sleep(cfg.interval)
```

---

## 4  Agent Operating Manual

| Agent              | Mandate                                      | Required Inputs                            | Outputs                                  | Critical Tests                                        |
| ------------------ | -------------------------------------------- | ------------------------------------------ | ---------------------------------------- | ----------------------------------------------------- |
| **DataAgent**      | Maintain continuous, gap-free price feed.    | Exchange REST/WSS creds, symbol list.      | Normalised ticks to `data/`.             | 1-sec max data lag, explicit null-fill on gap.        |
| **ResearchAgent**  | Validate new signals vs. walk-forward OOS.   | Historical price DB, config YAML.          | JSON report with IR, turnover, drawdown. | Train/Test split reproducibility checksum.            |
| **SignalAgent**    | Produce position targets given latest state. | Current tick, rolling window.              | Target size `[-1,1]` per asset.          | Unit tests: identical inputs yield identical targets. |
| **RiskAgent**      | Translate targets to risk-capped orders.     | Targets, current positions, config limits. | Order intents (side, qty, px).           | Reject order that breaches max drawdown or VAR.       |
| **ExecutionAgent** | Execute and reconcile orders on exchange.    | Order intents, API creds.                  | Fills, cancels, error codes.             | Retry logic ≤ 3; reconcile unmatched fills.           |
| **AuditAgent**     | Persist every event with hash chain.         | All upstream events.                       | Append-only Parquet/CSV.                 | Nightly log digest checksum = prior hash.             |
| **ReportingAgent** | Surface P\&L, risk, outages.                 | Audit logs.                                | CLI/Streamlit dashboard, alert hooks.    | Latency from event to display < 5 s.                  |

Agents communicate only via defined data contracts (Parquet/Arrow).  No hidden state.

---

## 5  Delivery Road-Map (0–12 mo)

| Phase                  | Duration | Gate                                    | Build Items                                                              | Career-Leverage Output                                   |
| ---------------------- | -------- | --------------------------------------- | ------------------------------------------------------------------------ | -------------------------------------------------------- |
| **P0 Bootstrap**       | 2 wks    | Fetch & place live test order           | Repo skeleton, DataAgent, ExecutionAgent (testnet).                      | Demonstrable “tip-to-tail” trade loop.                   |
| **P1 Live MVP**        | 4 wks    | 7 day unattended run                    | Momentum signal, basic risk, AuditAgent, CLI report.                     | First publicly verifiable micro-track-record.            |
| **P2 Robustness**      | 8 wks    | 99 % loop uptime                        | Walk-forward resear­ch suite, stop-loss, fail-over, alerting.             | Post-mortem write-up suitable for recruiter / allocator. |
| **P3 Multi-Strategy**  | 3 mo     | Portfolio IR stable vs. OOS             | Second uncorrelated strat, portfolio allocator, Streamlit dash.          | Evidence of PM skill: allocation & risk budgeting.       |
| **P4 Asset Expansion** | 3 mo     | Equity or REIT module passes unit tests | Adapt data + execution layers; slippage & fee modelling for lit markets. | Demonstrated portability beyond crypto.                  |

---

## 6  Career-Pivot Actions

1. **Monthly Devlog → LinkedIn article.**  Publish performance, lessons, and code snippets to build external credibility.
2. **Quarterly Whitepaper.**  Document methodology and controls at a standard suitable for an allocator DDQ.
3. **Track-Record Dossier.**  Maintain a notarised PDF bundle of audit logs, strategy descriptions, and risk metrics—ready for interview or seed capital pitches.
4. **Internal Alignment.**  Ensure compliance disclosure and optional demo to current employer; positions you as a low-risk internal PM candidate.

---

## 7  Non-Negotiable Quality Gates

| Category                  | Pass Criteria                                                                                 |
| ------------------------- | --------------------------------------------------------------------------------------------- |
| **Code**                  | 100 % unit test coverage on deterministic functions; static type checks pass.                 |
| **Risk**                  | Max daily loss ≤ configured risk budget; VAR back-tests within policy error bands.            |
| **Ops**                   | Restart from crash < 5 min; no orphaned orders on reconnect.                                  |
| **Audit**                 | SHA-256 hash chain of logs verifies unaltered history.                                        |
| **Performance Reporting** | Equity curve, drawdown, turnover, fee drag, and benchmark relative return calculated nightly. |

---

## 8  Governance Rules for AI Contributors

1. **Always cite data lineage** when generating research results.
2. **No silent parameter changes.**  All hyper-params must be stored in version-controlled YAML.
3. **Fail fast.**  If back-test IR improves by > 30 % relative to prior benchmark, auto-trigger a nested OOS test; decline to deploy otherwise.
4. **Explain decisions** in plain text before committing code; human reviews anything touching risk or execution.
5. **Stop trading** if live drawdown exceeds 3 σ of back-test drawdown; require manual reset.

---
