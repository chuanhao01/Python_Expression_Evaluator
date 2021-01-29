
class Sort:
    def __init__(self, expr_list):
        self.list = expr_list

    def error(self, sort_by):
        raise NotImplementedError(f"Sorting by {sort_by} has not been implemented yet!!")

    def sort(self, sort_by):
        if sort_by == "value":
            self.merge_sort()

        elif sort_by == "length":
            self.bubble_sort()

        else:
            self.error(sort_by)

    def merge_sort(self):
        pass

    def bubble_sort(self):
        pass