from flask import Blueprint, request, jsonify
from app.models.db import prompts_collection, history_collection
from app.services.openai_service import get_ai_response
from datetime import datetime

ai_bp = Blueprint("ai", __name__)

@ai_bp.route("/")
def home():
    return "Server is running 🔥"

# =======================
# 🔥 ASK API
# =======================
@ai_bp.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.json
        user_input = data.get("userInput")

        if not user_input:
            return jsonify({"error": "userInput is required"}), 400

        # 🔹 Mongo se prompt uthao
        prompt = prompts_collection.find_one({"id": "Education Prompt"})

        if not prompt:
            return jsonify({"error": "Prompt not found"}), 404

        # 🔹 Template replace
        final_prompt = prompt["template"].replace("{{userInput}}", user_input)

        # 🔥 AI response
        response = get_ai_response(final_prompt)

        # 🔥 History save with time
        history_collection.insert_one({
            "input": user_input,
            "response": response,
            "createdAt": datetime.utcnow()
        })

        return jsonify({
            "response": response,
            "time": datetime.utcnow().isoformat()
        })

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": "Something went wrong"}), 500


# =======================
# 🔥 HISTORY API (separate)
# ======


@ai_bp.route("/history", methods=["GET"])
def get_history():
    try:
        data = list(history_collection.find().sort("createdAt", -1))

        result = []

        for item in data:
            obj = {
                "_id": str(item.get("_id")),
                "input": item.get("input"),
                "response": item.get("response"),
               "createdAt": datetime.utcnow()
            }

            # 🔥 SAFE datetime handling
            if "createdAt" in item and item["createdAt"]:
                try:
                    obj["createdAt"] = item["createdAt"].isoformat()
                except:
                    obj["createdAt"] = str(item["createdAt"])

            result.append(obj)

        return jsonify(result)

    except Exception as e:
        print("HISTORY ERROR:", str(e))   # 🔥 important
        return jsonify({"error": str(e)}), 500