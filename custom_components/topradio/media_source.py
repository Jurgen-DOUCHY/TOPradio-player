from homeassistant.components.media_source import MediaSource, MediaSourceItem, PlayMedia
from homeassistant.components.media_source.models import BrowseMediaSource
from homeassistant.core import HomeAssistant
from .const import DOMAIN, STATIONS

async def async_get_media_source(hass: HomeAssistant):
    return TOPradioSource(hass)

class TOPradioSource(MediaSource):
    name: str = "TOPradio"
    domain = DOMAIN
    
    def __init__(self, hass: HomeAssistant):
        super().__init__(DOMAIN)
        self.hass = hass
        self.thumbnail = "https://api.topradio.be/images/34292.a1097ca.16-9.1000.90.jpg"

    async def async_resolve_media(self, item: MediaSourceItem) -> PlayMedia:
        # Find the corresponding station for the stream
        for station in STATIONS:
            if station["source"] == item.identifier:
                return PlayMedia(
                    url=item.identifier,
                    mime_type="audio/mpeg",
                    title=station["name"],
                    thumbnail=station["logo"]
                )
        return PlayMedia(item.identifier, "audio/mpeg")

    async def async_browse_media(self, item: MediaSourceItem) -> BrowseMediaSource:
        streams = []
        
        for station in STATIONS:
            streams.append(
                BrowseMediaSource(
                    domain=DOMAIN,
                    identifier=station["source"],
                    media_class="music",
                    media_content_type="audio/mpeg",
                    title=station["name"],
                    can_play=True,
                    can_expand=False,
                    thumbnail=station["logo"]
                )
            )

        return BrowseMediaSource(
            domain=DOMAIN,
            identifier=None,
            media_class="directory",
            media_content_type="audio/mpeg",
            title="TOPradio",
            can_play=False,
            can_expand=True,
            children=streams,
            thumbnail=self.thumbnail
        )