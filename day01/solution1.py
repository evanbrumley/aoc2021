def main():
    with open("input", "r") as f:
        numbers_raw = f.read()

    numbers = [int(num) for num in numbers_raw.splitlines() if num]

    last_num = None
    count = 0

    for num in numbers:
        if last_num is not None and num > last_num:
            count += 1

        last_num = num

    print(count)


if __name__ == "__main__":
    main()
