import sys
import pymysql


class RDSWorks():
    """
    To handle all the RDS related works
    """

    def __init__(self, **kwargs) -> None:
        self.conn_params = kwargs

    def connect_to_db(self,) -> None:
        """
        Return a connection object
        """
        try:
            print("Connecting to db...")
            self.connection = pymysql.connect(**self.conn_params)
            print("Connection successful..")
            self.cursor = self.connection.cursor()
        except Exception as e:
            print(e)
            sys.exit(1)

    def get_muid_from_table(self, table: str, value: tuple, get: str, ) -> None:
        """
        Pass in an identity attribute value (email or phone,)
        return True if muid exists against value else return False
        """
        muid_exists_query = """SELECT {} FROM {} WHERE {}='{}'""".format(
            get, str(table), str(value[0]), str(value[1]))
        print(muid_exists_query)
        try:
            self.cursor.execute(muid_exists_query)
            muid = self.cursor.fetchone()
            print(muid)
            return muid[0]
        except Exception as e:
            print(e)
            print("MUID doesn't exist for given value: {}".format(str(value)))
            return None

    def check_if_exists(self, muid: str, attr_type: str, value: str, cuid: int,) -> bool:
        """
        Useful while inserting to identity_attributes table
        Check to see if the combination of muid, attr_type, value, cuid is already present
        """
        raise NotImplementedError

    def select_sql(self, table: str, ) -> list:
        """
        Emulating a SELECT query in SQL
        """
        raise NotImplementedError

    def insert_sql(self, table: str, attrs: list, values: list) -> None:
        """
        Emulating a INSERT query in SQL
        """
        attrs_string = ','.join(attrs)
        values_string = ','.join("'{}'".format(str(val)) for val in values)

        insert_query = """INSERT INTO {table}({attrs}) VALUES({values})""".format(
            table=table, attrs=attrs_string, values=values_string)
        print(insert_query)
        try:
            self.cursor.execute(insert_query)
            self.connection.commit()
        except Exception as e:
            print(e)

    def close_connection(self,) -> None:
        try:
            self.connection.close()
            print("Closed db connection..")
        except Exception as e:
            print(e)
