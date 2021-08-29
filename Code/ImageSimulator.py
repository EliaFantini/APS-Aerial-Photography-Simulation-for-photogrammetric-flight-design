import math
import os

import cv2
import numpy as np
import numpy.testing
import rasterio as rs
from rasterio.warp import reproject
from scipy.interpolate import griddata


class ImageSimulator:
    def __init__(self, orthophoto_path, dem_path, projection_centers_path, save_folder_path, dem_resampling_method,
                 image_resampling_method,
                 sensor_width, sensor_height, x_pix_num, y_pix_num, x_pc_offset, y_pc_offset, focal_length,
                 progress_signal, color_signal):
        '''
        instantiates the class and saves passed values.  It executes reprojection of the dem's pixel  to orthophoto's
        pixel. It creates a new temporary tif file and saves the result in it. It then counts the number of images to
        be simulated to calculate the increment of the progress bar for each image simulation finished. All length
        parameters are expressed in meters (sensor_width, sensor_height, x_pc_offset, y_pc_offset, focal_length).
        x_pix_num and y_pix_num are expressed in pixel.
        '''
        self.progress_signal = progress_signal
        self.color_signal = color_signal
        self.save_folder_path = save_folder_path
        self.dem_resampling_method = dem_resampling_method
        self.image_resampling_method = image_resampling_method
        self.ortho = rs.open(orthophoto_path)
        dem_to_reproject = rs.open(dem_path, 'r+')
        self.dem_generated_path = self.reprojection(dem_to_reproject)
        self.dem = rs.open(self.dem_generated_path)
        dem_to_reproject.close()
        self.min_height = self.dem.read(1, masked=True).min()
        self.sensor_width = sensor_width
        self.sensor_height = sensor_height
        self.x_pix_num = x_pix_num
        self.y_pix_num = y_pix_num
        self.pix_width = self.sensor_width / self.x_pix_num
        self.pix_height = self.sensor_height / self.y_pix_num
        self.x_pc_offset = x_pc_offset
        self.y_pc_offset = y_pc_offset
        self.focal_length = focal_length
        lines_file = open(projection_centers_path, 'r')
        counter = 0
        for cam_parameters in lines_file:
            if cam_parameters[0] == '#' in cam_parameters:
                continue
            counter += 1
        self.progress_increment_per_photo = 100 / counter
        self.progress = 0
        self.image_counter = 0
        lines_file.close()
        self.projection_centers = open(projection_centers_path, 'r')

    def start(self):
        '''
                for each image to be simulated it reads and saves the projection center parameters from the given file
                and, if needed, it calculates direction cosine. Then, using collinearity equations, it calculates the
                area of pixels to be processed and calls the specific functions to iterate on it, creating a new numpy
                ndarray initially full of zeros, then filled and resampled. After having processed and saved the image,
                the progress signal of a single completed simulation  is issued. In the end, it removes the temporary
                generated reprojection's dem file and issues the 100% progress signal.
        '''
        for cam_parameters in self.projection_centers:
            if cam_parameters[0] == '#' in cam_parameters:  # Skip initial lines of comments starting with '#' char
                continue
            params = cam_parameters.split('\t')
            for x in range(1, len(params)):
                params[x] = float(params[x])
            self.output_file_name = params[0]
            self.x_pc = params[1]
            self.y_pc = params[2]
            self.z_pc = params[3]
            omega_cp = math.radians(params[4])
            phi_cp = math.radians(params[5])
            kappa_cp = math.radians(params[6])
            if len(params) > 7:
                self.r11 = params[7]
                self.r12 = params[8]
                self.r13 = params[9]
                self.r21 = params[10]
                self.r22 = params[11]
                self.r23 = params[12]
                self.r31 = params[13]
                self.r32 = params[14]
                self.r33 = params[15]
            else:
                self.r11 = math.cos(phi_cp) * math.cos(kappa_cp)
                self.r12 = math.cos(omega_cp) * math.sin(kappa_cp) + math.sin(omega_cp) * math.sin(phi_cp) * math.cos(
                    kappa_cp)
                self.r13 = math.sin(omega_cp) * math.sin(kappa_cp) - math.cos(omega_cp) * math.sin(phi_cp) * math.cos(
                    kappa_cp)
                self.r21 = -math.cos(omega_cp) * math.sin(kappa_cp)
                self.r22 = math.cos(omega_cp) * math.cos(kappa_cp) - math.sin(omega_cp) * math.sin(phi_cp) * math.sin(
                    kappa_cp)
                self.r23 = math.sin(omega_cp) * math.cos(kappa_cp) + math.cos(omega_cp) * math.sin(phi_cp) * math.sin(
                    kappa_cp)
                self.r31 = math.sin(phi_cp)
                self.r32 = -math.sin(omega_cp) * math.cos(phi_cp)
                self.r33 = math.cos(omega_cp) * math.cos(phi_cp)
            tl = self.collinearity_equations_z_fixed(-self.pix_width * (self.x_pix_num / 2),
                                                     self.pix_height * (self.y_pix_num / 2))
            tr = self.collinearity_equations_z_fixed(self.pix_width * (self.x_pix_num / 2 - 1),
                                                     self.pix_height * (self.y_pix_num / 2))
            bl = self.collinearity_equations_z_fixed(-self.pix_width * (self.x_pix_num / 2),
                                                     -self.pix_height * (self.y_pix_num / 2 - 1))
            br = self.collinearity_equations_z_fixed(self.pix_width * (self.x_pix_num / 2 - 1),
                                                     -self.pix_height * (self.y_pix_num / 2 - 1))
            tl_to_pixel = self.dem.index(tl[0], tl[1])
            tr_to_pixel = self.dem.index(tr[0], tr[1])
            bl_to_pixel = self.dem.index(bl[0], bl[1])
            br_to_pixel = self.dem.index(br[0], br[1])
            to_elaborate_points_mask = np.zeros(self.ortho.shape, dtype=np.uint8)
            pts = np.array([[(tl_to_pixel[1], tl_to_pixel[0]), (tr_to_pixel[1], tr_to_pixel[0]),
                             (br_to_pixel[1], br_to_pixel[0]), (bl_to_pixel[1], bl_to_pixel[0])]], dtype=np.int32)
            cv2.fillPoly(to_elaborate_points_mask, pts, 255)  # Remove this line for high omega and phi values ( > 30
            # for example), or for really high pc_offset (x or y), major than half the size of the sensor
            pixel_values = numpy.nonzero(to_elaborate_points_mask)
            simulated_photo = np.zeros((self.y_pix_num, self.x_pix_num, 3), np.uint8)
            simulated_photo = self.simulate_photo(pixel_values, simulated_photo)
            simulated_photo = self.interpolate(simulated_photo, self.image_resampling_method)
            simulated_photo = simulated_photo.astype(np.uint8)
            self.save_photo(simulated_photo)
            self.image_counter += 1
            self.progress = int(self.progress_increment_per_photo * self.image_counter)
            self.progress_signal.emit(self.progress)
            self.color_signal.emit()
        self.dem.close()
        os.remove(self.dem_generated_path)
        self.progress_signal.emit(100)

    def save_photo(self, simulated_photo):
        '''
                it creates a new tif file, filled with the processed values, then saves it in the save folder's path
                provided.
        '''
        kwargs = self.ortho.meta.copy()
        kwargs.update({
            'count': 3,
            'width': self.x_pix_num,
            'height': self.y_pix_num
        })
        tif_simulated = rs.open(self.save_folder_path + self.output_file_name + '.tif', 'w', **kwargs)
        tif_simulated.write(simulated_photo[:, :, 0], 1)
        tif_simulated.write(simulated_photo[:, :, 1], 2)
        tif_simulated.write(simulated_photo[:, :, 2], 3)
        tif_simulated.close()

    def interpolate(self, simulated_photo, resampling_method):
        '''
                it creates a mask of all black pixels (missing data from original orthophoto file) and calls an
                interpolation function on them.
        '''
        non_zero_mask = np.zeros((simulated_photo.shape[0], simulated_photo.shape[1]), dtype="uint8")
        non_zero_mask[np.where((simulated_photo != [0, 0, 0]).all(axis=2))] = 255
        non_zero = np.nonzero(non_zero_mask)
        # A meshgrid of pixel coordinates
        nx, ny = simulated_photo.shape[1], simulated_photo.shape[0]
        X, Y = np.meshgrid(np.arange(0, nx, 1), np.arange(0, ny, 1))
        samples = simulated_photo[non_zero[0], non_zero[1]]
        if non_zero[0].size != 0:
            return griddata(non_zero, samples, (Y, X), method=resampling_method)  # 'linear’, ‘nearest’, ‘cubic’
        else:
            return simulated_photo

    def simulate_photo(self, pixel_values, simulated_photo):
        '''
                for each pixel in the area to be processed (pixel_values), it finds the 3-dimensional
                coordinates of the pixel in the orthophoto's reference system. Then, applying collinearity equations, it
                calculates the corresponding 2-dimensional coordinates in the camera's reference system. Finally, it
                calculates the related pixel coordinates and substitutes the pixel values with the ones taken from
                the orthophoto. If more orthophoto pixel map to the same image's pixel, only the one with the minor
                3-dimensional euclidean distance between the orthophoto point and the camera center is taken.
                Each 500000 pixels processed a new progress signal is issued, incrementing the progress' value properly,
                as a calculated fraction of the total progress increment each photo simulation gives to the completion
                of the algorithm.
        '''
        r_matrix = self.ortho.read(1)
        g_matrix = self.ortho.read(2)
        b_matrix = self.ortho.read(3)
        dem_z_matrix = self.dem.read(1)
        distances = np.zeros((self.y_pix_num, self.x_pix_num, 1), np.uint8)
        if pixel_values[0].size != 0:
            unitary_increment = self.progress_increment_per_photo // (pixel_values[0].size / 500000)
        else:
            unitary_increment = 1
        for i in range(pixel_values[0].size):
            if i != 0 and i % 500000 == 0:
                self.progress = self.progress + unitary_increment
                self.progress_signal.emit(self.progress)
            x, y = self.ortho.xy(pixel_values[0][i],
                                 pixel_values[1][i])
            z = dem_z_matrix[pixel_values[0][i]][pixel_values[1][i]]
            x1 = (-self.focal_length * (
                    (self.r11 * (x - self.x_pc) + self.r12 * (y - self.y_pc) + self.r13 * (z - self.z_pc)) / (
                    self.r31 * (x - self.x_pc) + self.r32 * (y - self.y_pc) + self.r33 * (z - self.z_pc))))
            y1 = (-self.focal_length * (
                    (self.r21 * (x - self.x_pc) + self.r22 * (y - self.y_pc) + self.r23 * (z - self.z_pc)) / (
                    self.r31 * (x - self.x_pc) + self.r32 * (y - self.y_pc) + self.r33 * (z - self.z_pc))))
            x_pix_value = int((((self.x_pix_num / 2) * self.pix_width + self.x_pc_offset) + x1) / self.pix_width)
            y_pix_value = int((((self.y_pix_num / 2) * self.pix_height - self.y_pc_offset) - y1) / self.pix_height)
            if 0 <= x_pix_value <= (self.x_pix_num - 1):
                if 0 <= y_pix_value <= (self.y_pix_num - 1):
                    pc_distance = math.sqrt(
                        math.pow((x - self.x_pc), 2) + math.pow((y - self.y_pc), 2) + math.pow(z - self.z_pc, 2))
                    if simulated_photo[y_pix_value, x_pix_value, 0] != 0 and pc_distance > distances[
                        y_pix_value, x_pix_value, 0]:
                        continue
                    simulated_photo[y_pix_value, x_pix_value, 0] = r_matrix[pixel_values[0][i]][pixel_values[1][i]]
                    simulated_photo[y_pix_value, x_pix_value, 1] = g_matrix[pixel_values[0][i]][pixel_values[1][i]]
                    simulated_photo[y_pix_value, x_pix_value, 2] = b_matrix[pixel_values[0][i]][pixel_values[1][i]]
                    distances[y_pix_value, x_pix_value, 0] = pc_distance
        return simulated_photo

    def collinearity_equations_z_fixed(self, x, y):
        '''
            applying collinearity equations, it goes from the 2-dimensional x,y coordinates of the camera's reference
            system to the corresponding 3-dimensional coordinates of the same point in the othophoto's reference system.
            Since z is fixed to the minimum height value found in the dem, only x_out and y_out are calculated
            (resolving a 2 equations system with 2 variables).
        '''
        x_out = self.x_pc + (self.min_height - self.z_pc) * ((
                                                                     self.r11 * (
                                                                     x + self.pix_width / 2 + self.x_pc_offset) + self.r21 * (
                                                                             y - self.pix_height / 2 + self.y_pc_offset) + self.r31 * self.focal_length) / (
                                                                     self.r13 * (
                                                                     x + self.pix_width / 2 + self.x_pc_offset) + self.r23 * (
                                                                             y - self.pix_height / 2 + self.y_pc_offset) + self.r33 * self.focal_length))
        y_out = self.y_pc + (self.min_height - self.z_pc) * ((
                                                                     self.r12 * (
                                                                     x + self.pix_width / 2 + self.x_pc_offset) + self.r22 * (
                                                                             y - self.pix_height / 2 + self.y_pc_offset) + self.r32 * self.focal_length) / (
                                                                     self.r13 * (
                                                                     x + self.pix_width / 2 + self.x_pc_offset) + self.r23 * (
                                                                             y - self.pix_height / 2 + self.y_pc_offset) + self.r33 * self.focal_length))
        return [x_out, y_out]

    def reprojection(self, dem_to_reproject):
        '''
            it maps the pixels of orthophoto raster with its associated coordinate reference system and
            transform to the pixels of dem raster with its different coordinate reference system and transform. This
            process is known as reprojection.
        '''
        kwargs = self.ortho.meta.copy()
        kwargs.update({
            'count': 1,
            'dtype': dem_to_reproject.dtypes[0],
            'nodata': dem_to_reproject.nodata
        })
        with rs.open(self.save_folder_path + 'reprojection_dem.tif', 'w', **kwargs) as dst:
            reproject(
                source=rs.band(dem_to_reproject, 1),
                destination=rs.band(dst, 1),
                src_transform=dem_to_reproject.transform,
                src_crs=dem_to_reproject.crs,
                src_nodata=dem_to_reproject.nodata,
                dst_transform=dst.transform,
                dst_crs=dst.crs,
                dest_nodata=dst.nodata,
                resampling=self.dem_resampling_method)
        return self.save_folder_path + 'reprojection_dem.tif'


if __name__ == '__main__':
    pass
    # for debugging only
    # path = ""
    # image_simulator = ImageSimulator(path + 'ortho.tif', path + 'dem.tif',
    #       path + 'Test/Focal_length_test/focal_length_test_1.txt',
    #        path + 'Test/Focal_length_test/', Resampling.nearest, 'nearest', 36 / 1000,
    #       24 / 1000, 3456, 2304, 0.0, 0.0,
    #       50 / 1000, None, None)
    # image_simulator.start()
