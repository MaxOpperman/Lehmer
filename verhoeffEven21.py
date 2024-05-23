import argparse
import matplotlib.pyplot as plt


def fig11(even_int: int):
    diff_4 = even_int - 4
    # Create figure and axes
    fig, ax = plt.subplots()

    # Set limits and aspect ratio
    x, y = 4+diff_4, 5+diff_4
    ax.set_xlim(-0.5, x+0.5)
    ax.set_ylim(-0.5, y+0.5)
    ax.set_aspect('equal')

    # Draw vertical lines
    for y_line in range(x + 1):
        ax.plot([y_line, y_line], [0, y], color='black', linewidth=1)

    # Draw horizontal lines except for the diagonal positions where x == y
    for y_line in range(y + 1):
        for x_line in range(even_int):
            if x != y:
                ax.plot([x_line, x_line + 1], [y_line, y_line], color='black', linewidth=1)

    # Highlighted path coordinates
    generated_tuples = []
    for i in range(0, diff_4, 2):
        generated_tuples.append((x-i, i))
        generated_tuples.append((x-i, y-i))
        generated_tuples.append((0, y-i))
        generated_tuples.append((0, y-i-1))
        generated_tuples.append((x-i-1, y-i-1))
        generated_tuples.append((x-i-1, 1))
        generated_tuples.append((x-i-2, 1))
    if even_int == 4:
        start = (4, 0)
    else:
        start = (4, 1)
    path = [(0, 1), (0, 0)] + generated_tuples + [start, (4, 5), (0, 5), (0, 4), (3, 4), (3, 1), (2, 1), (2, 3), (0, 3), (0, 2), (1, 2), (1, 1)]
    path_x, path_y = zip(*path)

    # Draw highlighted path
    ax.plot(path_x, path_y, color='blue', linewidth=5)

    # Draw black circles at key points
    key_points = [(0, 1), (1, 1)]
    for point in key_points:
        ax.plot(*point, 'ko', markersize=10)

    # Add text annotations
    annotations = {
        (0, y+0.5): f'1{even_int*"0"}2',
        (x, y+0.5): f'{even_int*"0"}12',
        (x, -0.5): f'2{even_int*"0"}1',
        (0, -0.5): f'21{even_int*"0"}',
        (0, 1.5): f'12{even_int*"0"}',
        (1, 0.5): f'021{(even_int-1)*"0"}',
    }
    for (x, y), text in annotations.items():
        ax.text(x, y, text, fontsize=12, ha='center', va='center')

    # Annotate points c and d
    ax.text(-0.5, 1, 'c', fontsize=12, ha='right', va='center')
    ax.text(1.5, 1, 'd', fontsize=12, ha='right', va='center')

    # Hide axes
    ax.axis('off')

    # Show plot
    plt.show()

if __name__ == "__main__":
    lehmer_strategy_help = "Default: random choices\r\n"
    parser = argparse.ArgumentParser(description="Helper tool to create a Hamiltonian path from 120^{k0} to 0210^{k0-1}.")
    parser.add_argument("-e", "--even", type=str, help="Input even integer")
    fig11(int(parser.parse_args().even))
