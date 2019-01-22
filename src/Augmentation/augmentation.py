import numpy as np
from open3d import *
import copy
import sys,os
from collections import defaultdict

from utils import helper
from utils.icp_helper import get_registeration
from utils.vis_helper import *

rel_path = os.path.realpath('')
reconstructed_scene = rel_path + '/Samples/scene0000_01_vh_clean_2.ply'
segmented_reconstructed_scene = rel_path + '/Samples/scene0000_01_vh_clean_2.labels.ply'
bed_pc_name = rel_path + '/Samples/new_bed.ply'

bed_hash = '1.0-0.7333333333333333-0.47058823529411764'

class Augmentor:

    def __init__(self, pointcloud, labeld_pointcloud):

        self.pointcloud = pointcloud
        self.labeld_pointcloud = labeld_pointcloud

        self.__find_all_objects()

    def __show_all_objects(self):

        for t in self.objects_dictionary_by_color:
            print(t)
            pcd = self.get_object_with_hashed_color(t)
            show_pcd([pcd])

    def get_object_with_hashed_color(self, hashed_color):

        return select_down_sample(self.pointcloud, self.objects_dictionary_by_color[hashed_color])

    def remove_object_with_index(self, hashed_color):

        l = range(0, len(self.pointcloud.points))
        return select_down_sample(self.pointcloud, [x for x in l if x not in self.objects_dictionary_by_color[hashed_color]])
    
    def change_object(self, object_to_change):

        object_to_change_hash = self.__get_hashed_color_of_object_from_name(object_to_change)

        scene_without_old_object = self.remove_object_with_index(object_to_change_hash)
        old_object = self.get_object_with_hashed_color(object_to_change_hash)

        source = self.__get_new_object_from_dataset(object_to_change_hash)

        transformed_new_object = self.__automated_registraion(source, old_object)

        return transformed_new_object, scene_without_old_object

    def __get_hashed_color_of_object_from_name(self, object_name):

        if(object_name is 'bed'):
            return bed_hash

    def __get_new_object_from_dataset(self, hashed_color):

        if(hashed_color is bed_hash):
            return read_point_cloud(bed_pc_name)

    def __automated_registraion(self, source, target):

        transformation = get_registeration(0.5, source, target)

        source_temp = copy.deepcopy(source)
        source_temp.transform(transformation)

        return (source_temp)

    def __pypcd_registration(self, source, target, number_of_iterations):
        #not usefull. not using

        transformation = self.__run_icp_with_pycpd(source, target, number_of_iterations)
        source_temp = copy.deepcopy(source)
        source_temp.transform(transformation)

        return (source_temp)

    def __manual_registration(self, source, target):
        #not usefull. not using. could be the next best thing to do.

        picked_id_source = bed_pc_corners #ACCORDING TO t

        picked_id_target = self.__pick_points(target)
        #picked_id_target = old_bed_corners
        print(picked_id_target)

        assert(len(picked_id_source)>=3 and len(picked_id_target)>=3)
        assert(len(picked_id_source) == len(picked_id_target))
        corr = np.zeros((len(picked_id_source),2))
        corr[:,0] = picked_id_source
        corr[:,1] = picked_id_target

        # estimate rough transformation using correspondences
        p2p = TransformationEstimationPointToPoint()
        trans_init = p2p.compute_transformation(source, target,
                Vector2iVector(corr))

        # point-to-point ICP for refinement
        threshold = 0.03 # 3cm distance threshold
        reg_p2p = registration_icp(source, target, threshold, trans_init,
                TransformationEstimationPointToPoint())

        source_temp = copy.deepcopy(source)
        source_temp.transform(reg_p2p.transformation)

        return (source_temp)

    def __run_icp_with_pycpd(self, source, target, iterations):
        #not usefull. not using.

        iterations = 100

        X = helper.make_pc_ready_for_pycpd(source, downsample = 10)
        Y = helper.make_pc_ready_for_pycpd(target, downsample = 1)

        T = np.zeros((4, 4))
        reg = rigid_registration(**{ 'X': Y, 'Y': X })
        reg.max_iterations = iterations

        reg.register()

        T[0:3, 0:3] = reg.R
        T[3,3] = 1
        T[0:3, 3] = np.transpose(reg.t)

        return T

    def __change_color(self, object, color):
        object_tmp = copy.deepcopy(object)
        object_tmp.paint_uniform_color(color)

        return object_tmp

    def __find_all_objects(self):

        l = defaultdict(list)
        i = 0
        for color in self.labeld_pointcloud.colors:
            l[self.ــget_object_hash_by_label_color(color)].append(i)
            i += 1

        self.objects_dictionary_by_color = l

    def ــget_object_hash_by_label_color(self, color):

        hashed_color = str(color[0]) + '-' + str(color[1]) + '-' + str(color[2])
        return hashed_color

    def __pick_points(self, pcd):
        #only needed when using __manul_registration

        print("")
        print("1) Please pick at least three correspondences using [shift + left click]")
        print("   Press [shift + right click] to undo point picking")
        print("2) Afther picking points, press q for close the window")

        vis = VisualizerWithEditing()
        vis.create_window()
        vis.add_geometry(pcd)
        vis.run()
        vis.destroy_window()

        return vis.get_picked_points()


if __name__ == "__main__":

    r = read_point_cloud(reconstructed_scene)
    l = read_point_cloud(segmented_reconstructed_scene)

    t = Augmentor(r, l)

    new_object, scene_without_old_object = t.change_object('bed')
    show_pcd([new_object, scene_without_old_object])
