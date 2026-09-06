def get_patient_data():
    print("Enter Patient Details")
    age = int(input("Age: "))
    severity = int(input("Severity (1-5): "))
    oxygen = input("Oxygen Level (normal/low): ")
    heartrate = input("Heart Rate (low/normal/high): ")
    consciousness = input("Consciousness (conscious/semi/unconscious): ")
    injury = input("Injury Type (none/minor/major): ")
    pain = int(input("Pain Level (0-10): "))

    return {
        "age": age,
        "severity": severity,
        "oxygen": oxygen,
        "heartrate": heartrate,
        "consciousness": consciousness,
        "injury": injury,
        "pain": pain
    }


patient_data = get_patient_data()

print("\nPatient Data Collected:")
print(patient_data)

