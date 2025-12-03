from database.DB_connect import DBConnect
from model.rifugio import Rifugio

class DAO:
    """
        Implementare tutte le funzioni necessarie a interrogare il database.
        """
    @staticmethod
    def readRifugi():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Errore di connessione al database.")
            return None
        cursor = cnx.cursor(dictionary=True)
        query = """ SELECT * FROM rifugio"""
        try:
            cursor.execute(query)
            for row in cursor:
                rifugio = Rifugio(
                    id=row["id"],
                    nome=row["nome"],
                    localita=row["localita"],
                    altitudine=row["altitudine"],
                    capienza=row["capienza"],
                    aperto=row["aperto"]
                )
                result.append(rifugio)
        except Exception as e:
            print(f"Errore durante la query: {e}")
            result = None
        finally:
            cursor.close()
            cnx.close()

        return result

    @staticmethod
    def read_connessioni_per_anno(year):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Errore di connessione al database.")
            return None
        cursor = cnx.cursor(dictionary=True)
        query = """ SELECT id_rifugio1,id_rifugio2 FROM connessione WHERE anno<=%s"""
        try:
            cursor.execute(query,(year,))
            for row in cursor:
                result.append((row["id_rifugio1"],row["id_rifugio2"]))
        except Exception as e:
            print(f"Errore durante la query: {e}")
            result = None
        finally:
            cursor.close()
            cnx.close()

        return result



