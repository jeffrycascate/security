using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Configuration;
using System.Collections.Generic;

namespace Naboo.Services.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class HostController : ControllerBase
    {
        public IConfiguration Configuration { get; }

        [HttpGet]
        [Route("All")]
        public ActionResult<IEnumerable<Naboo.DataAccess.Model.Host>> All()
        {
            return Ok(Naboo.Logic.Handler.HostHandler.All());
        }
    }
}