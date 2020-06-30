from extract_Info.analysis import Analysis

articles = {
    "Bus": [
        "http://english.astroawani.com/topic/rapid-kl-bus",
        "https://www.thestar.com.my/tech/tech-news/2020/06/19/google-maps-now-shows-bus-arrival-times-in-klang-valley#cxrecs_s",
        "https://moovitapp.com/kuala_lumpur-1082/alerts",
        "https://www.nst.com.my/news/nation",
        "https://www.thestar.com.my/metro/metro-news/2020/06/19/get-real-time-info-on-kl-buses-via-google-maps",
    ],
    "Train": [
        "https://www.nst.com.my/news/nation",
        "https://www.thestar.com.my/metro/metro-news/2020/06/19/get-real-time-info-on-kl-buses-via-google-maps",
        "https://moovitapp.com/kuala_lumpur-1082/alerts",
        "http://english.astroawani.com/topic/lrt-service",
        "https://www.kliaekspres.com/category/news/",
    ],
    "Walking": [
        "http://english.astroawani.com/topic/weather-forecast",
        "https://www.accuweather.com/en/my/kuala-lumpur/233776/weather-forecast/233776",
        "https://www.timeanddate.com/weather/malaysia/kuala-lumpur/ext",
        "https://www.theweathernetwork.com/my/weather/wilayah-persekutuan-kuala-lumpur/kuala-lumpur",
        "https://www.worldweatheronline.com/kuala-lumpur-weather/kuala-lumpur/my.aspx",
    ],
    "Car": [
        "https://www.carlist.my/news/road-closure--472442/",
        "https://worldofbuzz.com/these-roads-near-jalan-tun-razak-will-be-closed-at-certain-times-from-13th-march-till-29th-march/",
        "https://www.nst.com.my/news/nation/2020/05/589807/cmco-no-more-police-roadblocks-kl-today",
        "https://www.nst.com.my/news/nation/2020/04/580386/mco-9-roads-gombak-be-closed-today",
        "https://worldofbuzz.com/starting-8pm-today-these-main-roads-in-kl-will-be-closed-for-new-years-celebrations/",
    ]
}


def apply_sentiment(paths_arg):
    analysis = Analysis(debug=False)

    sentiment_data = dict()

    for type in articles:
        total_neg = 0
        total_size = 0
        for article in articles[type]:
            analysis.run_analysis(article)

            total_neg += analysis.neg
            total_size += analysis.article_len

        # percentage of negative words + 1
        sentiment_data[type] = (total_neg / total_size) + 1

    # more than 30%

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

            # apply by the type
            if direction[1] in sentiment_data:
                new_time_segment *= sentiment_data[direction[1]]

            new_time += new_time_segment

        new_path = dict(path)
        new_path['time'] = round(new_time)

        new_paths.append(new_path)

    if isinstance(paths_arg, dict):
        return new_paths[0]
    else:
        return new_paths
