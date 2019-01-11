using System;
using System.Linq;
using Naboo.DataAccess.Model;

namespace Dummy
{
    class Program
    {
        static void Main(string[] args)
        {
            var dbContext = new OSAgnosticContext();
            var hosts = dbContext.Host.ToList();
            foreach(var c in hosts) {
                Console.WriteLine($"Id:{c.Id} del hosts es {c.Name}");
            }

           
        }
    }
}
