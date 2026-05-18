# BIND9 Statistics Integration for Home Assistant

A lightweight, high-performance Home Assistant custom integration that polls metrics from a BIND9 DNS server's JSON statistics channel. 

Using Home Assistant's native `DataUpdateCoordinator`, this integration fetches data from your server exactly once per polling interval and updates all tracked sensors asynchronously, minimizing resource overhead on your DNS server.

## Features

* **UI Configuration:** Fully configurable via **Settings > Devices & Services** (no YAML required).
* **Connection Validation:** Automatically validates that the host endpoint is accessible before saving.
* **Long-Term Statistics Support:** Cumulative counters use `state_class: total_increasing`, making them fully compatible with Home Assistant's built-in statistical graphs and Energy/Utility dashboards.
* **Duplicate Prevention:** Prevents configuring multiple instances for the same host.

## Installation

### Method 1: HACS (Recommended)

1. Open **HACS** in your Home Assistant interface.
2. Click the **three dots (⋮)** in the top right corner and select **Custom repositories**.
3. Paste the URL of this repository into the **Repository** field:
   `https://github.com/yourusername/ha-bind9-stats`
4. Select **Integration** from the **Category** dropdown menu.
5. Click **Add**, then find the **BIND9 Statistics** card and click **Download**.
6. **Restart** Home Assistant.

### Method 2: Manual Installation

1. Download the source code as a ZIP file.
2. Extract the contents and copy the `custom_components/bind9_stats/` directory into your Home Assistant `config/custom_components/` directory.
3. Your folder structure should look like this:
   ```text
   config/
   └── custom_components/
       └── bind9_stats/
           ├── __init__.py
           ├── config_flow.py
           ├── manifest.json
           ├── sensor.py
           └── strings.json
