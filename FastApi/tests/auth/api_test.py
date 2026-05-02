import pytest

@pytest.mark.parametrize("email, password", [
    ("emailemail@gmail.com", "qwerty1234"),
    ("kotopes@gmail.com", "kotopes1234"),
    ("spongebob@gmail.com", "square123")
                         ])
async def test_auth_requests(email, password, ac):
    #register
    request = await ac.post("/auth/register", json={"email": email, "password": password})
    assert request.status_code == 200

    #login
    login = await ac.post("/auth/login", json={"email": email, "password": password})
    assert login.status_code == 200
    res = login.cookies["access_token"]
    assert res is not None
    assert "access_token" in login.json()

    #check auth
    only_auth = await ac.get("/auth/only_auth")
    assert only_auth.status_code == 200
    assert ac.cookies["access_token"] is not None

    #logout
    logout = await ac.post("/auth/logout")
    assert logout.status_code == 200
    res = ac.cookies
    assert "access_token" not in res

