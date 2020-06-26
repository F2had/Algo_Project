from extract_Info.analysis import Analysis


def apply_sentiment(paths_arg):
    analysis = Analysis(debug=False)
    analysis.run_analysis()

    percentage = analysis.neg / analysis.article_len

    # more than 30%
    if percentage > 0.3:
        if isinstance(paths_arg, dict):
            paths = [paths_arg]
        else:
            paths = paths_arg

        new_paths = []

        for path in paths:
            new_time = 0

            # direction = point name, transit, time, distance
            for direction in path['directions']:
                new_time_segment = direction[2]
                if direction[1] == 'Bus' or direction[1] == 'Car':
                    new_time_segment *= 1.3
                elif direction[1] == 'Walking':
                    new_time_segment *= 1.2

                new_time += new_time_segment

            new_path = dict(path)
            new_path['time'] = round(new_time)

            new_paths.append(new_path)

        if isinstance(paths_arg, dict):
            return new_paths[0]
        else:
            return new_paths

    return paths_arg
