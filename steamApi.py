import typing
import requests
import json


class PlayedGame(typing.TypedDict):
    appid: int
    name: str  # name of the app
    playtime_forever: int  # minutes
    img_icon_url: str
    playtime_windows_forever: int  # minutes
    playtime_mac_forever: int  # minutes
    playtime_linux_forever: int  # minutes
    rtime_last_played: int  # unix epoch timestamp
    content_descriptorids: typing.Optional[list[int]]


class PlayerInfo(typing.TypedDict):
    steamid: str
    communityvisibilitystate: int
    profilestate: int
    personaname: str
    commentpermission: int
    profileurl: str
    avatar: str
    avatarmedium: str
    avatarfull: str
    avatarhash: str
    lastlogoff: int
    personastate: int
    primaryclanid: str
    timecreated: int  # unix epoch timestamp
    personastateflags: int
    loccountrycode: str
    locstatecode: str


class AllOwnedGamesResponse(typing.TypedDict):
    game_count: int
    games: list[PlayedGame]


class SteamApiConnector:
    def __init__(self, steamapi_key: str):
        self.key = steamapi_key

    def get_all_owned_games(self, steamid: str, appinfo: bool = True, freegames: bool = True) -> AllOwnedGamesResponse:
        url = f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={self.key}&steamid={steamid}'
        if appinfo:
            url += '&include_appinfo=true'
        if freegames:
            url += '&include_played_free_games=true'

        response = requests.get(url).content
        response_data = json.loads(response)
        return response_data['response']

    def get_player_summaries(self, steamids: list[str]) -> list[PlayerInfo]:
        url = f'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={self.key}&steamids={steamids}'
        response = requests.get(url).content
        response_data = json.loads(response)
        return response_data['response']['players']
