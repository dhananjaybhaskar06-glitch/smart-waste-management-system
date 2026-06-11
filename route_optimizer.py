def get_collection_route(df):

    route = (
        df.sort_values(
            "fill_percentage",
            ascending=False
        )
        [["bin_id",
          "location",
          "fill_percentage"]]
    )

    return route