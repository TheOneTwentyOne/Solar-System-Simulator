import sys
import math
import time
import turtle
import numpy as np
import concurrent.futures
from celestial_object_class import celestial_object
from celestial_object_list_creator import create_celestial_objects
from turtle_list_creator import create_turtle_list





# Create objects for the celestial objects in the solar system, along with the pairs for gravitational influences
celestial_objects = create_celestial_objects()
celestial_object_pairs = [(x, y) for x in range(len(celestial_objects)) for y in range(x + 1, len(celestial_objects))]

# Starting Variables:
starting_time_UNIX = 1704067200 # UNIX time (seconds): Jan 1st, 2024, 00:00:00 GMT
#ending_time_UNIX = 1735689600   # UNIX time (seconds): Jan 1st, 2025, 00:00:00 GMT, MAIN RUNNER
ending_time_UNIX = 2020291200   # UNIX time (seconds): Jan 1st, 2035 (??), 00:00:00 GMT

ticks_per_second = 1/1600
ticks = int((ending_time_UNIX-starting_time_UNIX) * ticks_per_second) # 31622400 seconds between timestamps
current_time = float(starting_time_UNIX)

eclipse_dates = []

## Initialize turtle
#screen = turtle.Screen()
#screen.setup(width=800, height=800)
#val = 1e12
#screen.setworldcoordinates(-val, -val, val, val)  # Adjust this range based on your data
#screen.tracer(0)
#
#draw_orbit = False
#bodies = create_turtle_list()
#for body in bodies:
#    if draw_orbit == False:
#        body.penup()






def calculate_acceleration(body_one, body_two):
    pos_one = body_one.return_coordinates()
    pos_two = body_two.return_coordinates()
    mass_one = body_one.return_mass()
    mass_two = body_two.return_mass()
    
    displacement_vector = pos_two - pos_one
    distance = np.linalg.norm(displacement_vector)  # Calculate distance once
    
    grav_force = (6.6743E-11) * ((mass_one * mass_two) / (distance ** 2))
    
    force_vector = displacement_vector * (grav_force / distance)  # Vectorized calculation
    
    body_one_accel_vector = force_vector / mass_one
    body_two_accel_vector = -force_vector / mass_two
    
    return body_one_accel_vector, body_two_accel_vector



def iterate_simulation(celestial_objects, tps):

    global current_time

    def round_array(arr, n):
        return np.array([round(val, n) for val in arr])

    def distance_calc(pos_one, pos_two):
        distance = math.sqrt( ( (pos_two[0]-pos_one[0])**2 ) + ( (pos_two[1]-pos_one[1])**2 ) + ( (pos_two[2]-pos_one[2])**2 ) )
        return distance


    # 04 should be longer
    # than 03 if its a 
    # Lunar eclipse


    # Check for an eclipse:
    direction_vector = celestial_objects[3].return_coordinates() - celestial_objects[0].return_coordinates()
    direction_vector /= np.linalg.norm(direction_vector)
    alignment_threshold = 1000  # Threshold for alignment in meters
    sol_to_luna_vector = celestial_objects[4].return_coordinates() - celestial_objects[0].return_coordinates()
    perpendicular_distance = np.linalg.norm(np.cross(sol_to_luna_vector, direction_vector))
    is_aligned = perpendicular_distance <= alignment_threshold + celestial_objects[4].return_radius() + celestial_objects[3].return_radius()

    if is_aligned:
        eclipse_type = "Solar"
        if ( ( distance_calc( celestial_objects[0].return_coordinates(), celestial_objects[4].return_coordinates() ) ) > ( distance_calc( celestial_objects[0].return_coordinates(), celestial_objects[3].return_coordinates() ) ) ):
            eclipse_type = "Lunar"
        # Append eclipse date to the list
        eclipse_dates.append(f"{eclipse_type} Eclipse on: {(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(current_time)))}")


    # Calculate acceleration in parallel:
    for i in range(len(celestial_objects)):
        globals()[f"body{i}_cumulative_acceleration"] = np.array([0, 0, 0])
    
    def calculate_acceleration_for_pair(pair):
        body_one_accel, body_two_accel = calculate_acceleration(celestial_objects[pair[0]], celestial_objects[pair[1]])
        return pair[0], body_one_accel, pair[1], body_two_accel

    with concurrent.futures.ThreadPoolExecutor() as executor:
        acceleration_results = list(executor.map(calculate_acceleration_for_pair, celestial_object_pairs))

    for result in acceleration_results:
        body_one_index, body_one_accel, body_two_index, body_two_accel = result
        globals()[f"body{body_one_index}_cumulative_acceleration"] = np.add(body_one_accel, globals()[f"body{body_one_index}_cumulative_acceleration"])
        globals()[f"body{body_two_index}_cumulative_acceleration"] = np.add(body_two_accel, globals()[f"body{body_two_index}_cumulative_acceleration"])

    for i in range(len(celestial_objects)):
        celestial_objects[i].apply_acceleration(globals()[f"body{i}_cumulative_acceleration"], tps)
        celestial_objects[i].apply_velocity(tps)



    # Barycenter section:
    total_mass = 0
    barycenter = np.array([0.0, 0.0, 0.0])
    # Iterate over each celestial object
    for obj in celestial_objects:
        mass, coordinates = obj.return_mass(), obj.return_coordinates()
        total_mass += mass
        x, y, z = coordinates
        barycenter[0] += mass * x
        barycenter[1] += mass * y
        barycenter[2] += mass * z
    # Calculate the barycenter coordinates
    barycenter[0] /= total_mass
    barycenter[1] /= total_mass
    barycenter[2] /= total_mass
    for obj in celestial_objects:
        obj.set_coordinates(round_array(np.subtract(obj.return_coordinates(), barycenter), 4))
        obj.set_velocity(round_array(obj.return_velocity(), 4))
    







for count in range(ticks):
    iterate_simulation(celestial_objects, ticks_per_second)
    
    ## Draw the positions of celestial objects
    #for i, obj in enumerate(celestial_objects):
    #    x, y, _ = obj.return_coordinates()
    #    bodies[i].goto(x, y)
    
    # Update the screen
    #screen.update()

    # Calculate percentage finished
    percent_finished = (count + 1) / ticks * 100
    
    # Print percentage finished without newline
    sys.stdout.write(f"\rProgress: {percent_finished:.2f}%")  # \r to go back to the beginning of the line
    sys.stdout.flush()  # Flush the output to ensure it's immediately displayed
    current_time += 1 / ticks_per_second


print("Final UNIX timestamp:", current_time)
eclipse_dates = list(set(eclipse_dates))
eclipse_dates.sort()
with open("eclipses.txt", "w") as file:
    for date in eclipse_dates:
        file.write(f"{date}\n")



















## Time testing
#
#st = time.perf_counter_ns()
#et = time.perf_counter_ns()
#print("time1: ", (et-st))
#input()























































def calculate_acceleration(body_one, body_two):
    pos_one = body_one.return_coordinates()
    pos_two = body_two.return_coordinates()
    mass_one = body_one.return_mass()
    mass_two = body_two.return_mass()
    
    displacement_vector = pos_two - pos_one
    distance = np.linalg.norm(displacement_vector)  # Calculate distance once
    
    grav_force = (6.6743E-11) * ((mass_one * mass_two) / (distance ** 2))
    
    force_vector = displacement_vector * (grav_force / distance)  # Vectorized calculation
    
    body_one_accel_vector = force_vector / mass_one
    body_two_accel_vector = -force_vector / mass_two
    
    return body_one_accel_vector, body_two_accel_vector