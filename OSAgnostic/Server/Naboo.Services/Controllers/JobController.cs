using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Configuration;
using System.Collections.Generic;

namespace Naboo.Services.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class JobController : ControllerBase
    {
        public IConfiguration Configuration { get; }

        [HttpGet]
        [Route("JobByHostId")]
        public ActionResult<IEnumerable<Naboo.DataAccess.Model.Job>> JobByHostId(int HostId)
        {
            return Ok(Logic.Handler.JobHandler.JobByHostId(HostId));
        }
    }
}