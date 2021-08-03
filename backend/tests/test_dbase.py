def test_db_init_commands(runner):
    result = runner.invoke(args=['delete'])
    assert "Done!" in result.output

    result = runner.invoke(args=['populate'])
    assert "Populating" in result.output
    pass 
