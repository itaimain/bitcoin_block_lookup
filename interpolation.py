from typing import NamedTuple, Optional, Sequence


class Result(NamedTuple):
    previous_index: Optional[int]
    next_index: Optional[int]


def interpolation_nearby_lookup(arr: Sequence, target_value: int) -> Result:
    low_index = 0
    high_index = len(arr) - 1

    low_value = arr[0]
    high_value = arr[-1]

    if target_value <= low_value:
        return Result(-1, low_index)
    elif target_value >= high_value:
        return Result(high_index, None)

    while (high_index - low_index > 1 and target_value > low_value
           and target_value < high_value):

        pos_index = round(low_index + ((high_index - low_index) /
                                       (high_value - low_value)) *
                          (target_value - low_value))

        if high_index == pos_index or low_index == pos_index:
            pos_index = round((high_index + low_index) / 2)

        pos_value = arr[pos_index]

        if pos_value == target_value:
            return Result(pos_index, pos_index + 1)

        if pos_value < target_value:
            low_index = pos_index
            low_value = pos_value
        else:
            high_index = pos_index
            high_value = pos_value

    return Result(low_index, high_index)
