def main():
    with open("input", "r") as f:
        numbers_raw = f.read()

    numbers = [int(num) for num in numbers_raw.splitlines() if num]

    last_sum = None
    count = 0

    for window in iter_window(numbers, 3):
        this_sum = sum(window)
        if last_sum is not None and this_sum > last_sum:
            count += 1

        last_sum = this_sum

    print(count)


def iter_window(sequence, window_size):
    for i in range(len(sequence) - window_size + 1):
        yield sequence[i: i + window_size]


if __name__ == "__main__":
    main()
