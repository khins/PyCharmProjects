import _sqlite3 as lite


def create_database(database_path: str):
    conn = lite.connect(database_path)
    with conn:
        cur = conn.cursor()
        cur.execute("drop table if exists table_words")
        ddl = "create table table_words (word text not null constraint table_words_pk primary key, usage_count int " \
              "default 1 not null); "
        cur.execute(ddl)
        ddl = "create unique index table_words_word_uindex on table_words (word);"
        cur.execute(ddl)
    conn.close()


def save_words_to_database(database_path: str, words_list: list):
    conn = lite.connect(database_path)
    with conn:
        cur = conn.cursor()
        for word in words_list:
            sql = "select count(word) from table_words where word = '" + word + "'"
            cur.execute(sql)
            count = cur.fetchone()[0]
            if count > 0:
                sql = "update table_words set usage_count = usage_count + 1 where word = '" + word + "'"
            else:
                sql = "insert into table_words(word) values ('" + word + "')"
            cur.execute(sql)

        print("Database save complete")
