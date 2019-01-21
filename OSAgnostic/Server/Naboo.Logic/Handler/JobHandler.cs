using System;
using System.Collections.Generic;
using System.Linq;

namespace Naboo.Logic.Handler
{
    public partial class JobHandler
    {
        public static List<Naboo.Entities.Job> JobByHostId(int HostId)
        {
            var dbContext = new Naboo.DataAccess.Model.OSAgnosticContext(ConnectionHandler.ConnectionString());
            var jobs = dbContext.Job.Where(c => c.HostId == HostId).OrderBy(f => f.Id).ToList().Convert();
            return jobs;
        }

        public static int JobActive(int HostId)
        {
            var dbContext = new Naboo.DataAccess.Model.OSAgnosticContext(ConnectionHandler.ConnectionString());
            var count = dbContext.Job.Count(c => c.HostId == HostId && c.State == true);
            return count;
        }

        public static int JobInaActive(int HostId)
        {
            var dbContext = new Naboo.DataAccess.Model.OSAgnosticContext(ConnectionHandler.ConnectionString());
            var count = dbContext.Job.Count(c => c.HostId == HostId && c.State == false);
            return count;
        }

        public static Entities.Job Add(Entities.Job item)
        {
            Entities.Job result = new Entities.Job();
            var dbContext = new Naboo.DataAccess.Model.OSAgnosticContext(ConnectionHandler.ConnectionString());
            Naboo.DataAccess.Model.Job jobDb = item.Convert();
            dbContext.Job.Add(jobDb);
            dbContext.SaveChanges();
            result = jobDb.Convert();
            return result;
        }

        public static dynamic Exist(string Code, int HostId)
        {
            bool result = false;
            int Id = 0;
            var dbContext = new Naboo.DataAccess.Model.OSAgnosticContext(ConnectionHandler.ConnectionString());
            var jobDb = dbContext.Job.Where(c => c.Code.ToLower().Equals(Code.ToLower()) && c.HostId == HostId).FirstOrDefault();
            if (jobDb != null)
            {
                result = true;
                Id = jobDb.Id;
            }
            return new { Exist = result, Id = Id };
        }
    }

    public static class JobExtencions
    {
        public static List<Naboo.Entities.Job> Convert(this List<Naboo.DataAccess.Model.Job> items)
        {
            List<Naboo.Entities.Job> result = new List<Entities.Job>();
            foreach (var item in items)
            {
                result.Add(item.Convert());
            }
            return result;
        }

        public static Naboo.Entities.Job Convert(this Naboo.DataAccess.Model.Job item)
        {
            Naboo.Entities.Job result = new Naboo.Entities.Job();
            result.Id = item.Id;
            result.Code = item.Code;
            result.Name = item.Name;
            result.Interval = (int)item.Interval;
            result.HostId = item.HostId;
            result.OSType = item.OSType;
            result.CreateDate = DateTime.Now;
            result.UpdateDate = DateTime.Now;
            result.State = true;
            return result;
        }

        public static Naboo.DataAccess.Model.Job Convert(this Naboo.Entities.Job item)
        {
            Naboo.DataAccess.Model.Job result = new Naboo.DataAccess.Model.Job();

            result.Code = item.Code;
            result.Name = item.Name;
            result.Interval = (int)item.Interval;
            result.HostId = item.HostId;
            result.OSType = item.OSType;
            result.CreateDate = DateTime.Now;
            result.UpdateDate = DateTime.Now;
            result.State = true;
            return result;
        }
    }
}