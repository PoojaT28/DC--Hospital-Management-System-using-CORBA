import socket
import pickle

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 9999))
server.listen(5)

patients = {}
appointments = []

print("✅ Hospital Server Started...")

while True:
    client, addr = server.accept()
    print("Connected with", addr)

    data = client.recv(4096)
    request = pickle.loads(data)

    action = request.get("action")

    # ---------------- PATIENT FEATURES ----------------

    if action == "add":
        patients[request["id"]] = request
        response = "✅ Patient Added Successfully"

    elif action == "get":
        response = patients.get(request["id"], "❌ Patient Not Found")

    elif action == "all":
        response = patients

    elif action == "delete":
        if request["id"] in patients:
            del patients[request["id"]]
            response = "🗑️ Patient Deleted Successfully"
        else:
            response = "❌ Patient Not Found"

    elif action == "update":
        if request["id"] in patients:
            patients[request["id"]].update(request)
            response = "✏️ Patient Updated Successfully"
        else:
            response = "❌ Patient Not Found"

    elif action == "count":
        response = len(patients)

    elif action == "search_name":
        name = request["name"].lower()
        result = [p for p in patients.values() if name in p["name"].lower()]
        response = result if result else "❌ No matching patient found"


    elif action == "disease_filter":
        disease = request["disease"].lower()
        result = [p for p in patients.values() if disease in p["disease"].lower()]
        response = result if result else "❌ No patients found"

    elif action == "clear":
        patients.clear()
        response = "🧹 All records cleared"

    elif action == "backup":
        response = patients.copy()

    # ---------------- NEW FEATURES ----------------

    elif action == "book_appointment":
        appointment = {
            "id": request["id"],
            "name": request["name"],
            "date": request["date"],
            "doctor": request["doctor"]
        }
        appointments.append(appointment)
        response = "📅 Appointment Booked Successfully"

    elif action == "view_appointments":
        response = appointments if appointments else "❌ No appointments found"

    elif action == "emergency":
        response = f"🚨 EMERGENCY ALERT for Patient ID {request['id']}"

    else:
        response = "❌ Invalid Request"

    client.send(pickle.dumps(response))
    client.close()