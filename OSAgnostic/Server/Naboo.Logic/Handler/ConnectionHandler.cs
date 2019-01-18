using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace Naboo.Logic.Handler
{
    public static class ConnectionHandler
    {
        public static string ConnectionString()
        {
            string result = "";
            result = "server=192.168.0.14;database=osagnostic;user=root;pwd=Jcv1821@t5";
            return result;
        }
    }
}
