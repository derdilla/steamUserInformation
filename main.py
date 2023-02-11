import typing
import yaml
import steamApi


class Config(typing.TypedDict):
    steamapi_key: str
    steamid: str
    float_precision: int


def load_config(configfile: str = 'config.yml') -> Config:
    with open(configfile, 'r') as stream:
        config = yaml.safe_load(stream)

    if len(config['steamapi_key']) != 32:
        raise ValueError(f'No steam api key specified in: {configfile}')
    if len(config['steamid']) != 17:
        raise ValueError(f'No steamid specified in: {configfile}')

    return config


def main() -> None:
    config = load_config()
    steamapi = steamApi.SteamApiConnector(config['steamapi_key'])

    user_infos = steamapi.get_player_summaries([config['steamid']])
    owned_games = steamapi.get_all_owned_games(config['steamid'])['games']

    username = 'unknown'
    if len(user_infos) >= 1:
        username = user_infos[0]['personaname']
    total_playtime = 0
    for game in owned_games:
        total_playtime += game['playtime_forever']

    print(f'Stats of {username}:')
    if total_playtime > 60:
        total_playtime_h = '{:.2f}'.format(total_playtime/60)
        print(f'Total playtime: {total_playtime_h}h')
    else:
        print(f'Total playtime: {total_playtime}m')


if __name__ == '__main__':
    main()
