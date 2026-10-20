# -*- coding: utf-8 -*-
"""Home Solar Battery TOU Tariff Arbitrage & Dispatch for GenPark Personal Agent."""
import json
from typing import Dict, Any

class HomeSolarBatteryTOUArbitrageEngine:
    """Residential energy storage dispatch and TOU tariff price spread arbitrage engine."""

    @staticmethod
    def optimize_battery_tou_dispatch(battery_capacity_kwh: float, current_state_of_charge_pct: float, daily_solar_generation_kwh: float, off_peak_rate_usd_per_kwh: float, on_peak_rate_usd_per_kwh: float, feed_in_tariff_usd_per_kwh: float = 0.08) -> Dict[str, Any]:
        """Compute optimal battery charge/discharge schedule to exploit peak/off-peak rate differential."""
        usable_capacity = battery_capacity_kwh * 0.90  # 10% reserve margin
        available_energy = usable_capacity * (current_state_of_charge_pct / 100.0)
        
        # Energy arbitrage spread
        rate_spread = on_peak_rate_usd_per_kwh - off_peak_rate_usd_per_kwh
        # Daily financial savings from discharging battery during peak 4-9 PM instead of pulling from grid
        peak_discharge_kwh = min(usable_capacity, daily_solar_generation_kwh * 0.60 + available_energy)
        daily_arbitrage_savings = round(peak_discharge_kwh * rate_spread, 2)
        annualized_savings = round(daily_arbitrage_savings * 365, 2)

        return {
            "battery_capacity_kwh": battery_capacity_kwh,
            "usable_capacity_kwh": usable_capacity,
            "rate_spread_per_kwh": round(rate_spread, 3),
            "recommended_dispatch_mode": "TOU_ARBITRAGE_MAX_SELF_CONSUMPTION",
            "dispatch_schedule": {
                "00:00 - 06:00 (Super Off-Peak)": "Grid top-up if battery SOC < 40% at low rate.",
                "06:00 - 16:00 (Solar Generation)": "Direct solar to home load; surplus to 100% battery charge.",
                "16:00 - 21:00 (Peak Window)": f"Discharge battery to power 100% household load (Save ${on_peak_rate_usd_per_kwh}/kWh).",
                "21:00 - 24:00 (Off-Peak)": "Switch to grid power; preserve 20% emergency reserve."
            },
            "estimated_daily_savings_usd": daily_arbitrage_savings,
            "estimated_annual_savings_usd": annualized_savings
        }

    @staticmethod
    def generate_storm_reserve_override_protocol(weather_alert_level: str, forecasted_outage_hours: int, critical_load_kw: float) -> Dict[str, Any]:
        """Override economic arbitrage to guarantee 100% home backup power before storm grid failure."""
        required_backup_kwh = critical_load_kw * forecasted_outage_hours
        return {
            "weather_alert": weather_alert_level,
            "action": "SUSPEND_ARBITRAGE_ENGAGE_STORM_WATCH",
            "target_soc_pct": 100.0,
            "critical_backup_required_kwh": round(required_backup_kwh, 1),
            "load_shedding_recommendations": [
                "De-energize EV charger and heat pump auxiliary strips.",
                "Maintain refrigeration, well pump, and medical circuit power delivery.",
                "Disable all non-essential smart plug loads."
            ],
            "estimated_off_grid_runtime_hours": forecasted_outage_hours
        }
