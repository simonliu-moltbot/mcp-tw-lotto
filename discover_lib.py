from TaiwanLottery import TaiwanLotteryCrawler
import sys

try:
    crawler = TaiwanLotteryCrawler()
    print("Fetching Super Lotto...", file=sys.stderr)
    res = crawler.super_lotto()
    print(f"Super Lotto Type: {type(res)}", file=sys.stderr)
    print(f"Super Lotto Data: {res}", file=sys.stderr)
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
