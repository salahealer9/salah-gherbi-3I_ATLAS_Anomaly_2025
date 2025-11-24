import matplotlib.pyplot as plt

def photometric_anomaly(delta_m_obs, delta_m_geo):
    R = delta_m_obs / delta_m_geo
    return max(0.0, min(1.0, (R - 1.0) / 2.0))

def chromatic_anomaly(delta_color_max, baseline=0.2, span=0.5):
    # baseline ~ typical comet variation, span ~ anomaly range
    return max(0.0, min(1.0, (delta_color_max - baseline) / span))

def acceleration_anomaly(ng_detected, delta_t_days, t_scale=30.0):
    B_ng = 1.0 if ng_detected else 0.0
    T = max(0.0, min(1.0, delta_t_days / t_scale))
    return 0.5 * B_ng + 0.5 * T

def morphology_anomaly(level):
    """
    level: 0 = normal comet (coma+tail)
           0.5 = weak coma / marginal tail
           1 = point-like despite strong activity
    """
    return max(0.0, min(1.0, level))

def atlas_anomaly_index(
    delta_m_obs, delta_m_geo,
    delta_color_max,
    ng_detected, delta_t_days,
    morph_level,
    weights=None
):
    A_p = photometric_anomaly(delta_m_obs, delta_m_geo)
    A_c = chromatic_anomaly(delta_color_max)
    A_a = acceleration_anomaly(ng_detected, delta_t_days)
    A_m = morphology_anomaly(morph_level)

    axes = [A_p, A_c, A_a, A_m]

    if weights is None:
        weights = [0.25, 0.25, 0.25, 0.25]

    score = sum(w * a for w, a in zip(weights, axes))
    return score, dict(A_p=A_p, A_c=A_c, A_a=A_a, A_m=A_m)

# Example for 3I/ATLAS (approximate values)
delta_m_obs = 4.2
delta_m_geo = 1.5
delta_color_max = 0.72
ng_detected = True
delta_t_days = 30.0
morph_level = 0.9

score, components = atlas_anomaly_index(
    delta_m_obs, delta_m_geo,
    delta_color_max,
    ng_detected, delta_t_days,
    morph_level
)

print("Anomaly Index (0–1):", score)
print("Components:", components)

# Plotting section - using the components returned from the function
component_names = {
    "Photometric\n$A_p$": components["A_p"],
    "Chromatic\n$A_c$": components["A_c"], 
    "Acceleration\n$A_a$": components["A_a"],
    "Morphology\n$A_m$": components["A_m"],
}

labels = list(component_names.keys())
values = list(component_names.values())

plt.figure(figsize=(6, 4))
plt.bar(labels, values)
plt.ylim(0, 1.05)
plt.ylabel("Anomaly component value")
plt.title("Interstellar Anomaly Components for 3I/ATLAS")

# Optional: horizontal reference lines
plt.axhline(0.25, linestyle="--", alpha=0.3)
plt.axhline(0.5, linestyle="--", alpha=0.3)
plt.axhline(0.75, linestyle="--", alpha=0.3)

plt.tight_layout()
plt.savefig("atlas_anomaly_components.png", dpi=300)
plt.show()