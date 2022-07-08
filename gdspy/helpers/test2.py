from gdshelpers.geometry.chip import Cell
from gdshelpers.parts.waveguide import Waveguide
from gdshelpers.parts import Port
from gdshelpers.parts.splitter import DirectionalCoupler
from shapely.geometry import Polygon 

waveguide_1 = Waveguide.make_at_port(port=Port((0, 0), angle=0, width=1.3))
waveguide_2 = Waveguide.make_at_port(port=Port((0, 5), angle=0, width=1.3))

#waveguide_1.add_straight_segment(length=0)

DC = DirectionalCoupler.make_at_port(port=waveguide_1.current_port, length=30, gap=0.5, bend_radius=30, which=0)
DC1 = DirectionalCoupler.make_at_port(port=waveguide_2.current_port, length=30, gap=0.5, bend_radius=30, which=0)
#waveguide_2 = Waveguide.make_at_port(DC.right_ports[1])
#waveguide_2.add_straight_segment(length=0)

cell = Cell('CELL')
cell.add_to_layer(1, waveguide_1, DC)
cell.add_to_layer(2, waveguide_2, DC1)
cell.save("DC1.gds")
cell.show()