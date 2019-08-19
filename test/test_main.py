from starlette.testclient import TestClient

from .main import app

client = TestClient(app)

null = None

def test_main():
    response = client.get("/")
    assert response.status_code == 200

def test_post_location():
    # change response after each test as it adds to database and check 'id' before test in database
    # id parameter skipped from 8000 to 110046
    response = client.post(
        "/post_location/",
        json={"pincode": "xx/44444",
          "place_name": "roger",
          "admin_name": "waters",
          "latitude": 77.88,
          "longitude": 99.11,
          "accuracy": null}
    )
    assert response.status_code == 200
    assert response.json() == {
          "pincode": "xx/44444",
          "place_name": "roger",
          "admin_name": "waters",
          "latitude": 77.88,
          "longitude": 99.11,
          "accuracy": null,
          "id": 11047
    }
    
def test_post_location2():
    # pincode of Faridabad, Uttar Pradesh
    response = client.post(
        "/post_location/",
        json={"pincode": "IN/121001",
          "place_name": "roger",
          "admin_name": "waters",
          "latitude": 11.22,
          "longitude": 44.55,
          "accuracy": null}
    )
    assert response.status_code == 418
    assert response.json() == {
      "detail": "Location already registered by pincode"
    }

def test_post_location3():
    # parameters of Gurur, Chattisgarh
    response = client.post(
        "/post_location/",
        json={"pincode": "xx/44444",
          "place_name": "roger",
          "admin_name": "waters",
          "latitude": 20.6833,
          "longitude": 81.4,
          "accuracy": null}
    )
    assert response.status_code == 418
    assert response.json() == {
      "detail": "Location already registered by latitude and longitude"
    }

def test_post_location4():
    # parameters close to Inderlok, New Delhi
    response = client.post(
        "/post_location/",
        json={"pincode": "xx/44444",
          "place_name": "roger",
          "admin_name": "waters",
          "latitude":  28.75559,
          "longitude": 77.16669,
          "accuracy": null}
    )
    assert response.status_code == 418
    assert response.json() == {
      "detail": "Location already registered by latitude and longitude"
    }


def test_get_location():
    response = client.get("/get_location/?lat=28.7165&lon=77.1629")
    assert response.status_code == 200
    assert response.json() == [
  {
    "pincode": "IN/110088",
    "place_name": "Shalimar Bagh",
    "admin_name": "New Delhi",
    "latitude": 28.7165,
    "longitude": 77.1629,
    "accuracy": 6,
    "id": 75
  }
]
    
def test_get_location2():
    # imaginary parameters
    response = client.get("/get_location/?lat=12.34&lon=56.78")
    assert response.status_code == 420
    assert response.json() == {
      "detail": "Location not found"
    }


def test_get_using_postgres():
    response = client.get("get_using_postgres/?lat=31.4329&lon=75.6507&lim=4")
    assert response.status_code == 200
    assert response.json() == [
  {
    "pincode": "IN/144301",
    "place_name": "Alawalpur",
    "admin_name": "Punjab",
    "latitude": 31.4328,
    "longitude": 75.6508,
    "accuracy": 4,
    "id": 744
  },
  {
    "pincode": "IN/144303",
    "place_name": "Kala Bakra",
    "admin_name": "Punjab",
    "latitude": 31.4328,
    "longitude": 75.6508,
    "accuracy": null,
    "id": 745
  },
  {
    "pincode": "IN/144304",
    "place_name": "Lakhinder",
    "admin_name": "Punjab",
    "latitude": 31.4328,
    "longitude": 75.6508,
    "accuracy": null,
    "id": 746
  },
  {
    "pincode": "IN/144305",
    "place_name": "Khudda",
    "admin_name": "Punjab",
    "latitude": 31.4328,
    "longitude": 75.6508,
    "accuracy": null,
    "id": 747
  }
]
        
def test_get_using_postgres2():
    # imaginary parameters
    response = client.get("get_using_postgres/?lat=33.4329&lon=78.6507&lim=4")
    assert response.status_code == 201
    

def test_get_using_self():
    response = client.get("get_using_self/?lat=31.4329&lon=75.6507&lim=1")
    assert response.status_code == 200
    assert response.json() == [
  {
    "pincode": "IN/144305",
    "place_name": "Khudda",
    "admin_name": "Punjab",
    "latitude": 31.4328,
    "longitude": 75.6508,
    "accuracy": null,
    "id": 747
  },
  {
    "pincode": "IN/144304",
    "place_name": "Lakhinder",
    "admin_name": "Punjab",
    "latitude": 31.4328,
    "longitude": 75.6508,
    "accuracy": null,
    "id": 746
  },
  {
    "pincode": "IN/144303",
    "place_name": "Kala Bakra",
    "admin_name": "Punjab",
    "latitude": 31.4328,
    "longitude": 75.6508,
    "accuracy": null,
    "id": 745
  },
  {
    "pincode": "IN/144301",
    "place_name": "Alawalpur",
    "admin_name": "Punjab",
    "latitude": 31.4328,
    "longitude": 75.6508,
    "accuracy": 4,
    "id": 744
  }
]
        
def test_get_using_self2():
    # imaginary parameters
    response = client.get("get_using_self/?lat=33.4329&lon=78.6507&lim=10")
    assert response.status_code == 202


def test_detect():
    response = client.get("/detect/?lat=76.9969&lon=28.5198")
    assert response.status_code == 200
    assert response.json() == [
      [
        "Gurgaon"
      ]
    ]
      
def test_detect2():
    # imaginary parameters
    response = client.get("/detect/?lat=11.22&lon=33.44")
    assert response.status_code == 404
    assert response.json() == {
      "detail": "Location not found"
    }


