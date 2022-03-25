import meep as mp
import numpy as np
from matplotlib import pyplot as plt

sz = 100              # size of cell in z direction
fcen = 1 / 3.0        # center frequency of source
df = fcen / 20.0      # frequency width of source
amp = 1               # amplitude of source
k = 10**-5            # Kerr susceptibility
dpml = 1.0            # PML thickness

dimensions = 1
cell = mp.Vector3(0, 0, sz)
pml_layers = mp.PML(dpml)
resolution = 20

default_material = mp.Medium(index=1, chi3=k)

sources = mp.Source(mp.GaussianSource(fcen, fwidth=df), component=mp.Ex,
                    center=mp.Vector3(0, 0, -0.5*sz + dpml), amplitude=amp)

nfreq = 400
fmin = fcen / 2.0
fmax = fcen * 4

sim = mp.Simulation(cell_size=cell,
                    geometry=[],
                    sources=[sources],
                    boundary_layers=[pml_layers],
                    default_material=default_material,
                    resolution=resolution,
                    dimensions=dimensions)

trans = sim.add_flux(0.5 * (fmin + fmax), fmax - fmin, nfreq,
                     mp.FluxRegion(mp.Vector3(0, 0, 0.5*sz - dpml - 0.5)))

sim.run(until_after_sources=mp.stop_when_fields_decayed(
        50, mp.Ex, mp.Vector3(0, 0, 0.5*sz - dpml - 0.5), 1e-6))

freqs = mp.get_flux_freqs(trans)
spectra = mp.get_fluxes(trans)

plt.figure(dpi=150)
plt.semilogy(freqs,spectra)
plt.grid(True)
plt.xlabel('Frequency')
plt.ylabel('Transmitted Power (a.u.)')
plt.show()