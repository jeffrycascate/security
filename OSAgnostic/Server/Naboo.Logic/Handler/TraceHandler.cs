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
    }
}
