from core.cycle_cover import get_connected_cycle_cover
from core.helper_operations.cycle_cover_connections import generate_end_tuple_order


def generate_cycles(signature: tuple[int, ...]) -> list[list[tuple[int, ...]]]:
    """Generate the cycle structure for a given signature."""
    return get_connected_cycle_cover(signature)


def get_end_tuple_order(signature: tuple[int, ...]) -> list[tuple[int, ...]]:
    """Get the order of end tuples in the cycle cover."""
    return generate_end_tuple_order(signature)
