import requests
import datetime
import sys
import urllib3

# Suppress InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Constants
API_BASE = "https://api.taiwanlottery.com/TLCAPIWeB/Lottery"

GAME_MAP = {
    "super": "威力彩 (Super Lotto)",
    "big": "大樂透 (Big Lotto)",
    "539": "今彩539 (Daily Cash)"
}

API_CONFIG = {
    "super": {
        "endpoint": "SuperLotto638Result",
        "key": "superLotto638Res",
        "special": True
    },
    "big": {
        "endpoint": "Lotto649Result",
        "key": "lotto649Res",
        "special": True
    },
    "539": {
        "endpoint": "Daily539Result",
        "key": "daily539Res",
        "special": False
    }
}

def get_current_month_str():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m")

def get_latest_result(game_type: str):
    if game_type not in API_CONFIG:
        return {"error": "Invalid game type"}

    config = API_CONFIG[game_type]
    month = get_current_month_str()
    url = f"{API_BASE}/{config['endpoint']}?period&month={month}&pageSize=1"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
    }

    try:
        # verify=False because of SSL issues on some environments for this specific host
        resp = requests.get(url, headers=headers, verify=False, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        sys.stderr.write(f"API Fetch Error: {e}\n")
        return {"error": str(e)}

    # Parse content
    try:
        content = data.get("content", {})
        res_list = content.get(config["key"], [])
        if not res_list:
            return {"error": "No data found for this month"}
        
        # Latest is usually the first one because we requested pageSize=1?
        # Actually API returns list, likely sorted by date desc if we didn't specify order, 
        # but let's take the first one (latest period).
        latest = res_list[0]
        
        raw_nums = latest.get("drawNumberSize", [])
        period = latest.get("period")
        date_str = latest.get("lotteryDate") # 2026-01-30T00:00:00

        # Format date
        if date_str:
            date_str = date_str.split("T")[0]

        result = {
            "name": GAME_MAP[game_type],
            "term": str(period),
            "date": date_str,
            "regular": [],
            "special": None
        }

        if config["special"]:
            # Last one is special
            if len(raw_nums) > 0:
                result["regular"] = [str(n).zfill(2) for n in raw_nums[:-1]]
                result["special"] = str(raw_nums[-1]).zfill(2)
        else:
            result["regular"] = [str(n).zfill(2) for n in raw_nums]
            result["special"] = None
            
        return result

    except Exception as e:
        sys.stderr.write(f"Parsing Error: {e}\n")
        return {"error": f"Failed to parse API response: {e}"}

def fetch_all_games():
    # Helper for testing or bulk fetch
    results = {}
    for key in GAME_MAP:
        res = get_latest_result(key)
        if "error" not in res:
            results[key] = res
    return results
