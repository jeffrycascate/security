# region Imporst
import MySQLdb
import MySQLdb.cursors
# endregion

#region Class
class CommandResult(object):
    def __init__(self):
        self.Rows = []
        self.RowCount = 0
        self.LastRowId = 0
        self.Successfully = False
        self.ExceptionOriginal  = ""

#endregion

# region Methods

def CreateInstance(Host, User, Password, Database):
    db = MySQLdb.connect(host=Host, user=User, passwd=Password, db=Database)
    return db

def ExecuteCommand(db , query, paramaters):
    result = CommandResult()
    try:
        with db as conexion:
            cursor = conexion.execute(query, paramaters)
            result.Rows = conexion.fetchall()
            result.RowCount = conexion.rowcount
            result.LastRowId = conexion.lastrowid
        result.Successfully = True
    except Exception as e:
        result.Exception = e    
    return result


# endregion


    # region Constructor
if __name__ == "__main__":

    # region Configuration
    MySQLHost = '186.177.106.36'
    MySQLUser = 'root'
    MySQLPassword = 'Jcv1821@t5'
    MySQLDatabase = 'osagnostic'
    # endregion

    db = CreateInstance(Host= MySQLHost, User= MySQLUser, Password= MySQLPassword, Database= MySQLDatabase)
    queryStatement = 'INSERT INTO host( Name, IPLocal, IPPublic, MacAddress, State) VALUES ( @@CCSERVER@@, @@192.168.0.14@@, @@186.177.106.36@@, @@AC-81-12-82-0E-E5@@, b@@1@@);'.replace('@@', chr(39))
    parameters = ()
    rows = ExecuteCommand(db, queryStatement, parameters)
    queryStatement = 'select count(*) from host'
    dfasdfa = ExecuteCommand(db, queryStatement, parameters)
    
# endregion
