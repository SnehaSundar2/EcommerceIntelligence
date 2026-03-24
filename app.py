from flask import Flask, jsonify
from processing.data_processor import load_data
from ai_engine.decision_engine import analyze_data
from database.db import save_data, save_insights   # 👈 ADD THIS

app = Flask(__name__)

@app.route("/")
def run_pipeline():
    try:
        # 1. Load data
        data = load_data("data/dataset.csv")

        # 2. Save raw data to DB
        save_data(data)

        # 3. Run AI logic
        results = analyze_data(data)

        # 4. Save insights to DB 👇
        save_insights(results)

        return jsonify({
            "status": "Pipeline executed successfully ✅",
            "total_records": len(data),
            "insights_generated": len(results),
            "results": results
        })

    except Exception as e:
        return jsonify({
            "status": "Error ❌",
            "message": str(e)
        })


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)