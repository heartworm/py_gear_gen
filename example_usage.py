import matplotlib.pyplot as plt
from involute_gear import InvoluteGear
from mathutils import *

gear = InvoluteGear(teeth=30, module=3, pressure_angle_deg=20, max_steps=100)
dwg = gear.get_svg()
dwg.saveas('output.svg')


gear2 = InvoluteGear(teeth=10, module=3, pressure_angle_deg=20, max_steps=100)

points_gear = gear.generate_gear()

points_gear2 = gear2.generate_gear()
points_gear2 = np.dot(rotation_matrix(-2*gear2.theta_pitch_intersect), points_gear2)


plt.figure()
ax = plt.gca()
ax.add_artist(plt.Circle((0,0), gear.outer_radius, fill=False))
ax.add_artist(plt.Circle((0,0), gear.root_radius, fill=False))
ax.add_artist(plt.Circle((0,0), gear.base_radius, fill=False))
ax.add_artist(plt.Circle((0,0), gear.pitch_radius, fill=False))
plt.plot(points_gear[0,:], points_gear[1,:])
plt.plot(points_gear2[0,:] + (gear.pitch_radius + gear2.pitch_radius), points_gear2[1,:])
line_end = polar_to_cart((gear.outer_radius, gear.theta_pitch_intersect + gear.theta_tooth / 2))
plt.plot([0, line_end[0]], [0, line_end[1]])
plt.axis('equal')
plt.grid(True)
plt.show()