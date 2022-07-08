import numpy as np

from math import pi
from gdshelpers.geometry.chip import Cell
from gdshelpers.parts.waveguide import Waveguide
from gdshelpers.parts.coupler import GratingCoupler
from gdshelpers.parts.resonator import RingResonator
from gdshelpers.layout import GridLayout
from gdshelpers.parts.marker import SquareMarker
from gdshelpers.geometry.ebl_frame_generators import raith_marker_frame

coupler_params = {
    'width': 1.3,
    'full_opening_angle': np.deg2rad(40),
    'grating_period': 1.155,
    'grating_ff': 0.85,
    'n_gratings': 20,
    'taper_length': 16.
}

def generate_device_cell(resonator_radius, resonator_gap, origin=(25, 75)):
    left_coupler = GratingCoupler.make_traditional_coupler(origin, **coupler_params)
    wg1 = Waveguide.make_at_port(left_coupler.port)
    wg1.add_straight_segment(length=10)
    wg1.add_bend(-pi / 2, radius=50)
    wg1.add_straight_segment(length=75)

    ring_res = RingResonator.make_at_port(wg1.current_port, gap=resonator_gap, radius=resonator_radius)

    wg2 = Waveguide.make_at_port(ring_res.port)
    wg2.add_straight_segment(length=75)
    wg2.add_bend(-pi / 2, radius=50)
    wg2.add_straight_segment(length=10)
    right_coupler = GratingCoupler.make_traditional_coupler_at_port(wg2.current_port, **coupler_params)

    cell = Cell('SIMPLE_RES_DEVICE r={:.1f} g={:.1f}'.format(resonator_radius, resonator_gap))
    cell.add_to_layer(1, left_coupler, wg1, ring_res, wg2, right_coupler)
    cell.add_ebl_marker(layer=9, marker=SquareMarker(origin=(0, 0), size=20))
    return cell


layout = GridLayout(title='Simple parameter sweep', frame_layer=0, text_layer=2, region_layer_type=None)
radii = np.linspace(20, 50, 4)
gaps = np.linspace(0.1, 0.5, 5)

# Add column labels
layout.add_column_label_row(('Gap %0.2f' % gap for gap in gaps), row_label='')

for radius in radii:
    layout.begin_new_row('Radius\n%0.2f' % radius)
    for gap in gaps:
        layout.add_to_row(generate_device_cell(radius, gap))

layout_cell, mapping = layout.generate_layout()
layout_cell.add_frame(frame_layer=8, line_width=7)
layout_cell.add_ebl_frame(layer=10, frame_generator=raith_marker_frame, n=2)
layout_cell.show()