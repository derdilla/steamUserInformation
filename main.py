import typing
import yaml
import steamApi
import collections


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


def minutes_by_category(games: list[steamApi.PlayedGame], cat_names: list[str] = None, cat_count: int = -1,) -> dict[str, int]:
    banned_cat_names = ['of', 'by', 'in', 'the']
    banned_cat_names += [str(x) for x in range(100)]

    if len(games) < 1:
        raise ValueError('list must not be empty')
    if games[0].get('name') is None:
        raise ValueError('list must contain game name')

    if cat_names is None:
        word_list: list[str] = []
        cat_names = []

        for game in games:
            word_list += game['name'].split(' ')

        # cleaning data
        for word in word_list:
            word = word.lower().strip('.,:; \t')
            if word not in banned_cat_names:
                cat_names.append(word)

        if cat_count < 1:
            cat_count = len(games)

        # the most common words, sorted by count
        cat_names = [x[0] for x in collections.Counter(cat_names).most_common(cat_count)]

    minutes_per_cat: dict[str, int] = {}
    for game in games:
        for cat_name in cat_names:
            # add game which title contains the word to corresponding category
            # a game can only have one category
            if cat_name in game['name'].lower():
                if minutes_per_cat.get(cat_name):
                    minutes_per_cat[cat_name] += game['playtime_forever']
                else:
                    minutes_per_cat[cat_name] = game['playtime_forever']
                break

    return minutes_per_cat


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

    minutes_per_cat = minutes_by_category(owned_games)
    print(minutes_per_cat)


if __name__ == '__main__':
    main()
