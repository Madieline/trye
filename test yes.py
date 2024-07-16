#!/usr/bin/env python
# coding: utf-8

# In[3]:


import gspread
from matplotlib import pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

# Function to load the latest item from Google Sheets
def load_latest_item():
    # Connect to Google Sheets using service account credentials
    sa = gspread.service_account(filename='noble-velocity-429604-v7-683ffb52845c.json')
    sh = sa.open('ejeep_logbook')
    wks = sh.worksheet("LINE A")

    # Fetch the latest item from column B
    column_data = wks.col_values(2)
    last_item = column_data[-1].strip()  # Assuming the data is in column B and stripping whitespace

    return last_item

# Define the coordinates for the irregular shape (route)
coords = [(15, 1), (10, 1), (10, 3), (10, 4), (8, 4), (8, 4.5), (11, 4.5), (11, 5), (12.5, 5), (14.5, 5), (15, 5)]
x_coords = [15, 10, 10, 10, 8, 8, 11, 11, 12.5, 14.5, 15, 15]
y_coords = [1, 1, 3, 4, 4, 4.5, 4.5, 5, 5, 5, 5, 1]

# Define the coordinates and labels for the places (markers)
place_coords = [(15, 1), (10, 3), (8, 4), (11, 4.5), (12.5, 5), (14.5, 5)]
place_labels = ['HAGDAN NA BATO', 'LS COVERED COURTS', 'GATE 1', 'JSEC', 'LEONG HALL', 'XAVIER HALL']

# Load the pin icon image
icon_path = 'pin.png'  # Replace with your pin icon path
icon = plt.imread(icon_path)

# Create a figure and axis
fig, ax = plt.subplots()

# Plot the markers with pin icons and labels
for (x, y), label in zip(place_coords, place_labels):
    im = OffsetImage(icon, zoom=0.005)  # Adjust zoom factor as needed
    ab = AnnotationBbox(im, (x, y), xycoords='data', frameon=False)
    ax.add_artist(ab)
    ax.text(x + 0.1, y + 0.2, f' {label}', fontsize=8, verticalalignment='center_baseline', zorder=10)

# Function to highlight a specific route dynamically
def highlight_route(start, end):
    start_index = coords.index(place_coords[place_labels.index(start)])
    end_index = coords.index(place_coords[place_labels.index(end)])
    
    # Collect coordinates for the highlighted route segment from x_coords and y_coords
    highlighted_x = x_coords[start_index:end_index+1]  # Include the end point in the highlighted route
    highlighted_y = y_coords[start_index:end_index+1]
    
    # Plot the highlighted route segment
    ax.plot(highlighted_x, highlighted_y, color='red', linewidth=2, label=f'Route {start} to {end}')
    ax.legend()

# Example: Dynamically highlight a route based on the latest item from Google Sheets
try:
    last_item = load_latest_item()

    if last_item == "HAGDAN NA BATO":
        highlight_route("HAGDAN NA BATO", "LS COVERED COURTS")
    elif last_item == "LS COVERED COURTS":
        highlight_route("LS COVERED COURTS", "GATE 1")
    elif last_item == "GATE 1":
        highlight_route("GATE 1", "JSEC")
    elif last_item == "JSEC":
        highlight_route("JSEC", "LEONG HALL")
    elif last_item == "LEONG HALL":
        highlight_route("LEONG HALL", "XAVIER HALL")
    elif last_item == "XAVIER HALL":
        highlight_route("XAVIER HALL", "HAGDAN NA BATO")

    # Customize the plot
    ax.plot(x_coords, y_coords, color='lightgray', label='Other Routes')  # Plot the entire route line
    ax.set_title('Line A Route', fontsize=14, pad=20)  # Increase the font size of the title to 14 and pad with 20 points
    ax.axis('off')  # Turn off the axis

    # Adjust plot limits to fit markers and icons
    ax.set_xlim(min(x_coords) - 1, max(x_coords) + 1)
    ax.set_ylim(min(y_coords) - 1, max(y_coords) + 1)

    # Show the plot
    plt.show()

except Exception as e:
    print(f"Error: {e}")

