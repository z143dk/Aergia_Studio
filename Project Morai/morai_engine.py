import os
import sys
import logging

# Add parent directory to path to find intelligence_router
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from intelligence_router import router, TaskType
except ImportError:
    print("CRITICAL: Intelligence Router not found. Run from Project Aergia root.")
    sys.exit(1)

logging.basicConfig(level=logging.INFO, format='[MORAI] %(message)s')

class MoraiEngine:
    def __init__(self):
        self.router = router
        logging.info("Morai Engine Initialized (Genie Emulation Ready).")
        logging.info("Waiting for World Generation request...")

    def create_world(self, theme, description):
        """
        Uses the 'Genie 3' (Emulated via Gemini Pro) to design a game world.
        """
        logging.info(f"Genie: Dreaming up a '{theme}' world...")
        
        system_prompt = (
            "You are 'Genie', an advanced AI World Builder. "
            "Your job is to generate a comprehensive Game Design Document based on a theme. "
            "Describe the visual style, physics rules, and key locations."
        )
        
        user_prompt = f"THEME: {theme}\nDESCRIPTION: {description}"
        
        # Use Router with CREATIVE task type (Gemini Studio/Pro)
        world_design = self.router.generate(user_prompt, task_type=TaskType.CREATIVE, system_prompt=system_prompt)
        
        logging.info("Genie: World Design Complete.")
        return world_design

if __name__ == "__main__":
    engine = MoraiEngine()
    
    # Test Run
    print("\n--- Project Morai: Genie Test ---")
    theme = input("Enter a world theme (e.g., Cyberpunk City): ")
    if theme:
        design = engine.create_world(theme, "A dark city driven by neon lights and rain.")
        print("\n[GENIE OUTPUT]:\n")
        print(design)
