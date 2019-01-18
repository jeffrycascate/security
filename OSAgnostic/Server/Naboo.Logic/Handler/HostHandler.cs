using System.Collections.Generic;
using System.Linq;

namespace Naboo.Logic.Handler
{
    public partial class HostHandler
    {
        public static List<Naboo.Entities.Host> All()
        {
            List<Naboo.Entities.Host> result = new List<Entities.Host>();
            var dbContext = new Naboo.DataAccess.Model.OSAgnosticContext(ConnectionHandler.ConnectionString());
            var hostDb = dbContext.Host.OrderByDescending(c => c.State).ToList();
            result = hostDb.Convert();
            foreach (var item in result)
            {
                item.JobActive = Handler.JobHandler.JobActive(item.Id);
                item.JobInaActive = Handler.JobHandler.JobInaActive(item.Id);
            }
            return result;
        }
    }

    public static class HostExtencions
    {
        public static List<Naboo.Entities.Host> Convert(this List<Naboo.DataAccess.Model.Host> items)
        {
            List<Naboo.Entities.Host> result = new List<Entities.Host>();
            foreach (var item in items)
            {
                result.Add(item.Convert());
            }
            return result;
        }

        public static Naboo.Entities.Host Convert(this Naboo.DataAccess.Model.Host item)
        {
            Naboo.Entities.Host result = new Entities.Host();
            result.Id = item.Id;
            result.IPLocal = item.IPLocal;
            result.IPPublic = item.IPPublic;
            result.MacAddress = item.MacAddress;
            result.Name = item.Name;
            result.OSArchitecture = item.OSArchitecture;
            result.OSName = item.OSName;
            result.OSRelease = item.OSRelease;
            result.OSSystem = item.OSSystem;
            result.State = item.State;
            result.UpdateDate = result.UpdateDate;
            return result;
        }
    }
}