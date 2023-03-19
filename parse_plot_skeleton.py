import numpy as np
import open3d as o3d

"""
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


if __name__ == "__main__":

    exploratory_get_wound_region_coordinates()