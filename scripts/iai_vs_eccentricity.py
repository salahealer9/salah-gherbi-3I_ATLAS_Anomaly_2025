import matplotlib.pyplot as plt

objects = [
    {"name": "JFC",       "e": 0.5,  "iai": 0.03},
    {"name": "LPC",       "e": 0.99, "iai": 0.08},
    {"name": "1I/'Oumuamua",      "e": 1.20, "iai": 0.45},
    {"name": "2I/Borisov",        "e": 3.36, "iai": 0.16},
    {"name": "3I/ATLAS",          "e": 6.14, "iai": 0.95},
]

ecc = [obj["e"] for obj in objects]
iai = [obj["iai"] for obj in objects]
labels = [obj["name"] for obj in objects]

plt.figure(figsize=(6, 4))

# Plot points (once is enough)
for obj in objects:
    size = 80 if "ATLAS" in obj["name"] else 40
    plt.scatter(obj["e"], obj["iai"], s=size)

# Custom offsets per label (in points)
offsets = {
    "JFC":   (-8,  4),   # left and slightly up
    "LPC":   (8, -8),  # right and down
    "1I/'Oumuamua":  (8,  6),
    "2I/Borisov":    (8, -10),
    "3I/ATLAS":      ( 8,  4),
}

# Custom horizontal alignment depending on offset
for e, a, name in zip(ecc, iai, labels):
    dx, dy = offsets.get(name, (5, 5))
    ha = 'right' if dx < 0 else 'left'
    plt.annotate(
        name,
        (e, a),
        textcoords="offset points",
        xytext=(dx, dy),
        ha=ha,
        va='center',
        fontsize=8,
    )

plt.xlabel("Orbital eccentricity $e$")
plt.ylabel("Interstellar Anomaly Index (IAI)")
plt.title("IAI vs. Orbital Eccentricity")

plt.ylim(0.0, 1.05)
plt.xlim(0.0, 7.0)

plt.tight_layout()
plt.savefig("iai_vs_eccentricity.png", dpi=300)
plt.close()
