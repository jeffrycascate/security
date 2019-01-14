using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Configuration;
using System.Collections.Generic;
using System.Linq;

namespace Naboo.Services.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class TraceController : ControllerBase
    {
        public IConfiguration Configuration { get; }

        [HttpGet]
        public ActionResult<IEnumerable<Naboo.DataAccess.Model.Trace>> Get(int Id)
        {
            var dbContext = new Naboo.DataAccess.Model.OSAgnosticContext(Handler.ConnectionHandler.ConnectionString());
            var hosts = dbContext.Trace.Where(c => c.JobId == Id).OrderBy(f => f.Id).ToList();
            return Ok(hosts);
        }
    }
}