from flask import Flask, request, jsonify
import numpy as np
import random
import json
import os


app = Flask(__name__)

GRID_SIZE = 100
POWER = 2


def idw_interpolation(sensor_data):
    """
    sensor_data = list of dicts:
    [
        {"x": float, "y": float, "aqi": float},
        ...
    ]
    """

    grid = np.zeros((GRID_SIZE, GRID_SIZE))

    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):

            # Normalize grid coordinates (0 → 1)
            x = i / (GRID_SIZE - 1)
            y = j / (GRID_SIZE - 1)

            numerator = 0
            denominator = 0
            exact_match = False

            for sensor in sensor_data:
                sx = sensor["x"]
                sy = sensor["y"]
                aqi = sensor["aqi"]

                dx = x - sx
                dy = y - sy
                distance = np.sqrt(dx * dx + dy * dy)

                #If grid point exactly equals sensor location
                if distance == 0:
                    grid[i][j] = aqi
                    exact_match = True
                    break

                weight = 1 / (distance ** POWER)

                numerator += weight * aqi
                denominator += weight

            if not exact_match:
                grid[i][j] = numerator / denominator

    return grid


@app.route('/generate_aqi', methods=['POST'])
def generate_aqi():

    data = request.get_json()

    sensor_data = data.get("sensors")

    if not sensor_data or len(sensor_data) < 1:
        return jsonify({"error": "Provide at least one sensor"}), 400

    grid = idw_interpolation(sensor_data)

    response = {
        "grid_size": GRID_SIZE,
        "aqi_matrix": grid.tolist(),
        "min": float(np.min(grid)),
        "max": float(np.max(grid))
    }

    return jsonify(response)


@app.route('/generate_population', methods=['GET'])
def generate_population():

    files = [
        "population_data/population_matrix_1.json",
        "population_data/population_matrix_2.json",
        "population_data/population_matrix_3.json"
    ]

    selected_file = random.choice(files)

    try:
        with open(selected_file, "r") as f:
            data = json.load(f)

        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)