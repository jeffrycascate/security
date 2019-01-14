using System;
using System.Collections.Generic;

namespace Naboo.DataAccess.Model
{
    public partial class Host
    {
        public Host()
        {
            Job = new HashSet<Job>();
        }

        public int Id { get; set; }
        public string Name { get; set; }
        public string IPLocal { get; set; }
        public string IPPublic { get; set; }
        public string MacAddress { get; set; }
        public bool? State { get; set; }
        public DateTime? CreateDate { get; set; }
        public DateTime? UpdateDate { get; set; }
        public string OSName { get; set; }
        public string OSSystem { get; set; }
        public string OSRelease { get; set; }
        public string OSArchitecture { get; set; }

        public virtual ICollection<Job> Job { get; set; }
    }
}
