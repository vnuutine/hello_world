from hello_world import (
    Config,
    GreetingAssembler,
    TokenFactory,
    MessageFactory,
    Logger,
)

def test_assembler_builds_expected_greeting():
    cfg = Config(
        greeting_primary="Hello",
        greeting_secondary="world",
        separator=",",
        space=" ",
        punctuation="!",
        output_enabled=True,
    )

    logger = Logger("test")
    assembler = GreetingAssembler(
        cfg=cfg,
        token_factory=TokenFactory(logger),
        message_factory=MessageFactory(logger),
        logger=logger,
    )

    message = assembler.assemble()
    assert message.compile() == "Hello, world!"
    assert len(message.tokens) == 5