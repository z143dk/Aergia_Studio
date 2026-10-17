from schwab_api.client import SchwabClient
from squeeze_scanner import get_squeeze_candidates
from midas_strategist import MidasStrategist
import datetime

def run_briefing(output_callback=print):
    """
    Runs the briefing.
    output_callback: function to handle the text output (e.g. print, or gui_update)
    Returns: The full text report as a string.
    """
    report_lines = []

    def log(text):
        report_lines.append(text)
        output_callback(text)

    log(f"\n🌞 GOOD MORNING, TRADER! 🌞")
    log(f"Date: {datetime.date.today()}\n")
    
    # 1. Cash Check - Aggregate ALL Accounts
    client = SchwabClient()
    try:
        acct_ids = client.get_account_numbers()
        if acct_ids:
            total_net_liq = 0
            total_cash = 0
            
            log(f"💰 Account Status:")
            
            for i, acct in enumerate(acct_ids):
                # Retrieve details for each account
                hash_val = acct['hashValue']
                balance_info = client.get_account_balance(hash_val)
                
                sec_acct = balance_info.get('securitiesAccount', {})
                current_bal = sec_acct.get('currentBalances', {})
                
                # Schwab sometimes returns different fields for margin vs cash accounts
                # Try 'liquidationValue', fallback to 'equity'
                net_liq = current_bal.get('liquidationValue', current_bal.get('equity', 0))
                cash = current_bal.get('cashAvailableForTrading', 0)
                
                total_net_liq += net_liq
                total_cash += cash
                
                # Log individual (obfuscate hash for privacy if needed, using index)
                # Determine account type/name
                acct_type = sec_acct.get('type', 'Account')
                log(f"   [{i+1}] {acct_type}: ${net_liq} (Cash: ${cash})")

            log(f"   -------------------------")
            log(f"   TOTAL NET WORTH: ${total_net_liq}")
            log(f"   TOTAL CASH READY: ${total_cash}")
            
            if total_cash < 1000:
                log("\n⚠️ ALERT: Low Cash Balance. Fund account before placing big trades.")
        else:
            log("⚠️ No linked accounts found.")
            
    except Exception as e:
        log(f"⚠️ Could not fetch balance details: {e}")

    # 2. Squeeze Scanner
    log(f"\n🚀 Squeeze Watchlist (Zero-Cost):")
    candidates = get_squeeze_candidates()
    if not candidates:
        log("   No high-probability squeezes found today.")
    for c in candidates[:3]: # Top 3
        log(f"   * {c['symbol']} (SI: {c['short_float']}%) - Potential Squeeze!")

    # 3. AI Strategist
    log(f"\n🧠 Midas Brain (Daily Idea):")
    strategist = MidasStrategist()
    # Ask for a VERY short summary for the voice briefing
    idea = strategist.ask("Provide a 1-sentence trading idea for today's market conditions.", mode="explain")
    log(idea)
    
    return "\n".join(report_lines)

if __name__ == "__main__":
    run_briefing()
