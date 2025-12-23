from hello_world import Token

def test_token_render_always_returns_string():
    token = Token(1234)  # type: ignore[arg-type]
    assert token.render() == "1234"