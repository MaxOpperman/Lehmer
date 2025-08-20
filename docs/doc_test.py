import argparse
import ast
import os


def find_functions_with_docstring_issues(
    filename: str,
) -> list[
    tuple[
        str,
        list[str],
        list[str],
        list[str],
        str,
        str,
        list[tuple[str, str, str]],
        list[tuple[str, bool, bool]],
    ]
]:
    """
    Find the functions with issues in the docstring.

    Args:
        filename (str): The filename of the Python file to check for issues.

    Returns:
        list[tuple[str, list[str], list[str], list[str], str, str, list[tuple[str, str, str]], list[tuple[str, bool, bool]]]]:
            List of functions with issues in the docstring.
    """
    with open(filename, "r") as file:
        tree = ast.parse(file.read(), filename=filename)

    functions_with_issues = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if node.args.args:
                docstring = ast.get_docstring(node)
                if node.returns:
                    return_type_in_function = ast.unparse(node.returns)
                else:
                    return_type_in_function = "TODO"
                if docstring:
                    docstring_lines = docstring.split("\n")
                    params_in_docstring = []
                    params_type_in_docstring = []
                    optional_params_in_docstring = []
                    return_type_in_docstring = None
                    args_section = False
                    for i, line in enumerate(docstring_lines):
                        stripped_line = line.strip()
                        if stripped_line.startswith("Args:"):
                            args_section = True
                        elif stripped_line.startswith("Returns:"):
                            return_type_in_docstring = (
                                docstring_lines[i + 1].split(":")[0].strip()
                            )
                            break
                        elif args_section:
                            if (
                                stripped_line
                                and " " in stripped_line
                                and stripped_line.split()[1].startswith("(")
                                and stripped_line.split(":")[0].endswith(")")
                            ):
                                params_in_docstring.append(
                                    stripped_line.split()[0].rstrip(":")
                                )
                                param_type = stripped_line.split(":")[0].strip()
                                param_type = (
                                    " ".join(param_type.split()[1:])
                                    .strip()
                                    .lstrip("(")
                                    .rstrip(")")
                                )
                                if "optional" in param_type:
                                    optional_params_in_docstring.append(True)
                                    params_type_in_docstring.append(
                                        param_type.split(",")[0].strip()
                                    )
                                else:
                                    optional_params_in_docstring.append(False)
                                    params_type_in_docstring.append(param_type)
                    params_in_function = [arg.arg for arg in node.args.args]
                    params_type_in_function = [
                        ast.unparse(arg.annotation) if arg.annotation else "TODO"
                        for arg in node.args.args
                    ]
                    default_values_in_function = [False] * (
                        len(node.args.args) - len(node.args.defaults)
                    ) + [True] * len(node.args.defaults)
                    missing_params = [
                        param
                        for param in params_in_function
                        if param not in params_in_docstring
                    ]
                    if len(missing_params) > 0 and missing_params[0] == "self":
                        missing_params = missing_params[1:]
                        params_type_in_function = params_type_in_function[1:]
                        default_values_in_function = default_values_in_function[1:]
                    extra_params = [
                        param
                        for param in params_in_docstring
                        if param not in params_in_function
                    ]
                    return_type_mismatch = (
                        return_type_in_function != return_type_in_docstring
                    )
                    param_type_mismatches = []
                    if (
                        len(params_type_in_function) != len(params_type_in_docstring)
                        or len(
                            [
                                i
                                for i in range(len(params_type_in_function))
                                if params_type_in_function[i]
                                != params_type_in_docstring[i]
                            ]
                        )
                        > 0
                    ):
                        for i in range(len(params_type_in_function)):
                            if i < len(params_type_in_docstring) and i < len(
                                params_type_in_function
                            ):
                                if (
                                    params_type_in_function[i]
                                    != params_type_in_docstring[i]
                                ):
                                    param_type_mismatches.append(
                                        (
                                            params_in_function[i],
                                            params_type_in_function[i],
                                            params_type_in_docstring[i],
                                        )
                                    )
                            elif i >= len(params_type_in_function) and i < len(
                                params_type_in_docstring
                            ):
                                param_type_mismatches.append(
                                    (
                                        params_in_function[i],
                                        "TODO",
                                        params_type_in_docstring[i],
                                    )
                                )
                            else:
                                param_type_mismatches.append(
                                    (
                                        params_in_function[i],
                                        params_type_in_function[i],
                                        "TODO",
                                    )
                                )
                    param_optional_mismatches = []
                    if (
                        len(optional_params_in_docstring)
                        != len(default_values_in_function)
                        or len(
                            [
                                i
                                for i in range(len(optional_params_in_docstring))
                                if optional_params_in_docstring[i]
                                != default_values_in_function[i]
                            ]
                        )
                        > 0
                    ):
                        for i in range(len(optional_params_in_docstring)):
                            if i < len(default_values_in_function) and i < len(
                                optional_params_in_docstring
                            ):
                                if (
                                    optional_params_in_docstring[i]
                                    != default_values_in_function[i]
                                ):
                                    param_optional_mismatches.append(
                                        (
                                            params_in_function[i],
                                            default_values_in_function[i],
                                            default_values_in_function[i],
                                        )
                                    )
                            elif i >= len(default_values_in_function):
                                param_optional_mismatches.append(
                                    (
                                        params_in_function[i],
                                        "TODO",
                                        optional_params_in_docstring[i],
                                    )
                                )
                            else:
                                param_optional_mismatches.append(
                                    (
                                        params_in_function[i],
                                        default_values_in_function[i],
                                        "TODO",
                                    )
                                )
                    if (
                        missing_params
                        or extra_params
                        or return_type_mismatch
                        or len(param_type_mismatches) > 0
                        or len(param_optional_mismatches) > 0
                    ):
                        functions_with_issues.append(
                            (
                                node.name,
                                params_in_function,
                                missing_params,
                                extra_params,
                                return_type_in_function,
                                return_type_in_docstring,
                                param_type_mismatches,
                                param_optional_mismatches,
                            )
                        )
                elif (
                    not docstring
                    and node.name != "main"
                    and not (node.name.startswith("__") and node.name.endswith("__"))
                ):
                    functions_with_issues.append(
                        (
                            node.name,
                            [],
                            ["ALL"],
                            [],
                            return_type_in_function,
                            "TODO",
                            [],
                            [],
                        )
                    )
    return functions_with_issues


def find_all_python_files(directory: str) -> list[str]:
    """
    Find all Python files in the directory. Excludes: `venv`, `__pycache__`, and `permutation-software-master`

    Args:
        directory (str): The directory to check for Python files.

    Returns:
        list[str]: List of Python files in the directory.
    """
    python_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            # print(f"Checking file {file} - {root}, {_}")
            if (
                os.path.join(directory, "venv") in root
                or os.path.join(directory, ".venv") in root
                or os.path.join(directory, "__pycache__") in root
                or os.path.join(directory, "permutation-software-master") in root
            ):
                break
            if file.endswith(".py") and not file.startswith("test_"):
                python_files.append(os.path.join(root, file))
    return python_files


def main(directory: str, ignore_files: list[str]) -> None:
    """
    Main function to check the documentation in the Python files.

    Args:
        directory (str): The directory to check for Python files.
        ignore_files (list[str]): List of files to ignore.

    Returns:
        None: Prints the issues found in the documentation.
    """
    python_files = find_all_python_files(directory)
    # print(python_files)
    issues_count = 0
    for filename in python_files:
        if os.path.basename(filename).split(".")[0] in ignore_files or any(
            ignored_dir in os.path.abspath(filename).split(os.sep)
            for ignored_dir in ignore_files
        ):
            continue
        issues = find_functions_with_docstring_issues(filename)
        if issues:
            print(f"In file '{filename}'")
            for (
                func_name,
                _,
                missing_params,
                extra_params,
                return_type_in_function,
                return_type_in_docstring,
                param_type_mismatches,
                param_optional_mismatches,
            ) in issues:
                issues_count += 1
                # print(f"  Function '{func_name}' has parameters {params}.")
                if missing_params:
                    print(
                        f"    Function {func_name} is missing docstring for: {missing_params}"
                    )
                if extra_params:
                    print(
                        f"    Function {func_name} has an extra docstring for: {extra_params}"
                    )
                if return_type_in_function != return_type_in_docstring:
                    print(
                        f"    Function {func_name} has a mismatched return type: {return_type_in_function} != {return_type_in_docstring}"
                    )
                if len(param_type_mismatches) > 0:
                    for param, function_type, docstring_type in param_type_mismatches:
                        print(
                            f"    Function {func_name} has a mismatched type for parameter {param}: {function_type} != {docstring_type}"
                        )
                if len(param_optional_mismatches) > 0:
                    for (
                        param,
                        function_optional,
                        docstring_optional,
                    ) in param_optional_mismatches:
                        print(
                            f"    Function {func_name} has a mismatched optional for parameter {param}: {function_optional} != {docstring_optional}"
                        )
    if issues_count == 0:
        print("No issues found with the documentation!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Test the correctness of the documentation in the Python files."
    )
    parser.add_argument(
        "-p",
        "--path",
        type=str,
        help="Path of the parent directory",
    )
    parser.add_argument(
        "-i",
        "--ignore-files",
        type=str,
        help="Comma-separated files to ignore (without the path or .py extension)",
    )
    args = parser.parse_args()

    ignore_files = []
    if args.ignore_files:
        ignore_files = args.ignore_files.split(",")

    # check if the path is provided, otherwise use the current directory
    if args.path:
        main(args.path, ignore_files)
    else:
        main(".", ignore_files)
