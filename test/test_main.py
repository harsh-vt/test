from starlette.testclient import TestClient

from .main import app

client = TestClient(app)

null = None

def test_main():
    response = client.get("/")
    assert response.status_code == 200

def test_post_location():
    #change response after each test as it adds to database and check id before test in database
    response = client.post(
        "/post_location/",
        json={"pincode": "xx/44444",
          "place_name": "roger",
          "admin_name1": "waters",
          "latitude": 77.88,
          "longitude": 99.11,
          "accuracy": null}
    )
    assert response.status_code == 200
    assert response.json() == {
          "pincode": "xx/44444",
          "place_name": "roger",
          "admin_name1": "waters",
          "latitude": 77.88,
          "longitude": 99.11,
          "accuracy": null,
          "id": 6
    }
    
def test_post_location2():
    response = client.post(
        "/post_location/",
        json={"pincode": "xx/88888",
          "place_name": "roger",
          "admin_name1": "waters",
          "latitude": 77.88,
          "longitude": 99.11,
          "accuracy": null}
    )
    assert response.status_code == 418
    assert response.json() == {
      "detail": "Location already registered by pincode"
    }

def test_post_location3():
    response = client.post(
        "/post_location/",
        json={"pincode": "xx/44444",
          "place_name": "roger",
          "admin_name1": "waters",
          "latitude": 44.55,
          "longitude": 66.77,
          "accuracy": null}
    )
    assert response.status_code == 418
    assert response.json() == {
      "detail": "Location already registered by latitude and longitude"
    }

def test_post_location4():
    response = client.post(
        "/post_location/",
        json={"pincode": "xx/44444",
          "place_name": "roger",
          "admin_name1": "waters",
          "latitude": 44.549998,
          "longitude": 66.769998,
          "accuracy": null}
    )
    assert response.status_code == 418
    assert response.json() == {
      "detail": "Location already registered by latitude and longitude"
    }


def test_get_location():
    response = client.get("/get_location/?lat=88.99&lon=11.22")
    assert response.status_code == 200
    assert response.json() == [
        {
        "pincode": "xx/66666",
        "place_name": "jim",
        "admin_name1": "morrison",
        "latitude": 88.99,
        "longitude": 11.22,
        "accuracy": 4,
        "id": 4
        }
    ]
    
def test_get_location2():
    response = client.get("/get_location/?lat=12.34&lon=56.78")
    assert response.status_code == 420
    assert response.json() == {
      "detail": "Location not found"
    }


def test_get_using_postgres():
    response = client.get("get_using_postgres/?lat=11.2198&lon=33.4398&lim=100")
    assert response.status_code == 200
    assert response.json() == [
      {
        "pincode": "xx/99999",
        "place_name": "foo",
        "admin_name1": "fighter",
        "latitude": 11.22,
        "longitude": 33.44,
        "accuracy": null,
        "id": 1
      },
      {
        "pincode": "xx/88888",
        "place_name": "pink",
        "admin_name1": "floyd",
        "latitude": 11.21998,
        "longitude": 33.4998,
        "accuracy": null,
        "id": 2
      }
    ]
        
def test_get_using_postgres2():
    response = client.get("get_using_postgres/?lat=11.2198&lon=33.4398&lim=5")
    assert response.status_code == 200
    assert response.json() == [
      {
        "pincode": "xx/99999",
        "place_name": "foo",
        "admin_name1": "fighter",
        "latitude": 11.22,
        "longitude": 33.44,
        "accuracy": null,
        "id": 1
      }
    ]

def test_get_using_self():
    response = client.get("get_using_self/?lat=11.2198&lon=33.4398&lim=100")
    assert response.status_code == 200
    assert response.json() == [
      {
        "pincode": "xx/99999",
        "place_name": "foo",
        "admin_name1": "fighter",
        "latitude": 11.22,
        "longitude": 33.44,
        "accuracy": null,
        "id": 1
      },
      {
        "pincode": "xx/88888",
        "place_name": "pink",
        "admin_name1": "floyd",
        "latitude": 11.21998,
        "longitude": 33.4998,
        "accuracy": null,
        "id": 2
      }
    ]
        
def test_get_using_self2():
    response = client.get("get_using_self/?lat=11.2198&lon=33.4398&lim=5")
    assert response.status_code == 200
    assert response.json() == [
      {
        "pincode": "xx/99999",
        "place_name": "foo",
        "admin_name1": "fighter",
        "latitude": 11.22,
        "longitude": 33.44,
        "accuracy": null,
        "id": 1
      }
    ]


def test_detect():
    response = client.get("/detect/?lat=76.9969&lon=28.5198")
    assert response.status_code == 200
    assert response.json() == [
      [
        "Gurgaon"
      ]
    ]
      
def test_detect2():
    response = client.get("/detect/?lat=11.22&lon=33.44")
    assert response.status_code == 404
    assert response.json() == {
      "detail": "Location not found"
    }


