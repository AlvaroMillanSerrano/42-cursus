import sys

if __name__ == '__main__':
    i = len(sys.argv)
    print("=== Player Score Analytics ===")
    if i == 1:
        print(
            "No scores provided. Usage: python3 "
            "ft_score_analytics.py <score1> <score2> ...\n"
        )
    else:
        scores = []
        for n in range(1, i):
            scores.append(int(sys.argv[n]))
        print(f"Scores processed: {scores}")
        print(f"Total players: {len(scores)}")
        print(f"Total score: {sum(scores)}")
        print(f"Average score: {sum(scores) / len(scores)}")
        print(f"High score: {max(scores)}")
        print(f"Low score: {min(scores)}")
        print(f"Score range: {max(scores) - min(scores)}\n")
