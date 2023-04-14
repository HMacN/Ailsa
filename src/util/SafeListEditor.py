def safely_remove_list_indexes(list_to_edit, list_of_indexes: list) -> list:
    """
    A helper function to safely remove a list of indices from a list.

    @param list_to_edit:        A list object to remove values from.
    @param list_of_indexes:     A list of int values which are the indices to remove in the given list.
    @return:                    The given list, with the relevant values removed.
    """

    for index in sorted(list_of_indexes, reverse=True):
        if 0 <= index < len(list_to_edit):
            list_to_edit.pop(index)

    return list_to_edit

