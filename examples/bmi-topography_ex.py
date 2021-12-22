"""An example used in the README and documentation."""
import matplotlib.pyplot as plt

from bmi_topography import Topography

params = Topography.DEFAULT.copy()
params["south"] = 39.93
params["north"] = 40.00
params["west"] = -105.33
params["east"] = -105.26

boulder = Topography(**params)

boulder.fetch()
boulder.load()

boulder.da.plot()
plt.show()
