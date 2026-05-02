async def test_facilities_get(ac):
    response = await ac.get("/facilities")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

async def test_facilities_post(ac):
    facility_title = "Wi-Fi"
    post = await ac.post("/facilities", json={"title": facility_title})
    assert post.status_code == 200
    res = post.json()
    assert isinstance(res, dict)
    assert res["facility"]["title"] == "Wi-Fi"
    assert "facility" in post.json()


