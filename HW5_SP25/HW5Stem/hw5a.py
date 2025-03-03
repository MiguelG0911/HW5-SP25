# region imports
import numpy as np
from scipy.optimize import fsolve
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
# endregion

# region functions
def ff(Re, rr, CBEQN=False):
    """
    This function calculates the friction factor for a pipe based on the
    notion of laminar, turbulent and transitional flow.
    :param Re: the Reynolds number under question.
    :param rr: the relative pipe roughness (expect between 0 and 0.05)
    :param CBEQN: boolean to indicate if I should use Colebrook (True) or laminar equation
    :return: the (Darcy) friction factor
    """
    if CBEQN:
        # note: in numpy log is for natural log. log10 is log base 10.
        cb = lambda f: 1/np.sqrt(abs(f)) + 2.0 * np.log10((rr/3.7) + (2.51/(Re * np.sqrt(abs(f)))))
        # Provide a reasonable initial guess for fsolve to avoid convergence issues
        result = fsolve(cb, max(0.02, 1e-5))
        # Ensure the result is a scalar and not an array
        return result[0]
    else:
        return 64/Re
    pass

def plotMoody(plotPoint=False, pt=(0,0), marker='o', markersize=10, markeredgecolor='red', markerfacecolor='none', label=None, clear_plot=False):
    """
    This function produces the Moody diagram for a Re range from 1 to 10^8 and
    for relative roughness from 0 to 0.05 (20 steps). The laminar region is described
    by the simple relationship of f=64/Re whereas the turbulent region is described by
    the Colebrook equation.
    :param plotPoint: boolean to indicate if a point should be plotted
    :param pt: tuple (Re, f) for the point to plot
    :param marker: marker style for the point
    :param markersize: size of the marker
    :param markeredgecolor: color of the marker edge
    :param markerfacecolor: color of the marker face
    :param label: label for the marker in the legend
    :param clear_plot: boolean to indicate if the plot should be cleared before plotting
    :return: just shows the plot, nothing returned
    """

    # Step 1: create logspace arrays for ranges of Re
    ReValsCB = np.logspace(np.log10(4000), np.log10(1e8), 100)  # for use with Colebrook equation (i.e., Re in range from 4000 to 10^8)
    ReValsL = np.logspace(np.log10(600.0), np.log10(2000.0), 20)  # for use with Laminar flow (i.e., Re in range from 600 to 2000)
    ReValsTrans = np.logspace(np.log10(2000.0), np.log10(4000.0), 50)  # for use with Transition flow (i.e., Re in range from 2000 to 4000)

    # Step 2: create array for range of relative roughnesses
    rrVals = np.array([0, 1E-6, 5E-6, 1E-5, 5E-5, 1E-4, 2E-4, 4E-4, 6E-4, 8E-4, 1E-3, 2E-3, 4E-3, 6E-3, 8E-3, 1.5E-2, 2E-2, 3E-2, 4E-2, 5E-2])

    # Step 3: calculate the friction factor in the laminar range
    ffLam = np.array([ff(Re, 0) for Re in ReValsL])  # use list comprehension for all Re in ReValsL and calling ff
    ffTrans = np.array([ff(Re, 0) for Re in ReValsTrans])  # use list comprehension for all Re in ReValsTrans and calling ff

    # Step 4: calculate friction factor values for each rr at each Re for turbulent range
    ffCB = np.array([[ff(Re, rr, True) for Re in ReValsCB] for rr in rrVals])

    # Step 5: construct the plot
    plt.figure(figsize=(10, 8))  # Set figure size for better readability
    plt.loglog(ReValsL, ffLam, 'b-')  # plot the laminar part as a solid line
    plt.loglog(ReValsTrans, ffTrans, 'b--')  # plot the transition part as a dashed line
    for nRelR in range(len(ffCB)):
        plt.loglog(ReValsCB, ffCB[nRelR], 'k-')  # plot the lines for the turbulent region for each pipe roughness
        plt.annotate(xy=(ReValsCB[-1], ffCB[nRelR][-1]), text=f"{rrVals[nRelR]:.2e}")  # annotate each curve

    plt.xlim(600, 1E8)
    plt.ylim(0.008, 0.10)
    plt.xlabel(r"Reynolds number $Re$", fontsize=16)
    plt.ylabel(r"Friction factor $f$", fontsize=16)
    plt.text(2.5E8, 0.02, r"Relative roughness $\frac{\epsilon}{d}$", rotation=90, fontsize=16)
    ax = plt.gca()  # capture the current axes for use in modifying ticks, grids, etc.
    ax.tick_params(axis='both', which='both', direction='in', top=True, right=True, labelsize=12)  # format tick marks
    ax.tick_params(axis='both', grid_linewidth=1, grid_linestyle='solid', grid_alpha=0.5)
    ax.tick_params(axis='y', which='minor')
    ax.yaxis.set_minor_formatter(FormatStrFormatter("%.3f"))
    plt.grid(which='both')
    if plotPoint:
        plt.plot(pt[0], pt[1], marker=marker, markersize=markersize, markeredgecolor=markeredgecolor, markerfacecolor=markerfacecolor, label=label)  # plot the point with specified properties


def main():

    #Ask to plot a blank Moody Chart with no markers. This is to ensure hw5a works alone without affecting the function of hw5b.
    create_chart = input("Do you want to print a blank Moody Chart? (yes/no): ")
    if create_chart == 'yes' or 'y' or 'Yes':
        plotMoody()
        plt.show()
    else:
        print("Did not create a blank Moody Chart")

# endregion

# region function calls
if __name__ == "__main__":
    main()
# endregion