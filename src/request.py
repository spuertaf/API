import requests

def make_request(request_url):
    schedule = {
        "schedule": [["P1", "Lunes", "Martes", "13:00", "15:00", "14:00", "16:00"],
                    ["Economia", "Lunes", "Miercoles", "12:00", "14:30", "9:00", "12:00"],
                    ["Lineal", "Martes", "Miercoles", "9:00", "11:30", "15:00", "16:30"]]
    }

    response = requests.post(request_url,json=schedule)
    print(response.text)
    
    
if __name__ == "__main__":
    make_request(
        request_url="http://127.0.0.1:5000/getcombinations"
    )