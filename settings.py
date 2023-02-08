# DO DONT TOUCH
import funcs as fn

# ==== Settings

# Default sql query in the box
DEFAULT_CMD =  """ /* Example SQL Command */ 
SELECT TREE.INVYR, TREE.TREE, PLOT.PLOT, TREE.SUBP, TREE.DIA, PLOT.LAT, PLOT.LON
FROM TREE
INNER JOIN PLOT ON TREE.PLT_CN=PLOT.CN """

# the deafult output dir (or make dir)
DEFAULT_OUTPUT_DIR = fn.default_output()
DATAMART_URL = "https://experience.arcgis.com/experience/3641cea45d614ab88791aef54f3a1849/"