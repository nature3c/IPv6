import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("country-counts.csv")
df.columns = ["Country", "Count"]

world = gpd.read_file("world_data/ne_110m_admin_0_countries.shp")

world = world.merge(df, how="left", left_on="ISO_A2", right_on="Country")

# Fill missing data with 0 (unaffected countries)
world["Count"] = world["Count"].fillna(0)

# Apply log scale to affected countries
world["LogCount"] = np.log1p(world["Count"])  # log(Count + 1) to handle zeros safely

# Split affected and unaffected for custom coloring
affected = world[world["Count"] > 0]
unaffected = world[world["Count"] == 0]

fig, ax = plt.subplots(figsize=(12, 8))

# Plot unaffected countries as white
unaffected.plot(color="white", edgecolor="gray", ax=ax)

# Plot affected countries with log scaled gradient
affected.plot(column="LogCount", cmap="Reds", linewidth=0.8, edgecolor="black",
              legend=True,
              legend_kwds={"label": "Log(IP Counts) by Country"},
              ax=ax)

ax.set_title("Log Scaled IP Counts by Country", fontsize=14)
ax.axis("off")

plt.savefig("asn_choropleth_logscale.png", dpi=300)
plt.show()
