import math

def calculate_discriminant(a, b, c):
    return b**2 - 4*a*c

def solve_quadratic(a, b, c):
    discriminant = calculate_discriminant(a, b, c)
    if discriminant < 0:
        return discriminant, "Нет решений в действительных числах."
    elif discriminant == 0:
        x = -b / (2*a)
        return discriminant, f"Один корень: x = {x:.2f}"
    else:
        x1 = (-b + math.sqrt(discriminant)) / (2*a)
        x2 = (-b - math.sqrt(discriminant)) / (2*a)
        return discriminant, f"Два корня: x1 = {x1:.2f}, x2 = {x2:.2f}"
