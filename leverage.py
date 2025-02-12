import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import math


# Define the functions
def LR_call(t, LR0):
    return LR0 * (1 - t) / (1 - t * LR0)


def LR_short(t, LR0):
    return LR0 * (1 + t) / (1 - t * LR0)


def LR_ratio(t, LR0):
    return LR_short(t, LR0) / LR_call(t, LR0)


# Set up the figure and axis
fig, ax = plt.subplots(figsize=(12, 8))
plt.subplots_adjust(left=0.1, bottom=0.3)  # Adjust layout to make room for the slider

# Initial value of LR(0)
initial_LR0 = 2.0


# Function to calculate dynamic t range based on LR(0)
def calculate_t_range(LR0):
    t_min = 0.0
    t_max = 1 / LR0 - 0.01  # Avoid division by zero
    return t_min, t_max


# Generate initial t values
t_min, t_max = calculate_t_range(initial_LR0)
t_values = np.linspace(t_min, t_max, 400)

# Plot the initial curves
line_call, = plt.plot(t_values, LR_call(t_values, initial_LR0), label=r'$LR_{call}(t)$', color='blue')
line_short, = plt.plot(t_values, LR_short(t_values, initial_LR0), label=r'$LR_{short}(t)$', color='red')
line_ratio, = plt.plot(t_values, LR_ratio(t_values, initial_LR0), label=r'$\frac{LR_{short}(t)}{LR_{call}(t)}$',
                       color='green', linestyle='--')

# Add labels, title, and legend
plt.xlabel('t (Change in Stock Price / Original Stock Price)')
plt.ylabel('Leverage Ratio (LR(t))')
plt.title(f'Leverage Ratios vs. Stock Price Change (LR(0) = {initial_LR0})')
plt.axhline(0, color='black', linewidth=0.5, linestyle='--')  # Add a horizontal line at y=0
plt.axvline(0, color='black', linewidth=0.5, linestyle='--')  # Add a vertical line at t=0
plt.legend()
plt.grid(True)

# Set initial y-axis limits
plt.ylim(1, 10 * initial_LR0)

# Add a slider for LR(0)
ax_slider = plt.axes([0.2, 0.1, 0.6, 0.03])  # Define slider position
slider = Slider(ax_slider, 'LR(0)', 1, 10.0, valinit=initial_LR0)


# Update function for the slider
def update(val):
    LR0 = slider.val

    # Update t range dynamically
    t_min, t_max = calculate_t_range(LR0)
    t_values = np.linspace(t_min, t_max, 400)

    # Update the curves
    line_call.set_data(t_values, LR_call(t_values, LR0))
    line_short.set_data(t_values, LR_short(t_values, LR0))
    line_ratio.set_data(t_values, LR_ratio(t_values, LR0))

    # Update the title
    ax.set_title(f'Leverage Ratios vs. Stock Price Change (LR(0) = {LR0})')

    # Update the y-axis limits
    ax.set_ylim(1, 10 * (math.exp(0.25*(LR0-1))+1))
    ax.set_xlim(0, 1/LR0-0.01)

    # Redraw the plot
    fig.canvas.draw_idle()


# Attach the update function to the slider
slider.on_changed(update)

# Show the plot
plt.show()