"""An example used in the README and documentation."""
import matplotlib.pyplot as plt
from bmi_topography import Topography


params = Topography.DEFAULT.copy()
params["south"] = 39.75
params["north"] = 40.25
params["west"] = -105.25
params["east"] = -104.75

boulder = Topography(**params)

boulder.fetch()
boulder.load()

boulder.dataarray.plot()
plt.show()
