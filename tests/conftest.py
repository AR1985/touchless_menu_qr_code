from application import generate_random_url


class TestHelperFunctions:
    def test_generate_random_url_length_between_3_and_93_characters(self):
        url = generate_random_url()
        assert len(url) in range(3,94)
