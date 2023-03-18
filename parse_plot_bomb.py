import pandas as pd
import json
import folium

from folium.plugins import HeatMapWithTime

"""
Cody Whitt
pkz325
CPSC 4530 Spring 2023
Assignment 3

For DataSet 2 - Geospatial Pixel/Area Based

Some references that helped me for this,
https://towardsdatascience.com/data-101s-spatial-visualizations-and-analysis-in-python-with-folium-39730da2adf
https://www.kaggle.com/code/daveianhickey/how-to-folium-for-maps-heatmaps-time-analysis
"""


def parse_data():
    """
    Parsing Step for WW2 DataSet
    """

    # Read in Raw and Look
    print("Load Raw")
    raw_df = pd.read_csv("raw_data/operations.csv")
    print(raw_df.head())
    print(raw_df.info())

    # Filter to applicable attributes
    print("First Filter")
    keep_attributes = ["Mission Date", "Target Latitude", "Target Longitude", "High Explosives Weight (Tons)"]
    parsed_df = raw_df[keep_attributes]
    parsed_df.dropna(inplace=True)
    print(parsed_df.head())
    print(parsed_df.info())

    # Filter to Europe Only
    print("Second Filter")
    parsed_df = parsed_df[(parsed_df["Target Latitude"] >= 34.0) &
                          (parsed_df["Target Latitude"] <= 72.0)]
    parsed_df = parsed_df[(parsed_df["Target Longitude"] >= -25.0) &
                          (parsed_df["Target Longitude"] <= 45.0)]
    print(parsed_df.head())
    print(parsed_df.info())

    # Check Weights, Discard 0.0 Weights
    print("Check Weight 1")
    print(parsed_df["High Explosives Weight (Tons)"].max())
    print(parsed_df["High Explosives Weight (Tons)"].min())

    print("Third Filter")
    parsed_df = parsed_df[parsed_df["High Explosives Weight (Tons)"] != 0.0]
    print(parsed_df.head())
    print(parsed_df.info())

    print("Check Weight 2")
    print(parsed_df["High Explosives Weight (Tons)"].max())
    print(parsed_df["High Explosives Weight (Tons)"].min())

    # Convert to Mission Year
    print("Mission Year")
    parsed_df["Mission Year"] = parsed_df["Mission Date"].apply(lambda x: x.split("/")[-1])
    print(parsed_df.head())
    print(parsed_df.info())

    # Write
    parsed_df.to_csv("parsed_data/ww2_bombing_parsed.csv", index=False)


def plot_data():
    """
    Plotting Step for WW2 DataSet
    """

    print("Plotting WW2")
    print("Note: Writes .html to /figures, I then opened in browser to view/interact")

    df = pd.read_csv("parsed_data/ww2_bombing_parsed.csv")

    # Folium Map Object
    map_obj = folium.Map(location=[50.0, 10.0], zoom_start=5)

    # Pre-sort so the year filtering/use below works right
    df.sort_values(by=["Mission Year"], inplace=True, ascending=True)

    # Add Data for heatmap, grouped by year
    lats_longs = []
    for year in list(df["Mission Year"].unique()):
        print(f"Adding Year:{year}")
        year_df = df[df["Mission Year"] == year]
        year_lat_longs = []
        for i, row in year_df.iterrows():
            year_lat_longs.append(
                [row["Target Latitude"], row["Target Longitude"], row["High Explosives Weight (Tons)"]])
        lats_longs.append(year_lat_longs)

    HeatMapWithTime(data=lats_longs,
                    index=list(df["Mission Year"].unique())).add_to(map_obj)

    # Add a title, found way here (Though it does require scrolling)
    # https://stackoverflow.com/questions/61928013/adding-a-title-or-text-to-a-folium-map
    loc = 'Allied Bombing By Tonnage in WW2 Europe By Year'
    title_html = '''
                     <h3 align="center" style="font-size:16px"><b>{}</b></h3>
                     '''.format(loc)
    map_obj.get_root().html.add_child(folium.Element(title_html))
    map_obj.save("figures/folium_ww2_bombing.html")


def main():

    parse_data()

    plot_data()


if __name__ == "__main__":

    main()
