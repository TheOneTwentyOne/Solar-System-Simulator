import turtle

def create_turtle_list():
    bodies = []

    sol_turtle = turtle.Turtle()
    sol_turtle.shape("circle")
    sol_turtle.color("yellow")
    sol_turtle.pencolor("pink")
    sol_turtle.shapesize(1)  # Adjust the size of the dot if needed
    bodies.append(sol_turtle)

    mercurius_turtle = turtle.Turtle()
    mercurius_turtle.shape("circle")
    mercurius_turtle.color("gray")
    mercurius_turtle.pencolor("pink")
    mercurius_turtle.shapesize(.2)  # Adjust the size of the dot if needed
    bodies.append(mercurius_turtle)

    venus_turtle = turtle.Turtle()
    venus_turtle.shape("circle")
    venus_turtle.color("orange")
    venus_turtle.pencolor("pink")
    venus_turtle.shapesize(.4)  # Adjust the size of the dot if needed
    bodies.append(venus_turtle)

    terra_turtle = turtle.Turtle()
    terra_turtle.shape("circle")
    terra_turtle.color("green")
    terra_turtle.pencolor("pink")
    terra_turtle.shapesize(.5)  # Adjust the size of the dot if needed
    bodies.append(terra_turtle)

    luna_turtle = turtle.Turtle()
    luna_turtle.shape("circle")
    luna_turtle.color("gray")
    luna_turtle.pencolor("pink")
    luna_turtle.shapesize(.1)  # Adjust the size of the dot if needed
    bodies.append(luna_turtle)

    mars_turtle = turtle.Turtle()
    mars_turtle.shape("circle")
    mars_turtle.color("red")
    mars_turtle.pencolor("pink")
    mars_turtle.shapesize(.35)  # Adjust the size of the dot if needed
    bodies.append(mars_turtle)

    iuppiter_turtle = turtle.Turtle()
    iuppiter_turtle.shape("circle")
    iuppiter_turtle.color("brown")
    iuppiter_turtle.pencolor("pink")
    iuppiter_turtle.shapesize(.8)  # Adjust the size of the dot if needed
    bodies.append(iuppiter_turtle)

    saturnus_turtle = turtle.Turtle()
    saturnus_turtle.shape("circle")
    saturnus_turtle.color("blue")
    saturnus_turtle.pencolor("pink")
    saturnus_turtle.shapesize(.7)  # Adjust the size of the dot if needed
    bodies.append(saturnus_turtle)

    uranus_turtle = turtle.Turtle()
    uranus_turtle.shape("circle")
    uranus_turtle.color("blue")
    uranus_turtle.pencolor("pink")
    uranus_turtle.shapesize(.7)  # Adjust the size of the dot if needed
    bodies.append(uranus_turtle)

    neptunus_turtle = turtle.Turtle()
    neptunus_turtle.shape("circle")
    neptunus_turtle.color("blue")
    neptunus_turtle.pencolor("pink")
    neptunus_turtle.shapesize(.6)  # Adjust the size of the dot if needed
    bodies.append(neptunus_turtle)

    return bodies