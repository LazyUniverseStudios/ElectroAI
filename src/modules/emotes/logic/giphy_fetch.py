import os
import random
import aiohttp

GIPHY_API_KEY = os.getenv("GIPHY_API_KEY")

async def fetch_giphy_emote(emote_name: str) -> str | None:
    """
    Fetch a random GIF URL from Giphy based on the provided emote name.

    Args:
        emote_name (str): The name of the emote to search for.
    
    Returns:
        str | None: A URL of a random GIF from Giphy, or None if no valid GIF was found.
    """
    search_url = "https://api.giphy.com/v1/gifs/search"
    search_params = {
        "api_key": GIPHY_API_KEY,
        "q": emote_name,
        "limit": 50,
        "offset": 0,
        "rating": "pg-13",
        "lang": "en"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(search_url, params=search_params) as response:
            if response.status != 200:
                print(f"Giphy API error: {response.status}")
                return None
                
            data = await response.json()
            gifs = data.get("data", [])
            
            if not gifs:
                return None

            valid_gifs = []
            for gif in gifs:
                # Extract title and slug safely
                title = gif.get("title", "").lower()
                slug = gif.get("slug", "").lower()
                
                # Extract tags if present (handling both list of strings or list of dicts)
                raw_tags = gif.get("tags") or []
                tags_text = " ".join(
                    t if isinstance(t, str) else t.get("name", "") 
                    for t in raw_tags
                ).lower()

                # Combine all searchable text
                metadata = f"{title} {slug} {tags_text}"

                # Exclude if "peak" appears anywhere in the metadata
                if "peak" not in metadata:
                    valid_gifs.append(gif)

            if not valid_gifs:
                return None

            random_gif = random.choice(valid_gifs)
            return random_gif["images"]["original"]["url"]