from flask import Blueprint, current_app, jsonify, request

from backend.db_connection import get_db

admin_routes = Blueprint("admin_routes", __name__)


# ---------- /reports ----------

@admin_routes.route("/reports", methods=["GET"])
def get_reports():
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM reports ORDER BY created_at DESC")
        return jsonify(cursor.fetchall()), 200
    finally:
        cursor.close()


@admin_routes.route("/reports", methods=["POST"])
def create_report():
    data = request.json
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            """INSERT INTO reports
               (created_by_user_id, offender_user_id, offender_type,
                offender_reference_id, report_text)
               VALUES (%s, %s, %s, %s, %s)""",
            (
                data["created_by_user_id"],
                data.get("offender_user_id"),
                data["offender_type"],
                data.get("offender_reference_id"),
                data["report_text"],
            ),
        )
        db.commit()
        return jsonify({"report_id": cursor.lastrowid}), 201
    finally:
        cursor.close()


@admin_routes.route("/reports", methods=["PUT"])
def update_report_status():
    data = request.json
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            """UPDATE reports
               SET report_status = %s, handled_by_admin_id = %s,
                   resolved_at = CASE WHEN %s = 'resolved' THEN NOW() ELSE resolved_at END,
                   resolution_notes = %s
               WHERE report_id = %s""",
            (
                data["report_status"],
                data.get("handled_by_admin_id"),
                data["report_status"],
                data.get("resolution_notes"),
                data["report_id"],
            ),
        )
        db.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Report not found"}), 404
        return jsonify({"message": "Report updated"}), 200
    finally:
        cursor.close()


@admin_routes.route("/reports", methods=["DELETE"])
def delete_report():
    data = request.json
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM reports WHERE report_id = %s", (data["report_id"],))
        db.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Report not found"}), 404
        return jsonify({"message": "Report deleted"}), 200
    finally:
        cursor.close()


# ---------- /servers ----------

@admin_routes.route("/servers", methods=["GET"])
def get_servers():
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM servers ORDER BY server_name")
        return jsonify(cursor.fetchall()), 200
    finally:
        cursor.close()


@admin_routes.route("/servers", methods=["POST"])
def create_server():
    data = request.json
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            """INSERT INTO servers (server_name, region, environment, status, capacity_percent)
               VALUES (%s, %s, %s, %s, %s)""",
            (
                data["server_name"],
                data["region"],
                data.get("environment", "production"),
                data.get("status", "healthy"),
                data.get("capacity_percent", 0.00),
            ),
        )
        db.commit()
        return jsonify({"server_id": cursor.lastrowid}), 201
    finally:
        cursor.close()


# ---------- /servers/<id> ----------

@admin_routes.route("/servers/<int:server_id>", methods=["GET"])
def get_server(server_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM servers WHERE server_id = %s", (server_id,))
        server = cursor.fetchone()
        if not server:
            return jsonify({"error": "Server not found"}), 404
        return jsonify(server), 200
    finally:
        cursor.close()


@admin_routes.route("/servers/<int:server_id>", methods=["PUT"])
def update_server(server_id):
    data = request.json
    db = get_db()
    cursor = db.cursor()
    try:
        fields, values = [], []
        for col in ("server_name", "region", "environment", "status", "capacity_percent"):
            if col in data:
                fields.append(f"{col} = %s")
                values.append(data[col])
        if not fields:
            return jsonify({"error": "No fields to update"}), 400
        values.append(server_id)
        cursor.execute(
            f"UPDATE servers SET {', '.join(fields)} WHERE server_id = %s", values
        )
        db.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Server not found"}), 404
        return jsonify({"message": "Server updated"}), 200
    finally:
        cursor.close()


@admin_routes.route("/servers/<int:server_id>", methods=["DELETE"])
def delete_server(server_id):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM servers WHERE server_id = %s", (server_id,))
        db.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Server not found"}), 404
        return jsonify({"message": "Server deleted"}), 200
    finally:
        cursor.close()


# ---------- /servers/<id>/alerts ----------

@admin_routes.route("/servers/<int:server_id>/alerts", methods=["GET"])
def get_server_alerts(server_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT * FROM alerts WHERE server_id = %s ORDER BY recorded_at DESC",
            (server_id,),
        )
        return jsonify(cursor.fetchall()), 200
    finally:
        cursor.close()


@admin_routes.route("/servers/<int:server_id>/alerts", methods=["POST"])
def create_alert(server_id):
    data = request.json
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            """INSERT INTO alerts (server_id, alert_severity, alert_type, alert_message)
               VALUES (%s, %s, %s, %s)""",
            (server_id, data["alert_severity"], data["alert_type"], data["alert_message"]),
        )
        db.commit()
        return jsonify({"alert_id": cursor.lastrowid}), 201
    finally:
        cursor.close()


@admin_routes.route("/servers/<int:server_id>/alerts", methods=["PUT"])
def update_server_alert(server_id):
    data = request.json
    db = get_db()
    cursor = db.cursor()
    try:
        fields, values = [], []
        for col in ("alert_severity", "alert_type", "alert_message", "alert_status"):
            if col in data:
                fields.append(f"{col} = %s")
                values.append(data[col])

        if data.get("alert_status") == "acknowledged" and "acknowledged_by_admin_id" in data:
            fields.append("acknowledged_by_admin_id = %s")
            fields.append("acknowledged_at = NOW()")
            values.append(data["acknowledged_by_admin_id"])
        if data.get("alert_status") == "resolved":
            fields.append("resolved_at = NOW()")

        if not fields:
            return jsonify({"error": "No fields to update"}), 400
        values.extend([server_id, data["alert_id"]])
        cursor.execute(
            f"UPDATE alerts SET {', '.join(fields)} WHERE server_id = %s AND alert_id = %s",
            values,
        )
        db.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Alert not found"}), 404
        return jsonify({"message": "Alert updated"}), 200
    finally:
        cursor.close()


@admin_routes.route("/servers/<int:server_id>/alerts", methods=["DELETE"])
def delete_server_alert(server_id):
    data = request.json
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            "DELETE FROM alerts WHERE alert_id = %s AND server_id = %s",
            (data["alert_id"], server_id),
        )
        db.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Alert not found"}), 404
        return jsonify({"message": "Alert deleted"}), 200
    finally:
        cursor.close()


# ---------- /alert/<id> ----------

@admin_routes.route("/alert/<int:alert_id>", methods=["GET"])
def get_alert(alert_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM alerts WHERE alert_id = %s", (alert_id,))
        alert = cursor.fetchone()
        if not alert:
            return jsonify({"error": "Alert not found"}), 404
        return jsonify(alert), 200
    finally:
        cursor.close()


@admin_routes.route("/alert/<int:alert_id>", methods=["PUT"])
def update_alert(alert_id):
    data = request.json
    db = get_db()
    cursor = db.cursor()
    try:
        fields, values = [], []
        for col in ("alert_severity", "alert_type", "alert_message", "alert_status"):
            if col in data:
                fields.append(f"{col} = %s")
                values.append(data[col])

        if data.get("alert_status") == "acknowledged" and "acknowledged_by_admin_id" in data:
            fields.append("acknowledged_by_admin_id = %s")
            fields.append("acknowledged_at = NOW()")
            values.append(data["acknowledged_by_admin_id"])
        if data.get("alert_status") == "resolved":
            fields.append("resolved_at = NOW()")

        if not fields:
            return jsonify({"error": "No fields to update"}), 400
        values.append(alert_id)
        cursor.execute(
            f"UPDATE alerts SET {', '.join(fields)} WHERE alert_id = %s", values
        )
        db.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Alert not found"}), 404
        return jsonify({"message": "Alert updated"}), 200
    finally:
        cursor.close()


@admin_routes.route("/alert/<int:alert_id>", methods=["DELETE"])
def delete_alert(alert_id):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM alerts WHERE alert_id = %s", (alert_id,))
        db.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Alert not found"}), 404
        return jsonify({"message": "Alert deleted"}), 200
    finally:
        cursor.close()
