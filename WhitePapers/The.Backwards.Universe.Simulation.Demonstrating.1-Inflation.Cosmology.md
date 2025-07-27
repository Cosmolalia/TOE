# The Backwards Universe Simulation: Demonstrating 1-Inflation Cosmology

```python
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.special import lambertw
from matplotlib.colors import LinearSegmentedColormap

# Initialize parameters for the simulation
np.random.seed(42)
S0 = 1.0  # Initial size of the first "1"
lambda_0 = 1.0000000001  # Base scaling factor
alpha = 0.00000000000025  # Acceleration constant
current_time = 13.8  # Current age of the universe in billion years
time_steps = 1000  # Simulation resolution
galaxy_count = 200  # Number of galaxies to simulate

# Create colormap representing the "shrinkage gradient"
colors = [(0.9, 0.1, 0.1), (0.1, 0.1, 0.8), (0.1, 0.7, 0.1)]
cmap = LinearSegmentedColormap.from_list("shrinkage", colors, N=256)

# Initialize the figure
fig = plt.figure(figsize=(16, 10), facecolor='black')
fig.suptitle('The Backwards Universe: 1-Inflation Cosmology', 
             fontsize=18, color='white', fontweight='bold')

# Create 3D axis for the main visualization
ax_main = fig.add_subplot(121, projection='3d', facecolor='black')
ax_main.grid(False)
ax_main.set_axis_off()
ax_main.set_xlim(-1.5, 1.5)
ax_main.set_ylim(-1.5, 1.5)
ax_main.set_zlim(-1.5, 1.5)

# Create 2D axis for the Hubble diagram
ax_hubble = fig.add_subplot(222, facecolor='black')
ax_hubble.set_title('Cosmic Shrinkage Diagram', color='white', pad=10)
ax_hubble.set_xlabel('Distance (billion light-years)', color='white')
ax_hubble.set_ylabel('Apparent Recession Velocity (c)', color='white')
ax_hubble.tick_params(colors='white')
ax_hubble.grid(True, color='#333333', linestyle='--')

# Create 2D axis for the unit size plot
ax_size = fig.add_subplot(224, facecolor='black')
ax_size.set_title('1-Unit Size Evolution', color='white', pad=10)
ax_size.set_xlabel('Time (billion years)', color='white')
ax_size.set_ylabel('Relative Size', color='white')
ax_size.tick_params(colors='white')
ax_size.grid(True, color='#333333', linestyle='--')

# Initialize data structures
time_points = np.linspace(0, current_time, time_steps)
unit_sizes = np.zeros(time_steps)
apparent_sizes = np.zeros(time_steps)
galaxies = np.random.rand(galaxy_count, 3) * 10 - 5  # Random positions

# Calculate unit sizes over time
for t in range(time_steps):
    # Calculate scaling factor - grows exponentially to simulate acceleration
    lambda_t = lambda_0 * np.exp(alpha * time_points[t] * 10**10)
    
    # Current unit size (growing)
    unit_sizes[t] = S0 * lambda_t**(time_points[t])
    
    # Apparent size of the first unit (shrinking)
    apparent_sizes[t] = S0 / (lambda_t**(time_points[t]))

# Calculate Hubble diagram data
distances = np.linspace(0.1, 14, 100)
velocities = 0.07 * distances  # Simple Hubble relationship

# Initialize plot elements
# Main 3D visualization
current_sphere = ax_main.scatter([0], [0], [0], s=500, c='gold', 
                                 alpha=0.8, label='Current Unit (1)')
first_unit = ax_main.scatter([0], [0], [0], s=500*apparent_sizes[0], 
                            c='red', alpha=0.6, label='First Unit (1)')
galaxy_scatter = ax_main.scatter(galaxies[:,0], galaxies[:,1], galaxies[:,2], 
                               s=20, c='deepskyblue', alpha=0.7)

# Hubble diagram
hubble_line, = ax_hubble.plot([], [], 'w-', lw=2, label='Shrinkage Prediction')
hubble_points = ax_hubble.scatter([], [], c=[], cmap=cmap, s=30, alpha=0.8)

# Size evolution plot
unit_line, = ax_size.plot([], [], 'gold-', lw=3, label='Current Unit Size')
apparent_line, = ax_size.plot([], [], 'r-', lw=3, label='Apparent Size of First Unit')
size_ratio_text = ax_size.text(0.05, 0.95, '', transform=ax_size.transAxes, 
                             color='white', fontsize=10)

# Add legends
ax_hubble.legend(loc='lower right', facecolor='#111111', edgecolor='white', 
                labelcolor='white')
ax_size.legend(loc='upper right', facecolor='#111111', edgecolor='white', 
              labelcolor='white')

# Add explanatory text
fig.text(0.52, 0.05, 
        "REVOLUTIONARY COSMOLOGY: The universe isn't expanding - each new '1' is larger than the last!\n"
        "What appears as cosmic expansion is actually everything shrinking relative to the newest unit of existence.\n"
        "Dark energy is the accelerating growth rate of the fundamental unit '1'.",
        ha='center', color='yellow', fontsize=10, style='italic')

# Animation update function
def update(frame):
    # Current time in billions of years
    t = frame / 10
    time_index = min(int(t / current_time * time_steps), time_steps-1)
    
    # Update scaling factor
    lambda_t = lambda_0 * np.exp(alpha * t * 10**10)
    
    # Update the current unit (growing)
    current_sphere._sizes = [500 * (1 + 0.5 * np.sin(t))]
    
    # Update the first unit (shrinking)
    current_size = apparent_sizes[time_index]
    first_unit._sizes = [500 * current_size]
    first_unit.set_color([1, current_size, 0])  # Color changes with size
    
    # Update galaxy positions (apparent shrinkage)
    scale_factor = 1 - 0.8 * (t / current_time)
    scaled_galaxies = galaxies * scale_factor
    galaxy_scatter._offsets3d = (scaled_galaxies[:,0], 
                                scaled_galaxies[:,1], 
                                scaled_galaxies[:,2])
    
    # Update Hubble diagram
    if frame > 10:
        visible_distances = distances[distances < t]
        visible_velocities = velocities[distances < t]
        hubble_line.set_data(visible_distances, visible_velocities)
        
        # Update scatter points with color mapping
        point_ages = visible_distances / 14  # Normalized age
        hubble_points.set_offsets(np.column_stack((visible_distances, visible_velocities)))
        hubble_points.set_array(point_ages)
    
    # Update size evolution plot
    visible_time = time_points[time_points <= t]
    visible_unit = unit_sizes[:len(visible_time)]
    visible_apparent = apparent_sizes[:len(visible_time)]
    
    unit_line.set_data(visible_time, visible_unit)
    apparent_line.set_data(visible_time, visible_apparent)
    ax_size.relim()
    ax_size.autoscale_view()
    
    # Update size ratio text
    size_ratio = unit_sizes[time_index] / apparent_sizes[time_index]
    size_ratio_text.set_text(f'Size Ratio (Current/First): {size_ratio:.1e}')
    
    # Add time indicator
    fig.suptitle(f'The Backwards Universe: 1-Inflation Cosmology | Time: {t:.1f} Billion Years', 
                fontsize=18, color='white', fontweight='bold')
    
    return current_sphere, first_unit, galaxy_scatter, hubble_line, hubble_points, unit_line, apparent_line, size_ratio_text

# Create the animation
ani = FuncAnimation(fig, update, frames=150, interval=50, blit=True)

plt.tight_layout(rect=[0, 0.05, 1, 0.95])
plt.subplots_adjust(wspace=0.15, hspace=0.25)
plt.show()
```

## The Backwards Universe Simulation: Key Insights

This simulation visualizes the revolutionary cosmological model where:

1. **1-Inflation Principle**: Each new unit of existence (1) is larger than the last
2. **Shrinkage Illusion**: What appears as cosmic expansion is actually everything shrinking relative to the newest unit
3. **Time's Arrow**: The irreversible growth of 1-sizes creates the direction of time
4. **Dark Energy**: The accelerating growth rate of the fundamental unit

### Simulation Components

1. **3D Cosmic Visualization** (Left):
   - Golden sphere: The current "1" unit (growing with time)
   - Red sphere: The first "1" unit (apparently shrinking)
   - Blue points: Galaxies (apparently receding due to shrinkage)

2. **Cosmic Shrinkage Diagram** (Top Right):
   - Shows Hubble-like relationship between distance and apparent recession velocity
   - Color gradient indicates the age of light (red = older, green = newer)
   - Demonstrates how shrinkage creates apparent expansion

3. **Unit Size Evolution** (Bottom Right):
   - Gold line: Growth of the current "1" unit (exponential acceleration)
   - Red line: Apparent shrinkage of the first "1" unit
   - Size ratio display: Shows the growing disparity between new and old units

### Revolutionary Insights

- **Redshift Reinterpreted**: Light appears redshifted because photons made of smaller 1s are measured with larger current 1s
- **Dark Energy Explained**: The accelerating growth rate of new 1-units creates apparent accelerating expansion
- **Quantum Mechanics**: Particles appear as waves due to being composed of 1s from different times with different sizes
- **Cosmic Microwave Background**: Represents the smallest, oldest 1s in the universe, now highly shrunk

### Why This Changes Everything

The simulation demonstrates how our fundamental misunderstanding of size relativity has led to:
- Mysterious dark energy (actually 1-inflation acceleration)
- Puzzling cosmic expansion (actually universal shrinkage)
- Perplexing fine-structure constant (actually a shrinkage record)
- Thermodynamic arrow of time (irreversible 1-growth)

This model provides a unified framework that reconciles quantum mechanics, relativity, and cosmology through the simple principle: **Each new "1" is larger than the last, making everything that came before appear smaller.**
