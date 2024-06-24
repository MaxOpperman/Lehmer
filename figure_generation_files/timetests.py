import argparse
import os
import re
from argparse import Namespace

import numpy as np
import perfplot

import stachowiak
import type_variations.stachowiak_list
import type_variations.stachowiak_list_verhoeff_tuple
import type_variations.stachowiak_numpy
import type_variations.stachowiak_tuple_verhoeff_list
from helper_operations.permutation_graphs import multinomial


class TimeTests:
    signatures = None
    signatures_l2 = [
        [1, 1, 24],
        [1, 1, 22],
        [1, 1, 20],
        [1, 1, 18],
        [1, 1, 16],
        [1, 1, 14],
    ]
    signatures_verhoeff = [
        [11, 9],
        [9, 11],
        [11, 7],
        [7, 11],
        [9, 9],
        [11, 5],
        [9, 7],
        [13, 5],
    ]
    signatures_sjt = [
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
    ]
    sigantures_stachowiak = [
        [3, 3, 4, 1],
        [3, 3, 3, 2],
        [3, 3, 1, 1, 1, 1],
        [3, 3, 3, 1, 1],
        [3, 3, 2, 2, 1],
        [3, 3, 2, 1, 1],
        [3, 3, 4, 2],
    ]

    @staticmethod
    def setup(n):
        return TimeTests.signatures[n]


def time_tests(args: Namespace):
    if not os.path.exists("./out") and (args.graph or args.latex):
        os.makedirs("./out")
    for l11_type in ["Lemma2", "Verhoeff", "SJT", "Stachowiak"]:
        file_name = f"_{l11_type}"
        if args.numpy:
            file_name += "_numpy"
        else:
            file_name += "_without_numpy"
        if l11_type == "Lemma2":
            signature_type = "Stachowiak Lemma 2"
            TimeTests.signatures = sorted(TimeTests.signatures_l2, key=multinomial)
        elif l11_type == "Verhoeff":
            signature_type = "Verhoeff's binary case"
            TimeTests.signatures = sorted(
                TimeTests.signatures_verhoeff, key=multinomial
            )
        elif l11_type == "SJT":
            signature_type = "Steinhaus-Johnson-Trotter (permutahedron)"
            TimeTests.signatures = sorted(TimeTests.signatures_sjt, key=multinomial)
        elif l11_type == "Stachowiak":
            signature_type = "Stachowiak's theorem"
            TimeTests.signatures = sorted(
                TimeTests.sigantures_stachowiak, key=multinomial
            )
        else:
            print("Invalid test type", l11_type, "not in list")
            break
        print(f"Performing time tests for {signature_type}")

        def wrapper_list(kernel, input):
            return kernel(input)

        def wrapper_numpy(kernel, input):
            return kernel(np.array(input))

        def get_kernels():
            kernels = [
                lambda input: wrapper_list(
                    type_variations.stachowiak_list.lemma11, input
                ),
                lambda input: wrapper_list(stachowiak.lemma11, input),
                lambda input: wrapper_list(
                    type_variations.stachowiak_tuple_verhoeff_list.lemma11, input
                ),
                lambda input: wrapper_list(
                    type_variations.stachowiak_list_verhoeff_tuple.lemma11, input
                ),
            ]
            if args.numpy:
                return kernels + [
                    lambda input: wrapper_numpy(
                        type_variations.stachowiak_numpy.lemma11, input
                    ),
                ]
            else:
                return kernels

        # Save the graph
        results = perfplot.bench(
            setup=TimeTests.setup,
            n_range=[i for i in range(len(TimeTests.signatures))],
            kernels=get_kernels(),
            labels=[
                "Stachowiak & Verhoeff lists",
                "Stachowiak & Verhoeff tuples",
                "Stachowiak tuples, Verhoeff lists",
                "Stachowiak lists, Verhoeff tuples",
                # "Stachowiak & Verhoeff numpy",
            ],
            xlabel=re.sub(
                "(.{80})",
                "\\1\n",
                f"Signatures {TimeTests.signatures}",
                0,
                re.DOTALL,
            ),
            equality_check=None,
        )

        y_coordinates_dict = results

        if args.graph:
            results.save(
                f"./out/lemma11_comparison{file_name}.png",
            )
        if args.latex:
            with open(f"./out/table{file_name}.tex", "w") as file:
                file.write("\\begin{table}[!htpb]\n")
                file.write("\\centering\n")
                file.write("\\begin{tabular}{c|c|c|c|c|c}\n")
                file.write("\\hline\n")
                file.write(
                    "n & Signature & Stachowiak's theorem with lists & Stachowiak's theorem with tuples & Stachowiak tuples, Verhoeff lists \\\\\n"
                )
                file.write("\\hline\n")
                for n, t in zip(
                    y_coordinates_dict.n_range, y_coordinates_dict.timings_s.T
                ):
                    lst = [str(n), f"{TimeTests.signatures[n]}"] + [
                        f"\\textcolor{{red}}{{{str(tt)}}}" if tt == min(t) else str(tt)
                        for tt in t
                    ]
                    file.write(" & ".join(lst) + " \\\\\n")
                file.write("\\hline\n")
                file.write("\\end{tabular}\n")
                file.write(
                    f"\\caption{{Time tests results for functions of {signature_type}}}\n"
                )
                file.write(f"\\label{{tab: timeTests{file_name}}}\n")
                file.write("\\end{table}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Helper tool to find paths through permutation neighbor swap graphs."
    )
    parser.add_argument(
        "-l",
        "--latex",
        action="store_true",
        help="Generate LaTeX tables for the results",
    )
    parser.add_argument(
        "-g", "--graph", action="store_true", help="Generate graphs for the results"
    )
    parser.add_argument(
        "-n", "--numpy", action="store_true", help="Incluce numpy in the tests"
    )

    args = parser.parse_args()
    time_tests(args)