import numpy as np
import random
from tMap import Resort_Map
from genetic import gen_algoth

gen = gen_algoth()
out =  gen.rand_map()

print(out.trail_set)
print(np.array(out.chair_set))
