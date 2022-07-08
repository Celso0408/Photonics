from gdshelpers.geometry.chip import Cell
from gdshelpers.parts.waveguide import Waveguide
from gdshelpers.parts import Port

# standard python imports
import numpy as np
import matplotlib.pyplot as plt
import gdspy
import os

### Length scale in micron.

# Waveguide width
wg_width = 0.45
# Waveguide separation in the beginning/end
wg_spacing_in = 8
# Length of the coupling region
coup_length = 10
# Length of the bend region
bend_length = 16
# Waveguide separation in the coupling region
wg_spacing_coup = 0.10
# Total device length along propagation direction
device_length = 100

def bend_pts(bend_length, width, npts=10):
    """ Set of points describing a tanh bend from (0, 0) to (length, width)"""
    x = np.linspace(0, bend_length, npts)
    y = width*(1 + np.tanh(6*(x/bend_length - 0.5)))/2
    return np.stack((x, y), axis=1)

def arm_pts(length, width, coup_length, bend_length, npts_bend=30):
    """ Set of points defining one arm of an integrated coupler """
    ### Make the right half of the coupler arm first
    # Make bend and offset by coup_length/2
    bend = bend_pts(bend_length, width, npts_bend)
    bend[:, 0] += coup_length / 2
    # Add starting point as (0, 0)
    right_half = np.concatenate(([[0, 0]], bend))
    # Add an extra point to make sure waveguide is straight past the bend
    right_half = np.concatenate((right_half, [[right_half[-1, 0] + 0.1, width]]))
    # Add end point as (length/2, width)
    right_half = np.concatenate((right_half, [[length/2, width]]))

    ### Make the left half by reflecting and omitting the (0, 0) point
    left_half = np.copy(right_half)[1:, :]
    left_half[:, 0] = -left_half[::-1, 0]
    left_half[:, 1] = left_half[::-1, 1]
    
    return np.concatenate((left_half, right_half), axis=0)

# Plot the upper arm for the current configuration
arm_center_coords = arm_pts(
    device_length,
    wg_spacing_in/2,
    coup_length,
    bend_length)

# fig, ax = plt.subplots(1, figsize=(8, 3))
# ax.plot(arm_center_coords[:, 0], arm_center_coords[:, 1], lw=4)
# ax.set_xlim([-30, 30])
# ax.set_xlabel("x (um)")
# ax.set_ylabel("y (um)")
# ax.set_title("Upper beam splitter arm")
# ax.axes.set_aspect('equal')
# plt.show()

gdspy.current_library = gdspy.GdsLibrary()
lib = gdspy.GdsLibrary()

# Geometry must be placed in GDS cells to import into Tidy3D
coup_cell = lib.new_cell('Coupler')

substrate = gdspy.Rectangle(
    (-device_length/2, -wg_spacing_in/2-10),
    (device_length/2, wg_spacing_in/2+10),
    layer=0)
coup_cell.add(substrate)

def make_coupler(
    length, 
    wg_spacing_in,
    wg_width,
    wg_spacing_coup,
    coup_length,
    bend_length,
    npts_bend=30):
    """ Make an integrated coupler using the gdspy FlexPath object. """
    # Compute one arm of the coupler
    arm_width = (wg_spacing_in - wg_width - wg_spacing_coup)/2
    arm = arm_pts(length, arm_width, coup_length, bend_length, npts_bend)
    # Reflect and offset bottom arm
    coup_bot = np.copy(arm)
    coup_bot[:, 1] = -coup_bot[::-1, 1] - wg_width/2 - wg_spacing_coup/2
    # Offset top arm
    coup_top = np.copy(arm)
    coup_top[:, 1] += wg_width/2 + wg_spacing_coup/2
    
    # Create waveguides as GDS paths
    path_top = gdspy.FlexPath(coup_top, wg_width, layer=31, datatype=0)
    path_bot = gdspy.FlexPath(coup_bot, wg_width, layer=32, datatype=0)
    
    
    return [path_bot, path_top]

# Add the coupler to a gdspy cell
c1 = gdspy.Curve(-42, 7).V(0.1, 0)
p1 = gdspy.Polygon(c1.get_points(),layer=1, datatype=0)

c2 = gdspy.Curve(-45, 7).V(0.1, 0)
p2 = gdspy.Polygon(c2.get_points(),layer=5, datatype=0)

c3 = gdspy.Curve(-42, -7).V(0.1, 0)
p3 = gdspy.Polygon(c3.get_points(),layer=2, datatype=0)

c4 = gdspy.Curve(45, 7).V(0.1, 0)
p4 = gdspy.Polygon(c4.get_points(),layer=3, datatype=0)

c5 = gdspy.Curve(45, -7).V(0.1, 0)
p5 = gdspy.Polygon(c5.get_points(),layer=4, datatype=0)

gds_coup = make_coupler(
    device_length,
    wg_spacing_in,
    wg_width,
    wg_spacing_coup,
    coup_length,
    bend_length)

coup_cell.add(gds_coup);

coup_cell.add(p1);

coup_cell.add(p2);

coup_cell.add(p3);

coup_cell.add(p4);

coup_cell.add(p5);

# Uncomment to display the cell using the internal gdspy viewer
gdspy.LayoutViewer(lib)

os.makedirs('data', exist_ok=True)
lib.write_gds('data/coupler.gds')