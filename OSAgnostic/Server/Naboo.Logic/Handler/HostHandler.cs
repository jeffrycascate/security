using Naboo.Entities;
using System;
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

        public static dynamic Exist(string Name)
        {
            bool result = false;
            int Id = 0;
            var dbContext = new Naboo.DataAccess.Model.OSAgnosticContext(ConnectionHandler.ConnectionString());
            var hostDb = dbContext.Host.Where(c => c.Name.ToLower().Equals(Name.ToLower())).FirstOrDefault();
            if (hostDb != null)
            {
                result = true;
                Id = hostDb.Id;
            }
            return new { Exist = result, Id = Id };
        }

        public static Host Add(Host item)
        {
            Host result = new Host();
            var dbContext = new Naboo.DataAccess.Model.OSAgnosticContext(ConnectionHandler.ConnectionString());
            Naboo.DataAccess.Model.Host hostDb = item.Convert();
            dbContext.Host.Add(hostDb);
            dbContext.SaveChanges();
            result = hostDb.Convert();
            return result;
        }
        public static object StateChange(int id, bool state)
        {
            bool result = false;
            var dbContext = new Naboo.DataAccess.Model.OSAgnosticContext(ConnectionHandler.ConnectionString());
           
            try
            {
                var hostDb = dbContext.Host.Where(c => c.Id == id).FirstOrDefault();
                if(hostDb != null)
                {
                    hostDb.State = state;
                    dbContext.SaveChanges();
                    result = true;
                }
            }
            catch (Exception ex)
            {
 
            }
            return result;
        }

        public static object StateChangeServer()
        {
            bool result = false;
            var dbContext = new Naboo.DataAccess.Model.OSAgnosticContext(ConnectionHandler.ConnectionString());

            try
            {
                var hostsDb = (from itemDb in  dbContext.Host select itemDb).ToList();
                if (hostsDb != null)
                {
                    foreach (var item in hostsDb)
                    {
                        if(item.UpdateDate < DateTime.Now.AddSeconds(-30) && item.State == true)
                        {
                            item.State = false;
                        }
                    }
                    dbContext.SaveChanges();
                    result = true;
                }
            }
            catch (Exception ex)
            {

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

        public static Naboo.DataAccess.Model.Host Convert(this Naboo.Entities.Host item)
        {
            Naboo.DataAccess.Model.Host result = new Naboo.DataAccess.Model.Host();
            result.IPLocal = item.IPLocal;
            result.IPPublic = item.IPPublic;
            result.MacAddress = item.MacAddress;
            result.Name = item.Name;
            result.OSArchitecture = item.OS.Architecture;
            result.OSName = item.OS.Name;
            result.OSRelease = item.OS.Release;
            result.OSSystem = item.OS.System;
            result.State = item.State;
            result.UpdateDate = DateTime.Now;
            result.CreateDate = DateTime.Now;
            return result;
        }
    }
}