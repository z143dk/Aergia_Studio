
import os
import time
import logging
from intelligence_router import router
from router.schemas import TaskRequest

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("VisualCanon")

# Define the "Visual Canon" - 27 Assets
# Keys: Filenames
# Values: (Prompt, Aspect Ratio)
# Banners: 16:9 (Landscape) -> "landscape_16_9"
# Icons: 1:1 (Square) -> "square_hd"
# Wallpapers: 16:9 (Landscape) -> "landscape_16_9"

ASSETS = {
    # --- BANNERS (12) ---
    "Athena_Banner.png": ("Cinematic sci-fi fantasy library of wisdom, Athena motif, glowing neuron networks, teal and amber lighting, highly detailed, 8k, wide angle", "landscape_16_9"),
    "Prometheus_Banner.png": ("Cinematic sci-fi fantasy fire of knowledge, Prometheus motif, torch in darkness, teal and amber lighting, highly detailed, 8k, wide angle", "landscape_16_9"),
    "Hephaestus_Banner.png": ("Cinematic sci-fi fantasy forge of creation, Hephaestus motif, sparks and molten metal, teal and amber lighting, highly detailed, 8k, wide angle", "landscape_16_9"),
    "Aergia_Banner.png": ("Cinematic sci-fi fantasy sanctuary of rest, Aergia motif, soft pillows and clouds, teal and amber lighting, highly detailed, 8k, wide angle", "landscape_16_9"),
    "Hermes_Banner.png": ("Cinematic sci-fi fantasy speed and communication, Hermes motif, winged sandals and data streams, teal and amber lighting, highly detailed, 8k, wide angle", "landscape_16_9"),
    "Aura_Banner.png": ("Cinematic sci-fi fantasy wind and energy, Aura motif, swirling vortex of power, teal and amber lighting, highly detailed, 8k, wide angle", "landscape_16_9"),
    "Hestia_Banner.png": ("Cinematic sci-fi fantasy hearth and home, Hestia motif, warm central fire, teal and amber lighting, highly detailed, 8k, wide angle", "landscape_16_9"),
    "Hyperion_Banner.png": ("Cinematic sci-fi fantasy sun and oversight, Hyperion motif, watching eye, teal and amber lighting, highly detailed, 8k, wide angle", "landscape_16_9"),
    "Midas_Banner.png": ("Cinematic sci-fi fantasy gold and wealth, Midas motif, golden touch turning stone to gold, teal and amber lighting, highly detailed, 8k, wide angle", "landscape_16_9"),
    "Chimera_Banner.png": ("Cinematic sci-fi fantasy hybrid creature, Chimera motif, three heads, teal and amber lighting, highly detailed, 8k, wide angle", "landscape_16_9"),
    "Kairos_Banner.png": ("Cinematic sci-fi fantasy time and opportunity, Kairos motif, clockwork gears, teal and amber lighting, highly detailed, 8k, wide angle", "landscape_16_9"),
    "Plutus_Banner.png": ("Cinematic sci-fi fantasy abundance, Plutus motif, overflowing cornucopia, teal and amber lighting, highly detailed, 8k, wide angle", "landscape_16_9"),

    # --- ICONS (12) ---
    "Athena_Icon.png": ("Minimalist flat vector icon, Owl symbol of Athena, gold and teal, simple, clean, app icon style, white background", "square_hd"),
    "Prometheus_Icon.png": ("Minimalist flat vector icon, Torch symbol of Prometheus, gold and teal, simple, clean, app icon style, white background", "square_hd"),
    "Hephaestus_Icon.png": ("Minimalist flat vector icon, Anvil and Hammer symbol of Hephaestus, gold and teal, simple, clean, app icon style, white background", "square_hd"),
    "Aergia_Icon.png": ("Minimalist flat vector icon, Sleeping eye symbol of Aergia, gold and teal, simple, clean, app icon style, white background", "square_hd"),
    "Hermes_Icon.png": ("Minimalist flat vector icon, Winged Boot symbol of Hermes, gold and teal, simple, clean, app icon style, white background", "square_hd"),
    "Aura_Icon.png": ("Minimalist flat vector icon, Wind spiral symbol of Aura, gold and teal, simple, clean, app icon style, white background", "square_hd"),
    "Hestia_Icon.png": ("Minimalist flat vector icon, Hearth flame symbol of Hestia, gold and teal, simple, clean, app icon style, white background", "square_hd"),
    "Hyperion_Icon.png": ("Minimalist flat vector icon, Sun symbol of Hyperion, gold and teal, simple, clean, app icon style, white background", "square_hd"),
    "Midas_Icon.png": ("Minimalist flat vector icon, Golden Hand symbol of Midas, gold and teal, simple, clean, app icon style, white background", "square_hd"),
    "Chimera_Icon.png": ("Minimalist flat vector icon, Lion Goat Snake hybrid symbol of Chimera, gold and teal, simple, clean, app icon style, white background", "square_hd"),
    "Kairos_Icon.png": ("Minimalist flat vector icon, Hourglass symbol of Kairos, gold and teal, simple, clean, app icon style, white background", "square_hd"),
    "Plutus_Icon.png": ("Minimalist flat vector icon, Cornucopia symbol of Plutus, gold and teal, simple, clean, app icon style, white background", "square_hd"),

    # --- WALLPAPERS (3) ---
    "The_Journey.png": ("Epic expansive view, A traveler looking toward a teal horizon, cinematic, atmospheric, masterpiece, 8k", "landscape_16_9"),
    "The_Pantheon_Circle.png": ("All 12 symbols unified in a gold ring, The Pantheon Circle, minimalist, mystic, teal background, 8k", "landscape_16_9"),
    "The_Opening_Frame.png": ("Cinematic start-up screen, Aergia OS Logo centered, sleek, modern, futuristic, dark teal background, 8k", "landscape_16_9")
}

def download_file(url, filename):
    import requests
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(filename, 'wb') as f:
            f.write(response.content)
        return True
    except Exception as e:
        logger.error(f"Failed to download {filename}: {e}")
        return False

def main():
    logger.info("--- Starting Visual Canon Regeneration ---")
    
    success_count = 0
    
    for filename, (prompt, aspect_ratio) in ASSETS.items():
        if os.path.exists(filename):
            logger.info(f"Skipping existing: {filename}")
            success_count += 1
            continue

        logger.info(f"Generating: {filename}...")
        try:
            # Prepare payload for image_gen
            # Router expects 'image_gen' task type. 
            # Note: The router.executor logic for image_gen calls FALProvider.
            # FALProvider expects kwargs like 'image_size'.
            
            # Map simple aspect to FAL image_size enum/string if needed, 
            # or just pass it if your provider handles it.
            # Checking fal_provider.py triggers might be needed, but assuming standard payload structure.
            
            req = TaskRequest(
                prompt=prompt,
                task_type="image_gen",
                payload={
                    "image_size": aspect_ratio  # Passing explicitly
                }
            )
            
            # Execute
            result = router.orchestrate(req)
            
            # Result content from FAL provider is usually a URL string
            image_url = result.content
            
            if image_url and image_url.startswith("http"):
                if download_file(image_url, filename):
                    logger.info(f"✅ Saved: {filename}")
                    success_count += 1
                else:
                    logger.error(f"❌ Could not save {filename}")
            else:
                logger.error(f"❌ No valid URL returned for {filename}. Content: {str(image_url)[:50]}...")
                
        except Exception as e:
            logger.error(f"❌ Failed to generate {filename}: {e}")
            
    logger.info(f"\n--- Regeneration Complete: {success_count}/{len(ASSETS)} Assets Ready ---")

if __name__ == "__main__":
    main()
