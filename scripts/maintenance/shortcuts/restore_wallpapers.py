
import os
import logging
from intelligence_router import router
from router.schemas import TaskRequest

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("WallpaperRestore")

# The 3 Master Wallpapers (Canon Flow: Teal/Amber/Cinematic)
WALLPAPERS = {
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
    logger.info("--- Restoring Wallpapers to Canon Flow ---")
    
    for filename, (prompt, aspect_ratio) in WALLPAPERS.items():
        logger.info(f"Regenerating: {filename} (Force Quality)...")
        
        # Delete existing to force new generation
        if os.path.exists(filename):
            try:
                os.remove(filename)
                logger.info(f"Deleted legacy/existing {filename}")
            except Exception as e:
                logger.warning(f"Could not delete {filename}: {e}")

        try:
            req = TaskRequest(
                prompt=prompt,
                task_type="image_gen",
                payload={"image_size": aspect_ratio}
            )
            
            result = router.orchestrate(req)
            image_url = result.content
            
            if image_url and image_url.startswith("http"):
                if download_file(image_url, filename):
                    logger.info(f"✅ Restored: {filename}")
                else:
                    logger.error(f"❌ Save Failed: {filename}")
            else:
                logger.error(f"❌ No URL for {filename}")
                
        except Exception as e:
            logger.error(f"❌ Generation Failed for {filename}: {e}")

    logger.info("--- Wallpaper Restoration Complete ---")

if __name__ == "__main__":
    main()
