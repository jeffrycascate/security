using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Configuration;
using System.Collections.Generic;

namespace Naboo.Services.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class TraceController : ControllerBase
    {
        public IConfiguration Configuration { get; }

        [HttpGet]
        [Route("TraceByJobId")]
        public ActionResult<IEnumerable<Naboo.DataAccess.Model.Trace>> TraceByJobId(int JobId)
        {
            return Ok(Logic.Handler.TraceHandler.TraceByJobId(JobId));
        }

        [HttpPost]
        [Route("Add")]
        public ActionResult<bool> Add(Naboo.Entities.Trace item)
        {
            return Ok(Naboo.Logic.Handler.TraceHandler.Add(item));
        }
    }
}