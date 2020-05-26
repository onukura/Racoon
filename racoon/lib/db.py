# -*- coding: utf-8 -*-
import pandas as pd
from sqlalchemy.dialects import postgresql


def df2dict(df, key="tag", value="value"):
    config = {}
    for i, row in df.iterrows():
        config[row[key]] = row[value]
    return config


def get_df_from_db(db, table):
    query = create_query_for_get_table(db, table)
    df = pd.read_sql(query, db.engine)
    return df


def create_query_for_get_table(db, table):
    query_obj = db.session.query(table)
    query = query_obj.statement.compile(
        dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}
    )
    return query


def create_general_query(query_obj):
    return query_obj.statement.compile(
        dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}
    )
