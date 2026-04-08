import socket
import pickle

def send_request(req):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("localhost", 9999))

    client.send(pickle.dumps(req))
    response = pickle.loads(client.recv(4096))

    client.close()
    return response


while True:
    print("\n" + "="*50)
    print("🏥 HOSPITAL MANAGEMENT SYSTEM")
    print("="*50)
    print("1. Add Patient")
    print("2. Get Patient by ID")
    print("3. Show All Patients")
    print("4. Update Patient")
    print("5. Delete Patient")
    print("6. Total Patients Count")
    print("7. Search Patient by Name")
    print("8. Show Patients by Disease")
    print("9. Book Appointment")
    print("10. View Appointments")
    print("11. Send Emergency Alert")
    print("12. Clear All Records")
    print("13. Backup Data")
    print("14. Exit")
    print("="*50)

    try:
        choice = int(input("👉 Enter choice: "))
    except:
        print("❌ Invalid input")
        continue

    # ADD
    if choice == 1:
        pid = int(input("Enter ID: "))
        name = input("Enter Name: ")
        age = int(input("Enter Age: "))
        disease = input("Enter Disease: ")

        req = {
            "action": "add",
            "id": pid,
            "name": name,
            "age": age,
            "disease": disease
        }
        print(send_request(req))

    # GET
    elif choice == 2:
        pid = int(input("Enter ID: "))
        res = send_request({"action": "get", "id": pid})

        if isinstance(res, dict):
            print(f"ID: {res['id']} | Name: {res['name']} | Age: {res['age']} | Disease: {res['disease']}")
        else:
            print(res)

    # SHOW ALL
    elif choice == 3:
        data = send_request({"action": "all"})

        if data:
            for p in data.values():
                print(f"ID: {p['id']} | Name: {p['name']} | Age: {p['age']} | Disease: {p['disease']}")
        else:
            print("❌ No patients found")

    # UPDATE
    elif choice == 4:
        pid = int(input("Enter ID: "))
        name = input("Enter New Name: ")
        age = int(input("Enter New Age: "))
        disease = input("Enter New Disease: ")

        req = {
            "action": "update",
            "id": pid,
            "name": name,
            "age": age,
            "disease": disease
        }
        print(send_request(req))

    # DELETE
    elif choice == 5:
        pid = int(input("Enter ID: "))
        print(send_request({"action": "delete", "id": pid}))

    # COUNT
    elif choice == 6:
        print("Total Patients:", send_request({"action": "count"}))

    # SEARCH NAME
    elif choice == 7:
        name = input("Enter name: ")
        res = send_request({"action": "search_name", "name": name})

        if isinstance(res, list):
            for p in res:
                print(f"ID: {p['id']} | Name: {p['name']} | Age: {p['age']} | Disease: {p['disease']}")
        else:
            print(res)



    # DISEASE FILTER
    elif choice == 8:
        disease = input("Enter disease: ")
        res = send_request({"action": "disease_filter", "disease": disease})

        if isinstance(res, list):
            for p in res:
                print(f"ID: {p['id']} | Name: {p['name']} | Age: {p['age']} | Disease: {p['disease']}")
        else:
            print(res)

    # BOOK APPOINTMENT
    elif choice == 9:
        pid = int(input("Enter Patient ID: "))
        name = input("Enter Name: ")
        date = input("Enter Date: ")
        doctor = input("Enter Doctor: ")

        req = {
            "action": "book_appointment",
            "id": pid,
            "name": name,
            "date": date,
            "doctor": doctor
        }
        print(send_request(req))

    # VIEW APPOINTMENTS
    elif choice == 10:
        res = send_request({"action": "view_appointments"})

        if isinstance(res, list):
            for a in res:
                print(f"ID: {a['id']} | Name: {a['name']} | Date: {a['date']} | Doctor: {a['doctor']}")
        else:
            print(res)

    # EMERGENCY
    elif choice == 11:
        pid = int(input("Enter Patient ID: "))
        print(send_request({"action": "emergency", "id": pid}))

    # CLEAR
    elif choice == 12:
        print(send_request({"action": "clear"}))

    # BACKUP
    elif choice == 13:
        data = send_request({"action": "backup"})
        print("Backup Data:", data)

    # EXIT
    elif choice == 14:
        print("👋 Exiting...")
        break

    else:
        print("❌ Invalid choice")