using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace Naboo.Services.Handler
{
    public static class ConnectionHandler
    {
        public static string ConnectionString()
        {
            string result = "";
            result = "server=186.177.106.36;database=osagnostic;user=root;pwd=Jcv1821@t5";
            return result;
        }
    }
}
