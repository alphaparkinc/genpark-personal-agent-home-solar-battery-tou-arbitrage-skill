# -*- coding: utf-8 -*-
"""MCP Server for Home Solar Battery TOU Tariff Arbitrage & Dispatch Skill."""
import sys
import json
import logging
from typing import Dict, Any

from .core import HomeSolarBatteryTOUArbitrageEngine

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

TOOLS_SCHEMA = [
    {
        "name": "optimize_battery_tou_dispatch",
        "description": "Compute hourly optimal battery charge, discharge, and grid export schedule against peak/off-peak energy rates to minimize daily electric bill.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "battery_capacity_kwh": {
                    "type": "number"
                },
                "current_state_of_charge_pct": {
                    "type": "number"
                },
                "daily_solar_generation_kwh": {
                    "type": "number"
                },
                "off_peak_rate_usd_per_kwh": {
                    "type": "number",
                    "description": "e.g. 0.15"
                },
                "on_peak_rate_usd_per_kwh": {
                    "type": "number",
                    "description": "e.g. 0.55"
                },
                "feed_in_tariff_usd_per_kwh": {
                    "type": "number",
                    "description": "e.g. 0.08"
                }
            },
            "required": [
                "battery_capacity_kwh",
                "current_state_of_charge_pct",
                "daily_solar_generation_kwh",
                "off_peak_rate_usd_per_kwh",
                "on_peak_rate_usd_per_kwh"
            ]
        }
    },
    {
        "name": "generate_storm_reserve_override_protocol",
        "description": "Synthesize a proactive storm watch backup power override when severe weather threats risk utility grid failure.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "weather_alert_level": {
                    "type": "string",
                    "enum": [
                        "ADVISORY",
                        "WATCH",
                        "WARNING",
                        "EMERGENCY"
                    ]
                },
                "forecasted_outage_hours": {
                    "type": "integer"
                },
                "critical_load_kw": {
                    "type": "number"
                }
            },
            "required": [
                "weather_alert_level",
                "forecasted_outage_hours",
                "critical_load_kw"
            ]
        }
    }
]

def handle_rpc(line: str) -> str:
    try:
        req = json.loads(line)
        method = req.get("method")
        msg_id = req.get("id")

        if method == "initialize":
            res = {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-personal-agent-home-solar-battery-tou-arbitrage-skill", "version": "1.0.0"}
            }
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": res})

        elif method == "tools/list":
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"tools": TOOLS_SCHEMA}})

        elif method == "tools/call":
            params = req.get("params", {})
            tool_name = params.get("name")
            args = params.get("arguments", {})

            target_func = getattr(HomeSolarBatteryTOUArbitrageEngine, tool_name, None)
            if not target_func:
                return json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": f"Method not found: {tool_name}"}})

            result = target_func(**args)
            return json.dumps({
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps(result, indent=2)}]
                }
            })

        else:
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": f"Method not found: {method}"}})

    except Exception as e:
        return json.dumps({"jsonrpc": "2.0", "id": req.get("id") if "req" in locals() else None, "error": {"code": -32000, "message": str(e)}})

def run_test():
    print("[TEST] Running internal RPC self-test for genpark-personal-agent-home-solar-battery-tou-arbitrage-skill...")
    init_req = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}})
    init_res = json.loads(handle_rpc(init_req))
    assert init_res.get("result", {}).get("serverInfo", {}).get("name") == "genpark-personal-agent-home-solar-battery-tou-arbitrage-skill"

    list_req = json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
    list_res = json.loads(handle_rpc(list_req))
    assert len(list_res.get("result", {}).get("tools", [])) == 2
    print(f"[TEST] SUCCESS: {len(list_res['result']['tools'])} tools verified.")
    return True

if __name__ == "__main__":
    if "--test" in sys.argv:
        if run_test():
            sys.exit(0)
        sys.exit(1)

    for line in sys.stdin:
        if not line.strip():
            continue
        out = handle_rpc(line)
        sys.stdout.write(out + "\n")
        sys.stdout.flush()
