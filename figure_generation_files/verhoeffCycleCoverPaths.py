import argparse
import os

import matplotlib.pyplot as plt
from matplotlib.axes import Axes


def fig11(ax: Axes, even_int: int) -> None:
    """
    Generate and plot Figure 11 from Verhoeff's paper (see References). The figure displays a path between `c` and `d`:\n
        - `c1 = 12 0^k_0 1`
        - `d1 = 0 21 0^{k_0-1} 1`\n
    where `k_0` is an even integer (`even_int`). The path is highlighted in blue and important nodes are marked.

    Args:
        ax (Axes): The matplotlib Axes object to plot the figure on.
        even_int (int): An even integer value.

    Returns:
        None: Works in place to plot the figure on the given `ax`.

    References:
        - Tom Verhoeff. The spurs of D. H. Lehmer: Hamiltonian paths in neighbor-swap graphs of permutations. Designs, Codes, and Cryptography, 84(1-2):295-310, 7 2017.
    """
    diff_4 = even_int - 4

    # Set limits and aspect ratio
    x, y = 4 + diff_4, 5 + diff_4
    ax.set_xlim(-0.5, x + 0.5)
    ax.set_ylim(-0.5, y + 0.5)
    ax.set_aspect("equal")

    # Draw vertical lines
    for y_line in range(x + 1):
        ax.plot([y_line, y_line], [0, y], color="black", linewidth=1)

    # Draw horizontal lines except for the diagonal positions where x == y
    for y_line in range(y + 1):
        for x_line in range(x):
            if x_line != y_line - 1:
                ax.plot(
                    [x_line, x_line + 1], [y_line, y_line], color="black", linewidth=1
                )

    # Highlighted path coordinates
    generated_tuples = []
    for i in range(0, diff_4, 2):
        generated_tuples.append((x - i, i))
        generated_tuples.append((x - i, y - i))
        generated_tuples.append((0, y - i))
        generated_tuples.append((0, y - i - 1))
        generated_tuples.append((x - i - 1, y - i - 1))
        generated_tuples.append((x - i - 1, 1))
        generated_tuples.append((x - i - 2, 1))
    if even_int == 4:
        start = (4, 0)
    else:
        start = (4, 1)
    path = (
        [(0, 1), (0, 0)]
        + generated_tuples
        + [
            start,
            (4, 5),
            (0, 5),
            (0, 4),
            (3, 4),
            (3, 1),
            (2, 1),
            (2, 3),
            (0, 3),
            (0, 2),
            (1, 2),
            (1, 1),
        ]
    )
    path_x, path_y = zip(*path)

    # Draw highlighted path
    ax.plot(path_x, path_y, color="blue", linewidth=5)

    # Draw black circles at key points
    key_points = [(0, 1), (0, 0), (x, 0), (x, y), (0, y), (1, 1)]
    for point in key_points:
        ax.plot(*point, "ko", markersize=10)

    # Add text annotations
    annotations = {
        (0, y + 0.5): f'1{even_int*"0"}2',
        (x, y + 0.5): f'{even_int*"0"}12',
        (x, -0.5): f'2{even_int*"0"}1',
        (0, -0.5): f'21{even_int*"0"}',
        (0, 1.5): f'12{even_int*"0"}',
        (1, 0.5): f'021{(even_int-1)*"0"}',
    }
    for (x, y), text in annotations.items():
        ax.text(x, y, text, fontsize=12, ha="center", va="center")

    # Annotate points c and d
    ax.text(-0.25, 1, "c", fontsize=12, ha="right", va="center")
    ax.text(0.75, 1, "d", fontsize=12, ha="right", va="center")

    # Hide axes
    ax.axis("off")


def fig12(ax: Axes, even_int: int) -> None:
    """
    Generate and plot Figure 12 from Verhoeff's paper (see References). The figure displays a path between `a` and `b`:\n
        - `a0 = 12 0^{k_0-1} 1 0`
        - `b0 = 0 21 0^{k_0-2} 1 0`\n
    where `k_0` is an even integer (`even_int`). The path is highlighted in blue and important nodes are marked.

    Args:
        ax (Axes): The matplotlib Axes object to plot the figure on.
        even_int (int): An even integer value.

    Returns:
        None: Works in place to plot the figure on the given `ax`.

    References:
        - Tom Verhoeff. The spurs of D. H. Lehmer: Hamiltonian paths in neighbor-swap graphs of permutations. Designs, Codes, and Cryptography, 84(1-2):295-310, 7 2017.
    """
    diff_4 = even_int - 4

    # Set limits and aspect ratio
    x, y = 3 + diff_4, 5 + diff_4
    ax.set_xlim(-0.5, x + 0.5)
    ax.set_ylim(-0.5, y + 0.5)
    ax.set_aspect("equal")

    # Draw vertical lines
    for y_line in range(x + 1):
        ax.plot([y_line, y_line], [0, y], color="black", linewidth=1)

    # Draw horizontal lines except for the diagonal positions where x == y
    for y_line in range(y + 1):
        for x_line in range(x):
            if x_line != y_line - 1:
                ax.plot(
                    [x_line, x_line + 1], [y_line, y_line], color="black", linewidth=1
                )

    # Highlighted path coordinates
    generated_tuples = []
    for i in range(0, diff_4, 2):
        generated_tuples.append((x - i, i))
        generated_tuples.append((x - i, y - i))
        generated_tuples.append((0, y - i))
        generated_tuples.append((0, y - i - 1))
        generated_tuples.append((x - i - 1, y - i - 1))
        generated_tuples.append((x - i - 1, 1))
        generated_tuples.append((x - i - 2, 1))
    if even_int == 4:
        start = (3, 0)
    else:
        start = (3, 1)
    path = (
        [(0, 1), (0, 0)]
        + generated_tuples
        + [start, (3, 5), (0, 5), (0, 2), (1, 2), (1, 4), (2, 4), (2, 1), (1, 1)]
    )
    path_x, path_y = zip(*path)

    # Draw highlighted path
    ax.plot(path_x, path_y, color="blue", linewidth=5)

    # Draw black circles at key points
    key_points = [
        (0, 1),
        (0, 0),
        (x, 0),
        (x, y),
        (0, y),
        (1, 1),
        (x, y - 1),
        (x, y - 2),
    ]
    for point in key_points:
        ax.plot(*point, "ko", markersize=10)

    # Add text annotations
    odd_int = even_int - 1
    annotations = {
        (0, y + 0.5): f'1{odd_int*"0"}12',
        (x, y + 0.5): f'{odd_int*"0"}112',
        (x, -0.5): f'2{odd_int*"0"}11',
        (x - 0.1 + ((odd_int) * 0.25), y - 1): f'{odd_int*"0"}121',
        (x - 0.1 + ((odd_int) * 0.25), y - 2): f'{odd_int*"0"}211',
        (0, -0.5): f'21{odd_int*"0"}1',
        (0, 1.5): f'12{odd_int*"0"}1',
        (1, 0.5): f'021{(odd_int-1)*"0"}1',
    }
    for (x, y), text in annotations.items():
        ax.text(x, y, text, fontsize=12, ha="center", va="center")

    # Annotate points a and b
    ax.text(-0.25, 1, "a", fontsize=12, ha="right", va="center")
    ax.text(0.75, 1, "b", fontsize=12, ha="right", va="center")

    # Hide axes
    ax.axis("off")


def fig12_e_f(ax: Axes, even_int: int) -> None:
    """
    Generate and plot Figure 12 from Verhoeff's paper (see References). The figure displays a path between `e` and `f`:\n
        - `e0 = 1 02 0^{k_0-2} 1 0`
        - `f0 = 0 12 0^{k_0-2} 1 0`\n
    where `k_0` is an even integer (`even_int`). The path is highlighted in blue and important nodes are marked.

    Args:
        ax (Axes): The matplotlib Axes object to plot the figure on.
        even_int (int): An even integer value.

    Returns:
        None: Works in place to plot the figure on the given `ax`.

    References:
        - Tom Verhoeff. The spurs of D. H. Lehmer: Hamiltonian paths in neighbor-swap graphs of permutations. Designs, Codes, and Cryptography, 84(1-2):295-310, 7 2017.
    """
    diff_4 = even_int - 4

    # Set limits and aspect ratio
    x, y = 3 + diff_4, 5 + diff_4
    ax.set_xlim(-0.5, x + 0.5)
    ax.set_ylim(-0.5, y + 0.5)
    ax.set_aspect("equal")

    # Draw vertical lines
    for y_line in range(x + 1):
        ax.plot([y_line, y_line], [0, y], color="black", linewidth=1)

    # Draw horizontal lines except for the diagonal positions where x == y
    for y_line in range(y + 1):
        for x_line in range(x):
            if x_line != y_line - 1:
                ax.plot(
                    [x_line, x_line + 1], [y_line, y_line], color="black", linewidth=1
                )

    # Highlighted path coordinates
    generated_tuples = []
    for i in range(0, diff_4, 2):
        generated_tuples.append((x - i, i))
        generated_tuples.append((x - i, y - i))
        generated_tuples.append((0, y - i))
        generated_tuples.append((0, y - i - 1))
        generated_tuples.append((x - i - 1, y - i - 1))
        generated_tuples.append((x - i - 1, 1))
        generated_tuples.append((x - i - 2, 1))
    if even_int == 4:
        start = (3, 0)
    else:
        start = (3, 1)
    path = (
        [(0, 2), (0, 0)]
        + generated_tuples
        + [
            start,
            (3, 5),
            (0, 5),
            (0, 3),
            (1, 3),
            (1, 4),
            (2, 4),
            (2, 1),
            (1, 1),
            (1, 2),
        ]
    )
    path_x, path_y = zip(*path)

    # Draw highlighted path
    ax.plot(path_x, path_y, color="blue", linewidth=5)
    ax.plot([0, 1], [2, 2], color="orange", linewidth=5)

    # Draw black circles at key points
    key_points = [
        (0, 2),
        (0, 0),
        (x, 0),
        (x, y),
        (0, y),
        (1, 2),
        (x, y - 1),
        (x, y - 2),
    ]
    for point in key_points:
        ax.plot(*point, "ko", markersize=10)

    # Add text annotations
    odd_int = even_int - 1
    annotations = {
        (0, y + 0.5): f'1{odd_int*"0"}12',
        (x, y + 0.5): f'{odd_int*"0"}112',
        (x, -0.5): f'2{odd_int*"0"}11',
        (0, -0.5): f'21{odd_int*"0"}1',
        (((odd_int + 1.1) * -0.22), 2.0): f'e=102{(odd_int-1)*"0"}1',
        (0.8, 2.3): f'f=012{(odd_int-1)*"0"}1',
        (x - 0.1 + ((odd_int) * 0.25), y - 1): f'{odd_int*"0"}121',
        (x - 0.1 + ((odd_int) * 0.25), y - 2): f'{odd_int*"0"}211',
    }
    for (x, y), text in annotations.items():
        ax.text(x, y, text, fontsize=12, ha="center", va="center")

    # Annotate points e and f
    # ax.text(-0.25, 1, "a", fontsize=12, ha="right", va="center")
    # ax.text(0.75, 1, "b", fontsize=12, ha="right", va="center")
    # ax.text(-0.25, 2, "e", fontsize=12, ha="right", va="center")
    # ax.text(1.25, 2.25, "f", fontsize=12, ha="right", va="center")

    # Hide axes
    ax.axis("off")


def combined_figure(even_int: int, save: bool = False) -> None:
    """
    Generate and plot both Figure 11 and Figure 12 from Verhoeff's paper (see References) in a single plot.
    The figures display paths between `c` and `d` and between `a` and `b` respectively. The paths are highlighted in blue and important nodes are marked.

    Args:
        even_int (int): An even integer value.
        save (bool, optional): Save the image in the `./out` directory.

    Returns:
        None: Works in place to plot the figure.

    References:
        - Tom Verhoeff. The spurs of D. H. Lehmer: Hamiltonian paths in neighbor-swap graphs of permutations. Designs, Codes, and Cryptography, 84(1-2):295-310, 7 2017.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))

    # Draw both figures in the subplots
    fig11(ax1, even_int)
    fig12(ax2, even_int)

    # If save is enabled, save the figure
    if save:
        if not os.path.exists("./out"):
            os.makedirs("./out")
        plt.savefig(
            f"./out/VerhoeffCycleCover{even_int}EdgeCases.png",
            dpi=300,
            bbox_inches="tight",
        )
    else:
        # Show the combined plot
        plt.show()


def plot_individual_figures(
    even_int: int, save: bool = False, cycle: bool = False
) -> None:
    """
    Generate and plot Figure 11 and Figure 12 from Verhoeff's paper (see References) in separate plots.
    The figures display paths between `c` and `d` and between `a` and `b` respectively. The paths are highlighted in blue and important nodes are marked.
    If `save` is enabled, the images are saved in the `./out` directory. If not, the figures are displayed.

    Args:
        even_int (int): An even integer value, the number of 0s in the signature.
        save (bool, optional): Save the images in the `./out` directory. Defaults to `False` which displays the figures.
        cycle (bool, optional): Generate a cycle instead of a path. Default is `False`.

    Returns:
        None: Works in place to plot the figures.

    References:
        - Tom Verhoeff. The spurs of D. H. Lehmer: Hamiltonian paths in neighbor-swap graphs of permutations. Designs, Codes, and Cryptography, 84(1-2):295-310, 7 2017.
    """

    if cycle:
        fig, ax = plt.subplots()
        fig12_e_f(ax, even_int)
        if save:
            if not os.path.exists("./out"):
                os.makedirs("./out")
            plt.savefig(
                f"./out/Cycle{even_int-1}21And{even_int-1}11.png",
                dpi=300,
                bbox_inches="tight",
            )
        else:
            plt.show()
        return
    # Plot fig11
    fig, ax = plt.subplots()
    fig11(ax, even_int)
    if save:
        if not os.path.exists("./out"):
            os.makedirs("./out")
        plt.savefig(f"./out/Verhoeff{even_int}11.png", dpi=300, bbox_inches="tight")
    else:
        plt.show()

    # Plot fig12
    fig, ax = plt.subplots()
    fig12(ax, even_int)
    if save:
        if not os.path.exists("./out"):
            os.makedirs("./out")
        plt.savefig(
            f"./out/Verhoeff{even_int-1}21And{even_int-1}11.png",
            dpi=300,
            bbox_inches="tight",
        )
    else:
        plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate figures for Verhoeff's cycle cover edge cases."
    )
    parser.add_argument(
        "-e", "--even", type=int, required=True, help="Input even integer"
    )
    parser.add_argument(
        "-s", "--save", action="store_true", help="Save image in ./out directory"
    )
    parser.add_argument(
        "-m", "--merge", action="store_true", help="Merge the graphs into one plot"
    )
    parser.add_argument(
        "-c", "--cycle", action="store_true", help="Generate a cycle instead of a path"
    )

    args = parser.parse_args()

    if args.merge:
        combined_figure(args.even, args.save)
    else:
        plot_individual_figures(args.even, args.save, args.cycle)
