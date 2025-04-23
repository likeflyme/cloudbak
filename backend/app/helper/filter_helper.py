type_mapping = {
    1: [[49, 6]],
    2: [[3, 0], [43, 0]],
    3: [[49, 1]],
    4: [[49, 76]],
    5: [[49, 33]],
    6: [[49, 63]]
}


def convert_type(filter_type: int):
    return type_mapping[filter_type]
