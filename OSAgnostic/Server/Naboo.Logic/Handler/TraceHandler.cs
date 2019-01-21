using Naboo.DataAccess.Model;
using System;
using System.Collections.Generic;
using System.Linq;

namespace Naboo.Logic.Handler
{
    public partial class TraceHandler
    {
        public static List<Trace> TraceByJobId(int JobId)
        {
            var dbContext = new Naboo.DataAccess.Model.OSAgnosticContext(Handler.ConnectionHandler.ConnectionString());
            var trace = dbContext.Trace.Where(c => c.JobId == JobId).OrderByDescending(f => f.Id).ToList();
            return trace;
        }

        public static Entities.Trace Add(Entities.Trace item)
        {
            Entities.Trace result = new Entities.Trace();
            var dbContext = new Naboo.DataAccess.Model.OSAgnosticContext(ConnectionHandler.ConnectionString());
            Naboo.DataAccess.Model.Trace jobDb = item.Convert();
            dbContext.Trace.Add(jobDb);
            dbContext.SaveChanges();
            result = jobDb.Convert();
            return result;
        }
    }

    public static class TraceExtencions
    {
        public static List<Naboo.Entities.Trace> Convert(this List<Naboo.DataAccess.Model.Trace> items)
        {
            List<Naboo.Entities.Trace> result = new List<Entities.Trace>();
            foreach (var item in items)
            {
                result.Add(item.Convert());
            }
            return result;
        }

        public static Naboo.Entities.Trace Convert(this Naboo.DataAccess.Model.Trace item)
        {
            Naboo.Entities.Trace result = new Naboo.Entities.Trace();
            result.Id = item.Id;
            result.Severity = item.Severity;
            result.Successfully = item.Successfully;
            result.URL = item.Url;
            result.CreateDate = DateTime.Now.ToString();
            result.IP = item.Ip;
            result.JobId = item.JobId;
            return result;
        }

        public static Naboo.DataAccess.Model.Trace Convert(this Naboo.Entities.Trace item)
        {
            Naboo.DataAccess.Model.Trace result = new Naboo.DataAccess.Model.Trace();
            result.Message = item.Message;
            result.Severity = item.Severity;
            result.Successfully = item.Successfully;
            result.Url = item.URL;
            result.CreateDate = DateTime.Now;
            result.Ip = item.IP;
            result.JobId = item.JobId;
            return result;
        }
    }
}