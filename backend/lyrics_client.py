"""
LrcLib API Client for fetching song lyrics
"""
from typing import Optional, Dict
import aiohttp
import asyncio
from dataclasses import dataclass

@dataclass
class LyricsResult:
    """Container for lyrics data"""
    synced_lyrics: Optional[str] = None
    plain_lyrics: Optional[str] = None
    track_name: Optional[str] = None
    artist_name: Optional[str] = None
    album_name: Optional[str] = None
    duration: Optional[int] = None

class LyricsClient:
    """Async client for LrcLib API"""
    
    BASE_URL = "https://lrclib.net/api"
    USER_AGENT = "tidal-troi-ui/1.0.0 (https://github.com/RayZ3R0/tidal-troi-ui)"
    
    def __init__(self):
        self.session = None
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session"""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(
                headers={"User-Agent": self.USER_AGENT}
            )
        return self.session
    
    async def close(self):
        """Close the session"""
        if self.session and not self.session.closed:
            await self.session.close()
    
    async def get_lyrics(
        self,
        track_name: str,
        artist_name: str,
        album_name: Optional[str] = None,
        duration: Optional[int] = None
    ) -> Optional[LyricsResult]:
        """
        Get lyrics for a track
        
        Args:
            track_name: Name of the track
            artist_name: Name of the artist
            album_name: Name of the album (optional)
            duration: Duration in seconds (optional, helps matching)
        
        Returns:
            LyricsResult or None if not found
        """
        try:
            session = await self._get_session()
            
            params = {
                "track_name": track_name,
                "artist_name": artist_name,
            }
            
            if album_name:
                params["album_name"] = album_name
            if duration:
                params["duration"] = duration
            
            async with session.get(
                f"{self.BASE_URL}/get",
                params=params,
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                if response.status == 404:
                    print(f"  ℹ️  No lyrics found for: {artist_name} - {track_name}")
                    return None
                
                if response.status != 200:
                    print(f"  ⚠️  Lyrics API returned {response.status}")
                    return None
                
                data = await response.json()
                
                return LyricsResult(
                    synced_lyrics=data.get("syncedLyrics"),
                    plain_lyrics=data.get("plainLyrics"),
                    track_name=data.get("trackName"),
                    artist_name=data.get("artistName"),
                    album_name=data.get("albumName"),
                    duration=data.get("duration")
                )
                
        except asyncio.TimeoutError:
            print(f"  ⚠️  Lyrics API timeout for: {track_name}")
            return None
        except Exception as e:
            print(f"  ⚠️  Error fetching lyrics: {e}")
            return None
    
    async def search_lyrics(
        self,
        track_name: Optional[str] = None,
        artist_name: Optional[str] = None,
        album_name: Optional[str] = None
    ) -> list:
        """
        Search for lyrics
        
        Returns list of matching tracks
        """
        try:
            session = await self._get_session()
            
            params = {}
            if track_name:
                params["track_name"] = track_name
            if artist_name:
                params["artist_name"] = artist_name
            if album_name:
                params["album_name"] = album_name
            
            if not params:
                return []
            
            async with session.get(
                f"{self.BASE_URL}/search",
                params=params,
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                if response.status != 200:
                    return []
                
                return await response.json()
                
        except Exception as e:
            print(f"  ⚠️  Error searching lyrics: {e}")
            return []

# Global instance
lyrics_client = LyricsClient()