scores = [70, 60, 80, 90, 50]
filtered = filter(lambda score: score == 70, scores)

print(len(list(filtered)))
