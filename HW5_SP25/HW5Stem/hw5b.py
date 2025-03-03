# region imports
import hw5a as pta
import random as rnd
from matplotlib import pyplot as plt
# endregion

# region functions
def ffPoint(Re, rr):
    """
    This function takes Re and rr as parameters and outputs a friction factor according to the following:
    1. if Re>4000 use Colebrook Equation
    2. if Re<2000 use f=64/Re
    3. else calculate a probabilistic friction factor where the distribution has a mean midway between the prediction
       of the f=64/Re and Colebrook Equations and a standard deviation of 20% of this mean
    :param Re: the Reynolds number
    :param rr: the relative roughness
    :return: the friction factor
    """
    if Re >= 4000:
        return pta.ff(Re, rr, CBEQN=True) # Turbulent Flow (Colebrook Equation)
    if Re <= 2000: # Laminar Flow
        return pta.ff(Re, rr)
    CBff = pta.ff(4000, rr, CBEQN=True)  # # Friction factor at Re=4000 (Colebrook)
    Lamff = pta.ff(2000, rr)  # Friction factor at Re=2000 (laminar)
    mean = (CBff + Lamff) / 2
    sig = 0.2 * mean
    return rnd.normalvariate(mean, sig)  # use normalvariate to select a number randomly from a normal distribution

def PlotPoint(points):
    """
    Plot all points on the Moody diagram with an icon indicating if the flow is transitional.
    Plots the blank Moddy chart and add the markers as the user inputs parameters and plots all
    the markers and a legend specifying its Re and rr, once the loop is concluded.
    :args: point = Re, f, is_transition
    :param Re: Reynolds number
    :param f: friction factor
    :param is_transition: boolean indicating if the flow is in the transition region
    :param rr: relative roughness
    """

    pta.plotMoody(clear_plot=True)  # Plot the base Moody diagram
    for point in points:
        Re, f, is_transition, rr = point
        if is_transition:
            marker = '^'  # upward triangle for transition
        else:
            marker = 'o'  # circle for laminar or turbulent

        # Creates a label for the legend with Re and rr for each point
        label = f'Re={Re:.2e}, rr={rr:.2e}'

        # Plot the point on the Moody diagram
        plt.plot(Re, f, marker=marker, markersize=10, markeredgecolor='red', markerfacecolor='none', label=label)

    plt.legend(title="Re, rr - First to Last", loc='best') # Creates a legend specifying the Re and rr from the first entry to the last
    plt.show()  # Display the plot after all points are added


def calculate_head_loss_per_foot(f, D, V):
    """
    Calculate head loss per foot using the Darcy-Weisbach equation.
    :param f: friction factor
    :param D: pipe diameter in inches
    :param V: average velocity of the fluid in ft/s
    :return: head loss per foot in ft/ft
    """
    g = 32.2  # acceleration due to gravity in ft/s^2
    D_ft = D / 12  # convert diameter from inches to feet
    hf_L = f * (V**2) / (D_ft * 2 * g)
    return hf_L

def main():
    points = [] # A list to store all points and allows all points to be plotted

    while True:
        # Input from the user
        D = float(input("Enter the pipe diameter in inches: "))
        epsilon = float(input("Enter the pipe roughness in micro-inches: "))
        Q = float(input("Enter the flow rate in gallons per minute: "))

        # Convert inputs to consistent units
        epsilon_m = epsilon * 1e-6  # convert micro-inches to inches
        rr = epsilon_m / D  # Calculates relative roughness
        Q_cfs = Q * 0.002228  # convert gallons per minute to cubic feet per second
        A = 3.14159 * (D / 12)**2 / 4  # cross-sectional area in ft^2
        V = Q_cfs / A  # average velocity in ft/s

        # Calculate Reynolds number
        rho = 1.94  # density of water in slugs/ft^3
        mu = 2.34e-5  # dynamic viscosity of water in lb*s/ft^2
        Re = rho * V * (D / 12) / mu

        # Determine if the flow is in the transition region
        is_transition = 2000 < Re < 4000

        # Calculate friction factor
        f = ffPoint(Re, rr)

        # Calculate head loss per foot with given parameters and print it out
        hf_L = calculate_head_loss_per_foot(f, D, V)
        print(f"Head loss per foot: {hf_L:.6f} ft/ft")

        # Store the point, created from the given parameters, in the list for plotting
        points.append((Re, f, is_transition, rr))

        # Ask the user if they want to re-specify the parameters
        repeat = input("Do you want to continue adding parameters? (yes/no): ").strip().lower()
        if repeat != 'yes':
            break

    # Plot the points on the Moody diagram after the loop is finished by running PlotPoint using all
    # the values in the "points" list
    PlotPoint(points)
# endregion

# region function calls
if __name__ == "__main__":
    main()
# endregion