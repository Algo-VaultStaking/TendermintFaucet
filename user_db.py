import datetime
from math import floor
import requests
from logger import log, raw_audit_log
import secrets

import mariadb


# Connect to MariaDB Platform
def connection():
    try:
        conn = mariadb.connect(
            user=secrets.MARIADB_USER,
            password=secrets.MARIADB_PASSWORD,
            host=secrets.MARIADB_HOST,
            port=3306,
            database="comdex_faucet"
        )

        return conn


    except mariadb.Error as e:
        raw_audit_log(f"Error connecting to MariaDB Platform: {e}")
        exit()


def initial_setup():
    try:
        conn = connection()
        cur = conn.cursor()
        # cur.execute("DROP TABLE Transactions;")

        cur.execute("CREATE TABLE Transactions(UserID VARCHAR(20), "
                    "LastSeen VARCHAR(30), "
                    "Network VARCHAR(30));")

        cur.close()
        conn.close()
    except mariadb.Error as e:
        raw_audit_log(f"Error: {e}")


def get_user_last_transaction_time(user_id: str, network: str):
    conn = connection()
    cur = conn.cursor()
    cur.execute(f"SELECT LastSeen FROM Transactions WHERE UserID='{user_id}' AND Network='{network}';")
    for d in cur:
        cur.close()
        conn.close()
        return d[0]


def add_transaction(user_id: str, timestamp: str, network: str):
    conn = connection()
    cur = conn.cursor()
    cur.execute("SELECT UserID, Network FROM Transactions")
    found = False
    for id, ntwk in cur:
        if user_id == id and ntwk == network:
            found = True

    try:
        if found:
            command = "UPDATE Transactions " \
                      "SET LastSeen = '" + timestamp + "' " \
                      "WHERE UserID = '" + user_id + "' AND Network = '" + network + "';"
            cur.execute(command)
            conn.commit()
        else:
            cur.execute("INSERT INTO Transactions VALUES (?, ?, ?)",
                        (user_id, timestamp, network))

        conn.commit()
        cur.close()
        conn.close()
        return True
    except mariadb.Error as e:
        raw_audit_log(f"Error: {e}")
        conn.close()
        return False
