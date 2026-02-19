def calc(num1, num2, op):
    if op == "+":
        return num1 + num2
    elif op == "-":
        return num1 - num2
    elif op == "*":
        return num1 * num2
    elif op == "/":
        if num2 != 0:
            return num1 / num2
        else:
            return "нельзя делить на 0"
    else:
        return "неверная операция!"


def main():
    num1 = float(input("введите первое число: "))
    op = input("введите операцию (+, -, *, /): ")
    num2 = float(input("введите второе число: "))
    result = calc(num1, num2, op)
    print("Результат:", result)


if __name__ == "__main__":
    main()
