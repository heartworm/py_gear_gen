import matplotlib.pyplot as plt
from involute_gear import InvoluteGear
from mathutils import *

gear_args = {
    'fillet': 0.2,
    'backlash': 0.3,
    'module': 3,
}

gear = InvoluteGear(teeth=30, **gear_args)
gear2 = InvoluteGear(teeth=10, **gear_args)
gear3 = InvoluteGear(teeth=50, ring=True, **gear_args)

points_gear = np.dot(rotation_matrix(gear.theta_tooth_and_gap / 2), gear.generate_gear())
points_gear2 = gear2.generate_gear()
points_gear3 = gear3.generate_gear()

gear.get_svg().saveas('planet.svg')
gear2.get_svg().saveas('sun.svg')
gear3.get_svg().saveas('ring.svg')

plt.plot(points_gear[0,:], points_gear[1,:])
plt.plot(points_gear2[0,:] + (gear.pitch_radius + gear2.pitch_radius), points_gear2[1,:])
plt.plot(points_gear3[0,:], points_gear3[1,:])

plt.axis('equal')
plt.grid(True)
plt.show()
