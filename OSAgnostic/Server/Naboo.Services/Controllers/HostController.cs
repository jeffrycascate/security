using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Cors;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Configuration;
using Naboo.DataAccess.Model;

namespace Naboo.Services.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class HostController : ControllerBase
    {
        public IConfiguration Configuration { get; }

        [HttpGet]
        public ActionResult<IEnumerable<Naboo.DataAccess.Model.Host>> Get()
        {
            var dbContext = new Naboo.DataAccess.Model.OSAgnosticContext(Handler.ConnectionHandler.ConnectionString());
            var hosts = dbContext.Host.OrderByDescending(c => c.State).ToList();
            return Ok(hosts);
        }
    }
}