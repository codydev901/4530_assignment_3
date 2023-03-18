import pandas as pd
import plotly.express as px


"""
Cody Whitt
pkz325
CPSC 4530 Spring 2023
Assignment 3

For DataSet 1 - Geospatial Point Based

Some references that helped me for this,
https://stackoverflow.com/questions/53233228/plot-latitude-longitude-from-csv-in-python-3-6
https://plotly.com/python/mapbox-layers/
"""


def date_str_to_season(date_str: str):
    """
    Quick helper function for assigning a "season" to a date in context of parse_data() below
    """

    month = int(date_str.split("/", 1)[0])
    if month in [12, 1, 2]:
        return "Winter"
    elif month in [3, 4, 5]:
        return "Spring"
    elif month in [6, 7, 8]:
        return "Summer"
    else:
        return "Fall"


def parse_data():
    """
    Parsing portion of DUI/crime data set
    """

    # Read to DataFrame, Look at Head/Info
    print("Initial Load/Check")
    raw_df = pd.read_csv("raw_data/Police_Incident_Data.csv")
    print(raw_df.head())
    print(raw_df.info())

    # Find CrimeType Attribute
    print("Finding Crime Type Attribute")
    print(raw_df['Incident_Description'].unique())  # Looks like it's this one
    print(raw_df['Incident_Type'].unique())

    # Filter to DUI
    print("Post-Crime Filter Check")
    parsed_df = raw_df[raw_df["Incident_Description"] == "Driving Under The Influence"]
    print(parsed_df.head())
    print(parsed_df.info())

    # Keep Attributes Filter and Drop NA
    print("Post-Attribute Filter and DropNA")
    keep_attributes = ["Date_Incident", "Incident_Description", "Latitude", "Longitude"]
    parsed_df = parsed_df[keep_attributes]
    parsed_df.dropna(inplace=True)
    print(parsed_df.head())
    print(parsed_df.info())

    # Assign "Season"
    print("Assign Season")
    parsed_df["Season"] = parsed_df["Date_Incident"].apply(lambda x: date_str_to_season(x))
    print(parsed_df.head())
    print(parsed_df.info())

    parsed_df.to_csv("parsed_data/chattanooga_dui_season_parsed.csv", index=False)


def plot_data():
    """
    Plotting portion of DUI/crime data set
    """

    # Read Parsed Data
    df = pd.read_csv("parsed_data/chattanooga_dui_season_parsed.csv")

    # Plot
    fig = px.scatter_mapbox(df,
                            lat="Latitude",
                            lon="Longitude",
                            color="Season",
                            zoom=12,
                            title="Chattanooga DUI Arrest Locations By Season")

    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(autosize=True, hovermode='closest')

    # Annotations For Season Percents
    winter_a_p = round(len(df[df["Season"] == "Winter"]) / len(df) * 100.0, 1)
    spring_a_p = round(len(df[df["Season"] == "Spring"]) / len(df) * 100.0, 1)
    summer_a_p = round(len(df[df["Season"] == "Summer"]) / len(df) * 100.0, 1)
    fall_a_p = round(len(df[df["Season"] == "Fall"]) / len(df) * 100.0, 1)

    fig.add_annotation(text=f'Winter: {winter_a_p}%<br>Spring: {spring_a_p}%<br>Summer: {summer_a_p}%<br>Fall: {fall_a_p}%',
                       align='left',
                       showarrow=False,
                       xref='paper',
                       yref='paper',
                       x=1.07,
                       y=0.9,
                       bordercolor='black',
                       borderwidth=1)

    fig.show()


def main():

    parse_data()

    plot_data()


if __name__ == "__main__":

    main()

