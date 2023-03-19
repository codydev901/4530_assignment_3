import numpy as np
import pandas as pd
import open3d as o3d

"""
Cody Whitt
pkz325
CPSC 4530 Spring 2023
Assignment 3

For DataSet 3 - Scientific

Colors
https://github.com/isl-org/Open3D/issues/614
"""


def exploratory_get_wound_region_coordinates():

    print("Load a ply point cloud, print it, and render it")
    pcd = o3d.io.read_point_cloud("raw_data/Human skeleton.ply")
    # ply_point_cloud = o3d.data.PLYPointCloud()
    # pcd = o3d.io.read_point_cloud(ply_point_cloud.path)
    # print(pcd.points)
    # print("Colors")
    # print(np.asarray(pcd.colors))
    # print("Points")
    # print(np.asarray(pcd.points))
    # print(pcd)
    # num_points = len(np.asarray(pcd.points))
    # new_points = []
    new_colors = []
    for i, p in enumerate(pcd.points):
        if p[2] > 600:  # Head And Neck (Head)
            new_colors.append([0.0, 0.0, 0.0])
        elif p[2] < 5:  # Legs/Hands (Extremities)
            new_colors.append([0.0, 1.0, 0.0])
        elif p[0] < -93 or p[0] > 143:  # Arms (Extremities)
            new_colors.append([0.0, 1.0, 0.0])
        elif p[2] < 300:  # Abdomen
            new_colors.append([0.0, 0.0, 1.0])
        else:  # Chest
            new_colors.append([1.0, 0.0, 0.0])

    pcd.colors = o3d.utility.Vector3dVector(np.asarray(new_colors))
    # pcd.points = o3d.utility.Vector3dVector(np.asarray(new_points))

    o3d.visualization.draw_geometries([pcd])
                                      # zoom=0.99,
                                      # front=[0.4257, -0.2125, -0.8795],
                                      # lookat=[2.6172, 2.0475, 1.532],
                                      # up=[-0.0694, -0.9768, 0.2024])


def rgb_from_df_percent(df: pd.DataFrame, wound_location: str):

    wound_percent = df[df["wound_location"] == wound_location]
    wound_percent = list(wound_percent["relative_survival_rate_adjusted"])[0]

    red_percent = 1.0 - wound_percent

    return [red_percent, wound_percent, 0.0]


def plot_skeleton(civil_war: str):

    print(f"Generating Figure For:{civil_war}")

    df = pd.read_csv("parsed_data/civil_war_parsed.csv")
    df = df[df["civil_war"] == civil_war]
    pcd = o3d.io.read_point_cloud("raw_data/Human skeleton.ply")

    head_color = rgb_from_df_percent(df, "head")
    extremities_color = rgb_from_df_percent(df, "extremity")
    abdomen_color = rgb_from_df_percent(df, "abdomen")
    chest_color = rgb_from_df_percent(df, "chest")

    new_colors = []
    for i, p in enumerate(pcd.points):
        if p[2] > 600:  # Head And Neck (Head)
            new_colors.append(head_color)
        elif p[2] < 5:  # Legs/Hands (Extremities)
            new_colors.append(extremities_color)
        elif p[0] < -93 or p[0] > 143:  # Arms (Extremities)
            new_colors.append(extremities_color)
        elif p[2] < 300:  # Abdomen
            new_colors.append(abdomen_color)
        else:  # Chest
            new_colors.append(chest_color)

    pcd.colors = o3d.utility.Vector3dVector(np.asarray(new_colors))
    o3d.visualization.draw_geometries([pcd])


if __name__ == "__main__":

    # exploratory_get_wound_region_coordinates()

    plot_skeleton(civil_war="United States")

    # plot_skeleton(civil_war="Syria")