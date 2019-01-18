using Naboo.DataAccess.Model;
using System;
using System.Collections.Generic;
using System.Linq;

namespace Naboo.Logic.Handler
{
    public partial class JobHandler
    {
        public static List<Job> JobByHostId(int HostId)
        {
            var dbContext = new Naboo.DataAccess.Model.OSAgnosticContext(ConnectionHandler.ConnectionString());
            var jobs = dbContext.Job.Where(c => c.HostId == HostId).OrderBy(f => f.Id).ToList();
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
    }
}
