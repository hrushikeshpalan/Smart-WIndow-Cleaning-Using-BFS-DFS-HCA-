import tkinter as tk
import time
from tkinter import colorchooser
from collections import deque
from queue import Queue
import random
import matplotlib.pyplot as plt


window_width = 800  # Adjust according to your requirements
window_height = 600

total_area = (window_height-80)/20 * (window_width-80)/20       

cleaning_path = []

start_time = 0
end_time = 50



def detect_dirt(current_position):
    x = current_position[0]
    y = current_position[1]
    # Example: Assume dirt is represented by a specific color on the canvas
    pixel_color = canvas.itemcget(canvas.find_closest(x, y), 'fill')
    
    # Example: Let the user choose the color representing dirt
    dirt_color = "brown"
    
    # Check if the detected color matches the dirt color
    if pixel_color.lower() == dirt_color.lower():
        return True
    else:
        return False

def get_neighbors(position):
    x, y = position
    # Assuming 4-connectivity (up, down, left, right)
    neighbors = [
        (x - 20, y),  # Left    
        (x, y - 20),  # Up
        (x + 20, y),  # Right
        (x, y + 20),  # Down
    ]
    # You can add diagonal neighbors for 8-connectivity if needed
    # neighbors += [(x - 1, y - 1), (x - 1, y + 1), (x + 1, y - 1), (x + 1, y + 1)]
    
    # Filter out positions outside the window boundaries (modify based on your window size)
    neighbors = [(nx, ny) for nx, ny in neighbors if 40 <= nx < window_width-40 and 40 <= ny < window_height-40]

    return neighbors

def calculate_movement(current_position, next_position):
    # Assuming each step is one unit in both x and y directions
    current_x, current_y = current_position
    next_x, next_y = next_position

    # Calculate the difference in x and y coordinates
    dx = next_x - current_x
    dy = next_y - current_y

    return dx, dy

def detect_dirt_under_mechanism(mechanism_coords, dirt_area_coords):
    mech_x1, mech_y1, mech_x2, mech_y2 = mechanism_coords
    dirt_x1, dirt_y1, dirt_x2, dirt_y2 = dirt_area_coords

    if (dirt_x1 <= mech_x1 <= dirt_x2 or dirt_x1 <= mech_x2 <= dirt_x2) and \
       (dirt_y1 <= mech_y1 <= dirt_y2 or dirt_y1 <= mech_y2 <= dirt_y2):
        return True
    else:
        return False

def clean_dirt(mechanism_coords, root):
    dirt_areas = root.find_withtag("dirt")

    for dirt in dirt_areas:
        dirt_coords = canvas.coords(dirt)
        if detect_dirt_under_mechanism(mechanism_coords, dirt_coords):
            canvas.delete(dirt)  # Remove the dirt area
            break 



if __name__ == "__main__":
    root = tk.Tk()
    root.title("Window Cleaning Simulation")

    canvas = tk.Canvas(root, width=window_width, height=window_height, bg="black")
    canvas.pack()

    window_rect = canvas.create_rectangle(40, 40, window_width - 40, window_height - 40, outline="black", width=2, fill="lightblue")

    cleaning_mechanism = canvas.create_rectangle(40, 40, 60, 60, outline="black", width=2, fill="green")

    dirt_areas = [
        canvas.create_rectangle(100, 100, 120, 120, fill="brown", tags="dirt"),
        canvas.create_rectangle(580, 120, 600, 140, fill="brown", tags="dirt"),
        canvas.create_rectangle(160, 160, 180, 180, fill="brown", tags="dirt"),
        canvas.create_rectangle(220, 220, 240, 240, fill="brown", tags="dirt"),
        canvas.create_rectangle(460, 460, 480, 480, fill="brown", tags="dirt"),
        canvas.create_rectangle(40, 200, 60, 220, fill="brown", tags="dirt"),
        canvas.create_rectangle(500, 200, 520, 220, fill="brown", tags="dirt"),
        canvas.create_rectangle(100, 400, 120, 420, fill="brown", tags="dirt"),
        canvas.create_rectangle(360, 340, 380, 360, fill="brown", tags="dirt"),
        canvas.create_rectangle(660, 380, 680, 400, fill="brown", tags="dirt"),
        canvas.create_rectangle(720, 520, 740, 540, fill="brown", tags="dirt"),
    ]
    
    def move_cleaning_mechanism(dx, dy):
        canvas.move(cleaning_mechanism, dx, dy)

    def depth_first_search(start_position):
        visited = set()

        def dfs(current_position):
            print(current_position)
            cleaning_path.append(current_position)
            visited.add(current_position)

            neighbors = get_neighbors(current_position)

            for neighbor in neighbors:
                if neighbor not in visited:
                    if(detect_dirt(neighbor)): 
                        print("Dirt detected")
                        clean_dirt(canvas.coords(cleaning_mechanism), canvas)
                        # return True
                    move_cleaning_mechanism(*calculate_movement(current_position, neighbor))
                    canvas.update()
                    root.after(1)
                    dfs(neighbor)
                    return True

            return False

        # Start DFS from the initial position
        dfs(start_position)
   
    def breadth_first_search(current_position):
        visited_bfs = set()
        # print(current_position[0])

        my_queue = Queue()

        my_queue.put(current_position)

        while not my_queue.empty():
            canvas.update()
            root.after(1)
            bah = current_position
            current_position = my_queue.get()
            cleaning_path.append(current_position)
            if(detect_dirt(current_position)): 
                print("Dirt detected")
                clean_dirt(canvas.coords(cleaning_mechanism), canvas)
            move_cleaning_mechanism(*calculate_movement(bah, current_position))
            


            print(current_position)

            x = current_position[0]
            y = current_position[1]

            if (current_position[0], current_position[1]) not in visited_bfs:
                visited_bfs.add((current_position[0],current_position[1]))


                # Explore neighbors in all four directions
                neighbors = get_neighbors(current_position)

                for neighbor in neighbors:
                    nx = neighbor[0]
                    ny = neighbor[1]

                    # Check if the neighbor is within the matrix boundaries and not visited
                    if neighbor not in visited_bfs:
                        my_queue.put(neighbor)
        
    def hill_climbing(canvas, max_iterations):
        current_position = (40, 40)
        # move_cleaning_mechanism(current_position)

        for iteration in range(max_iterations):
            if(detect_dirt(current_position)): 
                print("Dirt detected")
                clean_dirt(canvas.coords(cleaning_mechanism), canvas)
            neighbors = get_neighbors(current_position)
            neighbor_values = [distance_to_nearest_dirt(neighbor) for neighbor in neighbors]

            if not any(neighbor_values):
                print("exiting")
                break  # No nearby dirt, exit the loop

            best_neighbor = neighbors[neighbor_values.index(min(neighbor_values))]

            cleaning_path.append(current_position)

            move_cleaning_mechanism(*calculate_movement(current_position, best_neighbor))
            current_position = best_neighbor
            # move_cleaning_mechanism(scale_factor, scale_factor)
            canvas.update()
            root.after(1)  # Adjust the delay as needed
        


    def distance_to_nearest_dirt(position):
        dirt_areas = canvas.find_withtag("dirt")
        min_distance = float('inf')

        for dirt in dirt_areas:
            dirt_coords = canvas.coords(dirt)
            dirt_center = (dirt_coords[0] + dirt_coords[2]) / 2, (dirt_coords[1] + dirt_coords[3]) / 2
            distance = ((position[0] - dirt_center[0]) ** 2 + (position[1] - dirt_center[1]) ** 2) ** 0.5
            min_distance = min(min_distance, distance)

        return min_distance

    

    def clean_window_dfs():
        global start_time
        global end_time
        start_time = time.time()
        depth_first_search((40, 40))
        # breadth_first_search([40,40])
        # hill_climbing(canvas, max_iterations=150)
        end_time = time.time()
        print(len(cleaning_path))
        pass

    def clean_window_bfs():
        global start_time
        global end_time
        start_time = time.time()
        # depth_first_search((40, 40))
        breadth_first_search([40,40])
        # hill_climbing(canvas, max_iterations=150)
        end_time = time.time()
        print(len(cleaning_path))
        pass

    def clean_window_hc():
        global start_time
        global end_time
        start_time = time.time()
        # depth_first_search((40, 40))
        # breadth_first_search([40,40])
        hill_climbing(canvas, max_iterations=150)
        end_time = time.time()
        print(len(cleaning_path))
        # Function to visualize movement for Hill Climb
        def visualize_movement(path):
            for step in path:
                # Update cleaning mechanism's position on the plot
                plt.plot(step[0], step[1], marker='o', color='blue')
                plt.pause(0.001)  # Pause for better visualization

        # Example path (replace with actual path from your algorithm)

        # Visualize movement
        plt.figure()
        plt.title("Cleaning Mechanism Movement")
        visualize_movement(cleaning_path)
        plt.show()
        pass


    clean_button = tk.Button(root, text="Clean Window using DFS", command=clean_window_dfs)
    clean_button.pack()
    clean_button = tk.Button(root, text="Clean Window using BFS", command=clean_window_bfs)
    clean_button.pack()
    clean_button = tk.Button(root, text="Clean Window using Hill Climb", command=clean_window_hc)
    clean_button.pack()

    root.mainloop()

    

    print(start_time, end_time)

    execution_time = end_time - start_time

    print(f"Path Length: {len(cleaning_path)}")
    print(f"Computation Time: {execution_time} seconds")
    print(f"Coverage Rate: {len(cleaning_path) / total_area * 100}%")


    elapsed_time = end_time - start_time

    print(f"Elapsed Time: {elapsed_time} seconds")






        