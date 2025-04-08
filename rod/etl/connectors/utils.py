def get_table_list_query(engine: str, db_name: str | None = None) -> str:
    engine = engine.lower()

    if engine == "postgresql":
        return """
            SELECT table_schema, table_name
            FROM information_schema.tables
            WHERE table_type = 'BASE TABLE';
        """

    if engine == "mysql":
        if not db_name:
            msg = "MySQL requires 'db_name' to query table list."
            raise ValueError(msg)
        return (
            """
            SELECT table_schema, table_name
            FROM information_schema.tables
            WHERE table_schema = %s AND table_type = 'BASE TABLE';
        """,
            (db_name,),
        )

    if engine == "sqlite":
        return """
            SELECT name as table_name
            FROM sqlite_master
            WHERE type = 'table';
        """

    if engine in {"mssql", "sqlserver"}:
        return """
            SELECT TABLE_SCHEMA, TABLE_NAME
            FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_TYPE = 'BASE TABLE';
        """

    msg = f"Unsupported engine: {engine}"
    raise ValueError(msg)
