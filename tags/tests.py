import ujson

# from tags.views import *


def test_create_tag(app):
    url = '/tags'
    client = app.test_client()

    # Send create request without data
    resp = client.post(url, json={})
    assert resp.status_code == 400

    # Send exist data
    resp = client.post(url, json={'name': 'Toyota'})
    assert resp.status_code == 400

    resp = client.post(url, json={'name': 'Simple tag'})

    assert resp.status_code == 201


def test_find_tags(app):
    url = '/tags_find'
    client = app.test_client()

    # Send request without data
    resp = client.post(url, json={})
    assert resp.status_code == 400
    resp = client.post(url, json={'text': 'Toyota'})
    assert resp.status_code == 200

    # test with add two additional words
    resp = client.post(url, json={'text': 'Air test test Conditioning'})
    data = ujson.loads(resp.data)
    assert resp.status_code == 200
    assert data == [{'name': 'Air Conditioning'}]

    # full text test
    test_text = """
New Toyota Corolla LE 2007, Air Conditioning, Leather seaters, Auxillary Gear/4 Wheel Drive,SRS-Airbags, Alloy Wheels,
Abs System, AM/FM Radio, Anti-Lock Brakes, Armrests, CD & DVD Player,Reverse Camera And Navigation system,Good-Engine,
First-Body, Good-Interior,Cup Holders, Electric Mirrors, Electric Windows, Fog Lights, Front Fog Lamps, Power Steering,
Roof Rack, Spoiler,Tinted Windows, Wheel Locks, Jack, Wheel Spanners, Spare Tire, LIMITED Edition.
Also Available in Different Colours.
Beware Of Fraudsters, therefore do not send money or picture to any dealer or individual you have not gone to inspect
the car first,Please See What You Want To Buy Before Any Payment .
    """

    resp = client.post(url, json={'text': test_text})
    data = ujson.loads(resp.data)

    assert resp.status_code == 200
    assert len(data) == 5

    expected_data = [
        {'name': 'Toyota'},
        {'name': 'Toyota Corolla 2007'},
        {'name': 'Toyota Corolla LE'},
        {'name': '4 Wheel Drive'},
        {'name': 'Air Conditioning'}
    ]
    assert data == expected_data
