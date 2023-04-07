def safely_remove_list_indexes(list_to_edit, list_of_indexes: list) -> list:

    for index in sorted(list_of_indexes, reverse=True):
        if 0 <= index < len(list_to_edit):
            list_to_edit.pop(index)

    return list_to_edit

