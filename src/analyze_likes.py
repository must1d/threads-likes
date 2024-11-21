import json

from threads_likes import DATA_PATH

DATA_FILE = DATA_PATH / "likes_data.json"

if __name__ == "__main__":

    with DATA_FILE.open("w") as f:
        data = json.load(f)

    data = {int(k): v for k, v in data.items()}
    sorted_data = dict(sorted(data.items(), reverse=True))

    num_threads = len(sorted_data)

    users = {}

    for i, likes in enumerate(sorted_data.values()):
        for user in likes:
            if user not in users:
                users[user] = (1, i)
            else:
                users[user] = (users[user][0] + 1, users[user][1])

    overall_percentages = {
        user: likes / num_threads for user, (likes, _) in users.items()
    }
    percentages_since_first = {
        user: likes / (num_threads - begin) for user, (likes, begin) in users.items() if begin <= 0.9 * num_threads
    }  # very new likers are excluded from this analysis

    overall_percentages_sorted = dict(
        sorted(overall_percentages.items(), key=lambda item: item[1], reverse=True)
    )
    percentages_since_first_sorted = dict(
        sorted(percentages_since_first.items(), key=lambda item: item[1], reverse=True)
    )

    print("Overall Like Percentages")
    for i, (user, percentage) in enumerate(overall_percentages_sorted.items()):
        if i == 10:
            break
        print(f"{i + 1}. @{user}: {100 * percentage:.2f}%")

    print("\nPercentages Since First Like")
    for i, (user, percentage) in enumerate(percentages_since_first_sorted.items()):
        if i == 10:
            break
        print(f"{i + 1}. @{user}: {100 * percentage:.2f}%")
