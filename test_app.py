
from app import app, submissions


def test_home_page_loads():
    with app.test_client() as client:
        response = client.get("/")

        assert response.status_code == 200


def test_valid_submission_is_saved_and_displayed():
    submissions.clear()

    with app.test_client() as client:
        response = client.post(
            "/submit",
            data={
                "name": "Test Student",
                "registration": "BSE-062",
                "title": "Midterm Submission",
                "url": "https://github.com/example/project",
            },
            follow_redirects=True,
        )

        assert response.status_code == 200
        assert len(submissions) == 1

    submissions.clear()


def test_missing_registration_number_is_rejected():
    with app.test_client() as client:
        response = client.post(
            "/submit",
            data={
                "name": "Test Student",
                "registration": "",
                "title": "Midterm Submission",
                "url": "https://github.com/example/project",
            },
        )

        assert response.status_code == 400


def test_invalid_submission_url_is_rejected():
    with app.test_client() as client:
        response = client.post(
            "/submit",
            data={
                "name": "Test Student",
                "registration": "BSE-062",
                "title": "Midterm Submission",
                "url": "not-a-valid-url",
            },
        )

        assert response.status_code == 400
