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
        public ActionResult<IEnumerable<Naboo.Entities.Job>> JobByHostId(int HostId)
        {
            return Ok(Logic.Handler.JobHandler.JobByHostId(HostId));
        }

        [HttpGet]
        [Route("Exist")]
        public ActionResult<bool> Exist(string Code, int HostId)
        {
            return Ok(Naboo.Logic.Handler.JobHandler.Exist(Code, HostId));
        }

        [HttpPost]
        [Route("Add")]
        public ActionResult<bool> Add(Naboo.Entities.Job item)
        {
            return Ok(Naboo.Logic.Handler.JobHandler.Add(item));
        }
    }
}