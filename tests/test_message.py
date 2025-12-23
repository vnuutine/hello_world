from hello_world import Token, Message

def test_message_compile_preserves_order():
    msg = Message(tokens=[Token("Hello"), Token(", "), Token("world"), Token("!")])
    assert msg.compile() == "Hello, world!"