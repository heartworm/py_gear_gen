import numpy as np
from math import *
from mathutils import *
import sys
from svgwrite.path import Path
from svgwrite.mixins import ViewBox
from svgwrite import mm, Drawing
from dxfwrite import DXFEngine as dxf


class DimensionException(Exception):
    pass

class InvoluteGear:
    def __init__(self, module=1, teeth=30, pressure_angle_deg=20, clearance=0, fillet=0, backlash=0,
                 max_steps=50):

        pressure_angle = radians(pressure_angle_deg)
        self.module = module
        self.teeth = teeth
        self.pressure_angle = pressure_angle
        self.addendum = module
        self.dedendum = 1.157 * module

        self.clearance = clearance

        self.backlash = backlash


        self.pitch_radius = (module * teeth) / 2
        self.base_radius = cos(pressure_angle) * self.pitch_radius
        self.fillet_radius = fillet
        self.outer_radius = self.pitch_radius + self.addendum
        self.root_radius = self.pitch_radius - self.dedendum

        self.theta_pitch = pi * 2 / teeth
        self.theta_tooth = self.theta_pitch / 2 - (backlash / 2 / self.pitch_radius)
        self.max_steps = max_steps

        self.root_arc_length = (self.theta_pitch - self.theta_tooth) * self.root_radius

    def generate_half_tooth(self):

        phis = np.linspace(0, pi, self.max_steps)
        points_half = []

        reached_limit = False

        self.theta_pitch_intersect = None

        for phi in phis:
            x = (self.base_radius * cos(phi)) + (phi * self.base_radius * sin(phi))
            y = (self.base_radius * sin(phi)) - (phi * self.base_radius * cos(phi))
            dist = sqrt(x * x + y * y)
            theta = atan2(y, x)

            point = (x, y)


            reached_pitch = dist > self.base_radius

            reached_edge = dist >= self.outer_radius
            under_root = dist <= self.root_radius

            if self.theta_pitch_intersect is None and dist >= self.pitch_radius:
                self.theta_pitch_intersect = theta
            elif self.theta_pitch_intersect is not None and (theta) >= self.theta_pitch_intersect + self.theta_tooth / 2:
                reached_limit = True
                break

            if reached_edge:
                points_half.append(polar_to_cart((self.outer_radius, theta)))
            elif under_root:
                points_half.append(polar_to_cart((self.root_radius, theta)))
            else:
                points_half.append(point)

        if not reached_limit:
            raise Exception("Couldn't complete tooth profile ")

        return np.transpose(points_half)

    def generate_root(self, n_points):
        points_root = []
        for theta in np.linspace(self.theta_tooth + self.theta_pitch_intersect * 2, self.theta_pitch, n_points):
            theta_arc_length = (theta - self.theta_tooth) * self.root_radius
            first_fillet = theta_arc_length < self.fillet_radius
            second_fillet = (self.root_arc_length - theta_arc_length) < self.fillet_radius
            r = self.root_radius
            if first_fillet or second_fillet:
                circle_pos = min(theta_arc_length, (self.root_arc_length - theta_arc_length))
                r = r + (self.fillet_radius - sqrt(pow(self.fillet_radius, 2) - pow(self.fillet_radius - circle_pos, 2)))

            points_root.append(polar_to_cart((r, theta)))
        return np.transpose(points_root)

    def generate_tooth(self):
        points_first_half = self.generate_half_tooth()
        points_second_half = np.dot(rotation_matrix(self.theta_tooth + self.theta_pitch_intersect * 2), np.dot(flip_matrix(False, True), points_first_half))
        points_second_half = np.flip(points_second_half, 1)

        return np.concatenate((points_first_half, points_second_half), axis=1)

    def generate_module(self):
        points_tooth = self.generate_tooth()
        n_points_tooth = np.shape(points_tooth)[1]
        points_root = self.generate_root(n_points_tooth)
        points_module = np.concatenate((points_tooth, points_root), axis=1)
        return points_module

    def generate_gear(self):
        points_module = self.generate_module()
        points_teeth = [np.dot(rotation_matrix(self.theta_pitch * n), points_module) for n in range(self.teeth)]
        points_gear = np.concatenate(points_teeth, axis=1)
        return points_gear

    def get_point_list(self):
        gear = self.generate_gear()
        return np.transpose(gear)

    def get_svg(self, unit=mm):
        points = self.get_point_list()

        width, height = np.ptp(points, axis=0)

        left, top = np.min(points, axis=0)

        size = (width*unit, height*unit) if unit is not None else (width,height)

        dwg = Drawing(size=size, viewBox='{} {} {} {}'.format(left,top,width,height))

        p = Path('M')
        p.push(points)
        p.push('Z')

        dwg.add(p)

        return dwg



def error_out(s, *args):
    sys.stderr.write(s + "\n")