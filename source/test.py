class Id:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        s = ""
        x = self.value
        if x==0:
            s = 'a'+s
        while x > 0:
            y = (x) % 26
            s = chr(ord('a') + y) + s
            x = (x - 1) // 26

        return s

# Example usage:
my_id = Id(0)  # You can replace this with any numeric value
formatted_id = str(my_id)
print(formatted_id)