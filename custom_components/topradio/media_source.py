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

    async def async_resolve_media(self, item: MediaSourceItem) -> PlayMedia:
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