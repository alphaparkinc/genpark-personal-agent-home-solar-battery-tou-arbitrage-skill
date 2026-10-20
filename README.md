# Home Solar Battery TOU Tariff Arbitrage & Dispatch Skill

[![GenPark Official](https://img.shields.io/badge/GenPark-Official%20Skill-blue)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-GenPark-blue)](https://www.linkedin.com/company/92955550)
[![MCP Compliant](https://img.shields.io/badge/MCP-JSON--RPC%202.0-green)](https://modelcontextprotocol.io/)
[![Zero Dependency](https://img.shields.io/badge/Dependencies-Zero%20Stdlib-brightgreen)](https://python.org)

Residential solar PV generation forecasting, home battery storage (Tesla Powerwall / Enphase) charge/discharge dispatch against time-of-use (TOU) tariff curves, and grid export revenue maximizer. Built for GenPark (https://www.genpark.ai).

## 🌐 Official Channels
- **Official Website**: [https://www.genpark.ai](https://www.genpark.ai)
- **LinkedIn Page**: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550)

## 🛠️ MCP Tools Exposed
- `optimize_battery_tou_dispatch`: Compute hourly optimal battery charge, discharge, and grid export schedule against peak/off-peak energy rates to minimize daily electric bill.
- `generate_storm_reserve_override_protocol`: Synthesize a proactive storm watch backup power override when severe weather threats risk utility grid failure.

## 🚀 Installation & Usage
Run directly with pure Python standard library:
```bash
python -m genpark_personal_agent_home_solar_battery_tou_arbitrage_skill.server --test
```
