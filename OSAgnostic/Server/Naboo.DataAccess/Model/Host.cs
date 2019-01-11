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
        public string Iplocal { get; set; }
        public string Ippublic { get; set; }
        public string MacAddress { get; set; }
        public bool? State { get; set; }
        public DateTime? CreateDate { get; set; }
        public DateTime? UpdateDate { get; set; }
        public string Osname { get; set; }
        public string Ossystem { get; set; }
        public string Osrelease { get; set; }
        public string Osarchitecture { get; set; }

        public virtual ICollection<Job> Job { get; set; }
    }
}
