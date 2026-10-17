from router.registry import ProviderRegistry, ProviderIDs

class MidasStrategist:
    def __init__(self):
        try:
            self.registry = ProviderRegistry()
            # Default to Flash for speed, fallback to whatever is available
            if self.registry.has(ProviderIDs.GOOGLE_GEMINI_FLASH):
                self.model_id = ProviderIDs.GOOGLE_GEMINI_FLASH
            else:
                self.model_id = self.registry.list_ids()[0] # Grab first available
            
            print(f"Midas Brain ONLINE. Connected via Router to: {self.model_id}")
        except Exception as e:
            print(f"CRITICAL WARNING: Router Init Failed: {e}")
            self.registry = None

    def ask(self, prompt, mode="study"):
        """
        Sends a request to Gemini to generate ThinkScript or explain a strategy.
        mode: 'study' (default), 'scan', 'strategy', 'explain'
        """
        # Pre-baked Expert Requests (Shortcuts)
        if "option hacker" in prompt.lower() or "unusual flow" in prompt.lower():
            prompt = (
                "Write a thinkScript for an Option Hacker scan that finds options where "
                "the current volume is at least 2x the open interest and the volume is greater than 1,000 contracts. "
                "Explain how to paste this into the Custom Filter."
            )
            mode = "scan"
        elif "flow sentiment" in prompt.lower() or "ask vs bid" in prompt.lower():
            prompt = (
                "Write a thinkScript column for a ToS Watchlist that shows the percentage of trades "
                "hitting the Ask vs the Bid for the current day to measure Flow Sentiment."
            )
            mode = "study"
        elif "alert" in prompt.lower() and "block" in prompt.lower():
            prompt = (
                "Write a thinkScript alert for ToS that triggers when a single trade exceeds 5,000 contracts "
                "and the IV is increasing. Set Notify to Push."
            )
            mode = "study"

        base_instruction = ""
        
        if mode == "study" or mode == "scan":
            base_instruction = (
                "You are an expert ThinkScript developer for Thinkorswim. "
                "Output ONLY valid ThinkScript code that accomplishes the user's request. "
                "Include comments explaining how to use it (e.g., 'Paste into Scan tab'). "
            )
        elif mode == "strategy":
            base_instruction = (
                "You are an expert Options Strategist. "
                "The user wants a ThinkScript Strategy to backtest this idea. "
                "Include 'AddOrder' calls for entry and exit. "
                "Also provide a brief comment on the recommended risk management."
            )
        elif mode == "explain":
            base_instruction = (
                "You are a helpful Options Mentor. Explain this concept simply and clearly. "
                "Use bullet points."
            )

        if not self.registry:
            return "Error: Brain Offline."

        full_prompt = f"{base_instruction}\n\nUser Request: {prompt}"
        
        try:
            provider = self.registry.get(self.model_id)
            # System prompt is effectively the base_instruction here
            response = provider.generate(prompt, system_prompt=base_instruction)
            
            # Unpack response
            content = response.get("content", "") if isinstance(response, dict) else response.content
            return content
        except Exception as e:
            return f"Error contacting Midas Brain: {e}"

if __name__ == "__main__":
    bot = MidasStrategist()
    print("Midas Strategist Initialized. Running Expert Tests...")
    
    # Test 1: Option Hacker Shortcut
    print("\n--- Test 1: asking for 'Unusual Options Flow' ---")
    response = bot.ask("I want to find unusual options flow", mode="scan")
    print(response)
    
    # Save output to file to prove it works
    with open("expert_scan_code.txt", "w") as f:
        f.write(response)
