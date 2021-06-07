import rpy2
#import rpy2.robjects as robjects

#from functools import partial
#from rpy2.ipython import html
#from rpy2.robjects.packages import importr


from rpy2.robjects.packages import importr
# import R's "base" package
base = importr('base')

# import R's "utils" package
utils = importr('utils')