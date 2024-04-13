import math
import numpy as np
import sys
import turtle


class celestial_object:

# arguments for constructor:
#   coordinates, [x, y, z] matrix numpy format  |  unit used is meters
#   velocity, [x, y, z] matrix numpy format     |  unit used is meters per second
#   mass, decimal                               |  unit used is kilograms
#   radius, decimal                             |  unit used is meters
#   name, string                                |  unit N/A

    def __init__(self, c, v, m, r, n):
        self.__coordinates = c
        self.__velocity = v
        self.__mass = m
        self.__radius = r
        self.__name = n

    def set_coordinates(self, c):
        self.__coordinates = c

    def set_velocity(self, v):
        self.__velocity = v

    def return_coordinates(self):
        return self.__coordinates

    def return_velocity(self):
        return self.__velocity

    def return_mass(self):
        return self.__mass

    def return_radius(self):
        return self.__radius

    def return_name(self):
        return self.__name
    
    def apply_acceleration(self, a, t):
        self.__velocity = np.add(self.__velocity, np.divide(a, t))
    
    def apply_velocity(self, t):
        self.__coordinates = np.add(self.__coordinates, np.divide(self.__velocity, t))



def calculate_barycenter(celestial_objects):
    total_mass = 0
    barycenter_x = 0
    barycenter_y = 0
    barycenter_z = 0

    # Iterate over each celestial object
    for obj in celestial_objects:
        mass, coordinates = obj.return_mass(), obj.return_coordinates()
        total_mass += mass
        x, y, z = coordinates
        barycenter_x += mass * x
        barycenter_y += mass * y
        barycenter_z += mass * z

    # Calculate the barycenter coordinates
    barycenter_x /= total_mass
    barycenter_y /= total_mass
    barycenter_z /= total_mass

    return np.array([barycenter_x, barycenter_y, barycenter_z])

def round_array(arr, n):
    return np.array([round(val, 4) for val in arr])

def update_barycentric_coordinates_and_velocities(celestial_objects, barycenter):
    for obj in celestial_objects:
        obj.set_coordinates(round_array(np.subtract(obj.return_coordinates(), barycenter), 0))
        obj.set_velocity(round_array(obj.return_velocity(), 0))
    barycenter = np.array([0, 0, 0])

def calculate_acceleration(body_one, body_two):
    u_grav_const = 6.6743E-11 # measured in n * (m^2 / kg^2)
    pos_one = body_one.return_coordinates()
    pos_two = body_two.return_coordinates()
    mass_one = body_one.return_mass()
    mass_two = body_two.return_mass()
    distance = math.sqrt(((pos_one[0]-pos_two[0])**2)+((pos_one[1]-pos_two[1])**2)+((pos_one[2]-pos_two[2])**2)) # measured in m
    displacement_vector = [val2 - val1 for val1, val2 in zip(pos_one, pos_two)] # measured in m
    normalized_displacement_vector = [val / distance for val in displacement_vector] # normalized to unit vector of magnitude 1
    grav_force = u_grav_const*((mass_one * mass_two)/(distance**2)) # measured in n (newtons)
    force_vector = [val * grav_force for val in normalized_displacement_vector] # measured in n (newtons)
    body_one_accel_vector = np.array([((val/mass_one)) for val in force_vector]) # measured in m/s^2
    body_two_accel_vector = np.array([(((val/mass_two)*-1)) for val in force_vector]) # measured in m/s^2
    return body_one_accel_vector, body_two_accel_vector

    """
    temp = [(val1/tps)+val2 for val1, val2 in zip(body_one_accel_vector, body_one.return_velocity())]
    body_one.set_velocity(temp)
    temp = [(val1/tps)+val2 for val1, val2 in zip(body_one.return_velocity(), body_one.return_coordinates())]
    body_one.set_coordinates(temp)
    temp = [(val1/tps)+val2 for val1, val2 in zip(body_two_accel_vector, body_two.return_velocity())]
    body_two.set_velocity(temp)
    temp = [(val1/tps)+val2 for val1, val2 in zip(body_two.return_velocity(), body_two.return_coordinates())]
    body_two.set_coordinates(temp)
    """


def iterate_simulation(celestial_objects, tps):

    celestial_object_pairs = [(x, y) for x in range(len(celestial_objects)) for y in range(x + 1, len(celestial_objects))]

    for i in range(len(celestial_objects)):
        globals()[f"body{i}_cumulative_acceleration"] = np.array([0, 0, 0])
    
    for pair in celestial_object_pairs:
        body_one_accel, body_two_accel = calculate_acceleration(celestial_objects[pair[0]], celestial_objects[pair[1]])
        globals()[f"body{pair[0]}_cumulative_acceleration"] = np.add(body_one_accel, globals()[f"body{pair[0]}_cumulative_acceleration"])
        globals()[f"body{pair[1]}_cumulative_acceleration"] = np.add(body_two_accel, globals()[f"body{pair[1]}_cumulative_acceleration"])

    for i in range(len(celestial_objects)):
        celestial_objects[i].apply_acceleration(globals()[f"body{i}_cumulative_acceleration"], tps)
        celestial_objects[i].apply_velocity(tps)



celestial_objects = [
    sol := celestial_object(
        np.array([-1.191989241021022E+06*1000,-4.347653852987497E+05*1000, 3.146124488303781E+04*1000]),
        np.array([ 8.441015570617839E-03*1000,-1.221912229517152E-02*1000,-7.918736754502012E-05*1000]),
        1.98855E+30,
        695660*1000,
        "Sun"
        ),

    mercurius := celestial_object(
        np.array([-4.226941015560152E+07*1000, 2.954546597148274E+07*1000, 6.249265895718288E+06*1000]),
        np.array([-3.865601391340655E+01*1000,-3.734598383776862E+01*1000, 4.954276669322102E-01*1000]),
        3.3011E+23,
        2439.7*1000,
        "Mercury"
        ),

    venus := celestial_object(
        np.array([-1.081920113224358E+08*1000,-1.187776759100180E+07*1000, 6.048297942710424E+06*1000]),
        np.array([ 3.517776985981810E+00*1000,-3.499021677262173E+01*1000,-6.829385946234794E-01*1000]),
        4.8675E+24,
        6051.8*1000,
        "Venus"
        ),

    terra := celestial_object(
        np.array([-2.598836598098600E+07*1000, 1.445626126553490E+08*1000, 2.324549973998219E+04*1000]),
        np.array([-2.983351607599674E+01*1000,-5.135525753507316E+00*1000, 1.103959339770366E-03*1000]),
        5.9722E+24,
        6371*1000,
        "Earth"
        ),

    luna := celestial_object(
        np.array([-2.635609429981740E+07*1000, 1.447295779421217E+08*1000, 4.845187966158986E+04*1000]),
        np.array([-3.024438898825232E+01*1000,-6.010660216416693E+00*1000,-5.808542579651466E-02*1000]),
        7.342E+22,
        1737.4*1000,
        "Moon (Earth)"
        ),

    mars := celestial_object(
        np.array([-4.509604630809999E+07*1000,-2.175176647934361E+08*1000,-3.441055388979807E+06*1000]),
        np.array([ 2.466995826568801E+01*1000,-2.736343890484162E+00*1000,-6.620925260729528E-01*1000]),
        6.4171E+23,
        3389.5*1000,
        "Mars"
        ),

    iuppiter := celestial_object(
        np.array([ 5.214023950207858E+08*1000, 5.313678519725485E+08*1000,-1.386969717664611E+07*1000]),
        np.array([-9.472330329859803E+00*1000, 9.770254241116218E+00*1000, 1.713410188865314E-01*1000]),
        1.8982E+27,
        69911*1000,
        "Jupiter"
        ),

    saturnus := celestial_object(
        np.array([ 1.344585933043946E+09*1000,-5.564074299488643E+08*1000,-4.385980505864763E+07*1000]),
        np.array([ 3.154994095652995E+00*1000, 8.905566499358839E+00*1000,-2.800166767406997E-01*1000]),
        5.6834E+26,
        58232*1000,
        "Saturn"
        ),

    uranus := celestial_object(
        np.array([ 1.834574778290128E+09*1000, 2.288418091869818E+09*1000,-1.526801948375988E+07*1000]),
        np.array([-5.363307238645053E+00*1000, 3.942270462274153E+00*1000, 8.415494743780227E-02*1000]),
        86.813E+24,
        25362*1000,
        "Uranus"
        ),

    neptunus := celestial_object(
        np.array([ 4.463250326610554E+09*1000,-2.684320184407575E+08*1000,-9.733259894928326E+07*1000]),
        np.array([ 2.903902879855819E-01*1000, 5.457709778431394E+00*1000,-1.190948298321868E-01*1000]),
        102.409E+24,
        24624*1000,
        "Neptune"
        )

]

"""  
# New celestial object template:
    _____ := celestial_object(
        np.array([]),
        np.array([]),
        ,
        *1000,
        ""
        ),
"""


"""
# Starting Variables
solar_barycenter = [0, 0, 0]
starting_time_UNIX = 1704067200000 # UNIX millisecond time for Jan 1st, 2024, 00:00:00





seconds_per_day = 86400
ticks_per_second = 1
ticks = int(seconds_per_day*ticks_per_second)*31

for x in range(ticks):
    iterate_simulation(celestial_objects, ticks_per_second)
    barycenter = calculate_barycenter(celestial_objects)
    update_barycentric_coordinates_and_velocities(celestial_objects, barycenter)
    
    # Calculate percentage finished
    percent_finished = (x + 1) / ticks * 100
    
    # Print percentage finished without newline
    sys.stdout.write(f"\rProgress: {percent_finished:.2f}%")  # \r to go back to the beginning of the line
    sys.stdout.flush()  # Flush the output to ensure it's immediately displayed

print(terra.return_coordinates())
"""






# Initialize turtle
screen = turtle.Screen()
screen.setup(width=800, height=800)
val = 1e12
screen.setworldcoordinates(-val, -val, val, val)  # Adjust this range based on your data
screen.tracer(0)





# Create turtle for each celestial object
bodies = []

sol_turtle = turtle.Turtle()
#body1.penup()
sol_turtle.shape("circle")
sol_turtle.color("yellow")
sol_turtle.pencolor("pink")
sol_turtle.shapesize(1)  # Adjust the size of the dot if needed
bodies.append(sol_turtle)

mercurius_turtle = turtle.Turtle()
#body2.penup()
mercurius_turtle.shape("circle")
mercurius_turtle.color("gray")
mercurius_turtle.pencolor("pink")
mercurius_turtle.shapesize(.2)  # Adjust the size of the dot if needed
bodies.append(mercurius_turtle)

venus_turtle = turtle.Turtle()
#body3.penup()
venus_turtle.shape("circle")
venus_turtle.color("orange")
venus_turtle.pencolor("pink")
venus_turtle.shapesize(.4)  # Adjust the size of the dot if needed
bodies.append(venus_turtle)

terra_turtle = turtle.Turtle()
#body3.penup()
terra_turtle.shape("circle")
terra_turtle.color("green")
terra_turtle.pencolor("pink")
terra_turtle.shapesize(.5)  # Adjust the size of the dot if needed
bodies.append(terra_turtle)

luna_turtle = turtle.Turtle()
#body3.penup()
luna_turtle.shape("circle")
luna_turtle.color("gray")
luna_turtle.pencolor("pink")
luna_turtle.shapesize(.1)  # Adjust the size of the dot if needed
bodies.append(luna_turtle)

mars_turtle = turtle.Turtle()
#body3.penup()
mars_turtle.shape("circle")
mars_turtle.color("red")
mars_turtle.pencolor("pink")
mars_turtle.shapesize(.35)  # Adjust the size of the dot if needed
bodies.append(mars_turtle)

iuppiter_turtle = turtle.Turtle()
#body3.penup()
iuppiter_turtle.shape("circle")
iuppiter_turtle.color("brown")
iuppiter_turtle.pencolor("pink")
iuppiter_turtle.shapesize(.8)  # Adjust the size of the dot if needed
bodies.append(iuppiter_turtle)

saturnus_turtle = turtle.Turtle()
#body3.penup()
saturnus_turtle.shape("circle")
saturnus_turtle.color("blue")
saturnus_turtle.pencolor("pink")
saturnus_turtle.shapesize(.7)  # Adjust the size of the dot if needed
bodies.append(saturnus_turtle)

uranus_turtle = turtle.Turtle()
#body3.penup()
uranus_turtle.shape("circle")
uranus_turtle.color("blue")
uranus_turtle.pencolor("pink")
uranus_turtle.shapesize(.7)  # Adjust the size of the dot if needed
bodies.append(uranus_turtle)

neptunus_turtle = turtle.Turtle()
#body3.penup()
neptunus_turtle.shape("circle")
neptunus_turtle.color("blue")
neptunus_turtle.pencolor("pink")
neptunus_turtle.shapesize(.6)  # Adjust the size of the dot if needed
bodies.append(neptunus_turtle)




# Starting Variables
solar_barycenter = [0, 0, 0]
starting_time_UNIX = 1704067200000  # UNIX millisecond time for Jan 1st, 2024, 00:00:00

seconds_per_day = 86400
seconds_per_orbital_year = 365.256363004*seconds_per_day
ticks_per_second = .00001
ticks = int(seconds_per_orbital_year * ticks_per_second  * 164.8)

for count in range(ticks):
    iterate_simulation(celestial_objects, ticks_per_second)
    barycenter = calculate_barycenter(celestial_objects)
    update_barycentric_coordinates_and_velocities(celestial_objects, barycenter)
    
    # Draw the positions of celestial objects
    for i, obj in enumerate(celestial_objects):
        x, y, _ = obj.return_coordinates()
        bodies[i].goto(x, y)

    # Update the screen
    screen.update()

    # Calculate percentage finished
    percent_finished = (count + 1) / ticks * 100
    
    # Print percentage finished without newline
    sys.stdout.write(f"\rProgress: {percent_finished:.2f}%")  # \r to go back to the beginning of the line
    sys.stdout.flush()  # Flush the output to ensure it's immediately displayed

# Close the turtle graphics window when simulation is finished
turtle.done()