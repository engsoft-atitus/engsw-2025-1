import oracledb
from decouple import config
import ssl

def test_connection():
    try:
        dsn = f"""
        (DESCRIPTION=
            (ADDRESS=
                (PROTOCOL=TCPS)
                (HOST={config("DB_HOST")})
                (PORT={config("DB_PORT")})
            )
            (CONNECT_DATA=
                (SERVICE_NAME={config("DB_NAME")})
            )
        )
        """
        
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        conn = oracledb.connect(
            user=config("DB_USER"),
            password=config("DB_PASSWORD"),
            dsn=dsn,
            ssl_context=ssl_context
        )

        with conn.cursor() as cursor:
            cursor.execute("SELECT '✅ Conexão TCPS OK!' FROM dual")
            print(cursor.fetchone()[0])
        
        conn.close()
    except Exception as e:
        print(f"❌ Falha na conexão: {type(e).__name__}: {e}")

if __name__ == "__main__":
    test_connection()