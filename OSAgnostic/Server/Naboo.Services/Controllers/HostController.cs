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

        [HttpGet]
        [Route("Exist")]
        public ActionResult<bool> Exist(string Name)
        {
            return Ok(Naboo.Logic.Handler.HostHandler.Exist(Name));
        }

        [HttpPost]
        [Route("Add")]
        public ActionResult<bool> Add(Naboo.Entities.Host item)
        {
            return Ok(Naboo.Logic.Handler.HostHandler.Add(item));
        }

        [HttpGet]
        [Route("StateChange")]
        public ActionResult<bool> StateChange(int Id, bool State)
        {
            return Ok(Naboo.Logic.Handler.HostHandler.StateChange(Id, State));
        }

        [HttpGet]
        [Route("StateChangeServer")]
        public ActionResult<bool> StateChangeServer()
        {
            return Ok(Naboo.Logic.Handler.HostHandler.StateChangeServer());
        }

    }
}