import re
import perfplot
from permutation_graphs import multinomial
import stachowiak
import perfplot
import stachowiak
import type_variations.stachowiak_list
import type_variations.stachowiak_tuple_verhoeff_list
import type_variations.stachowiak_list_verhoeff_tuple
import os


class TimeTests:
    signatures = None
    signatures_l2 = [
        [1, 1, 4, 2, 2],
        [1, 1, 2, 3, 2],
        [1, 1, 2, 1, 1, 1, 1],
        [1, 1, 2, 6, 1],
        [1, 1, 2, 4, 2],
        [1, 1, 2, 5, 1],
        [1, 1, 4, 1, 1, 1],
        [1, 1, 6, 2, 1],
        [1, 1, 8, 3],
        [1, 1, 6, 4],
        [1, 1, 4, 6],
        [1, 1, 12, 2],
        [1, 1, 10, 1, 1],
    ]
    signatures_verhoeff = [
        [3, 3, 2, 2],
        [5, 5, 1, 1],
        [5, 3, 2, 1],
        [7, 3, 3],
        [3, 3, 7],
        [3, 3, 4, 1],
        [7, 7, 1],
        [3, 3, 2, 1, 1],
        [5, 3, 1, 1, 1],
        [3, 3, 8],
    ]
    signatures_sjt = [
        [1, 1, 1, 1, 1, 1, 2],
        [1, 1, 1, 1, 10],
        [1, 1, 1, 30],
        [1, 1, 1, 1, 1, 5],
        [1, 1, 1, 1, 11],
    ]

    @staticmethod
    def setup(n):
        return TimeTests.signatures[n]


for l11_type in ["Lemma2", "Verhoeff", "SJT"]:
    if l11_type == "Lemma2":
        signature_type = "Stachowiak Lemma 2"
        TimeTests.signatures = sorted(TimeTests.signatures_l2, key=multinomial)
    elif l11_type == "Verhoeff":
        signature_type = "Verhoeff"
        TimeTests.signatures = sorted(TimeTests.signatures_verhoeff, key=multinomial)
    elif l11_type == "SJT":
        signature_type = "Steinhaus-Johnson-Trotter"
        TimeTests.signatures = sorted(TimeTests.signatures_sjt, key=multinomial)
    else:
        print("Invalid test type", l11_type, "not in list")
        break
    print(f"Performing time tests for {signature_type}")

    # Save the graph
    results = perfplot.bench(
        setup=TimeTests.setup,
        n_range=[i for i in range(len(TimeTests.signatures))],
        kernels=[
            type_variations.stachowiak_list.lemma11,
            stachowiak.lemma11,
            type_variations.stachowiak_tuple_verhoeff_list.lemma11,
            type_variations.stachowiak_list_verhoeff_tuple.lemma11,
        ],
        labels=["Stachowiak & Verhoeff lists", "Stachowiak & Verhoeff tuples",
                "Stachowiak tuples, Verhoeff lists", "Stachowiak lists, Verhoeff tuples"],
        xlabel=re.sub(
            "(.{80})", "\\1\n", f"Signatures {TimeTests.signatures}", 0, re.DOTALL,
        ),
    )

    y_coordinates_dict = results
    print(y_coordinates_dict)
    if not os.path.exists("./out"):
        os.makedirs("./out")
    with open(f"./out/table{signature_type}.tex", "w") as file:
        file.write("\\begin{table}[!htpb]\n")
        file.write("\\centering\n")
        file.write("\\begin{tabular}{c|c|c|c|c|c}\n")
        file.write("\\hline\n")
        file.write("n & Signature & Stachowiak's theorem with lists & Stachowiak's theorem with tuples & Stachowiak tuples, Verhoeff lists \\\\\n")
        file.write("\\hline\n")
        for n, t in zip(y_coordinates_dict.n_range, y_coordinates_dict.timings_s.T):
            lst = [str(n), f"{TimeTests.signatures[n]}"] + [f"\\textcolor{{red}}{{{str(tt)}}}" if tt == min(t) else str(tt) for tt in t]
            file.write(" & ".join(lst) + " \\\\\n")
        file.write("\\hline\n")
        file.write("\\end{tabular}\n")
        file.write(f"\\caption{{Time tests results for {signature_type}}}\n")
        file.write(f"\\label{{tab: timeTests{l11_type}}}\n")
        file.write("\\end{table}\n")
    
    results.save(
        f"./out/lemma11_comparison{l11_type}.png",
    )