
async def test_get_hotels(ac):
    response = await ac.get("/hotel",
                          params={
                              "date_from": "2025-04-11",
                               "date_to": "2025-04-16",})
    print(f"{response.json()}")
    assert response.status_code == 200
