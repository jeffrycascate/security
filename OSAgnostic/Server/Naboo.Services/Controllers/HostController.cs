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
            var connection = Configuration.GetConnectionString("Dev2");
            var dbContext = new Naboo.DataAccess.Model.OSAgnosticContext("server=186.177.106.36;database=osagnostic;user=root;pwd=Jcv1821@t5");
            var hosts = dbContext.Host.Where(c=> c.State== true).ToList();
            if(hosts != null)
            {
                foreach (var item in hosts)
                {
                    item.Job = new List<Job>();
                    item.Job = dbContext.Job.Where(c =>  c.HostId== item.Id).ToList(); 
                }
            }
            return hosts;
        }
    }
}