import matplotlib.pyplot as plt
import os
import argparse


def fig11(ax, even_int: int):
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


def fig12(ax, even_int: int):
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
    key_points = [(0, 1), (0, 0), (x, 0), (x, y), (0, y), (1, 1)]
    for point in key_points:
        ax.plot(*point, "ko", markersize=10)

    # Add text annotations
    odd_int = even_int - 1
    annotations = {
        (0, y + 0.5): f'1{odd_int*"0"}12',
        (x, y + 0.5): f'{odd_int*"0"}112',
        (x, -0.5): f'2{odd_int*"0"}11',
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


def combined_figure(even_int: int, save=False):
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


def plot_individual_figures(even_int: int, save=False):
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
        description="Helper tool to create Hamiltonian paths."
    )
    parser.add_argument(
        "-e", "--even", type=int, required=True, help="Input even integer"
    )
    parser.add_argument(
        "-s", "--save", action="store_true", help="Save image in ./out directory"
    )
    parser.add_argument(
        "-c", "--combine", action="store_true", help="Combine the graphs into one plot"
    )

    args = parser.parse_args()

    if args.combine:
        combined_figure(args.even, args.save)
    else:
        plot_individual_figures(args.even, args.save)
