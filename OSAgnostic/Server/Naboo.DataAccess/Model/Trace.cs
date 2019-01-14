using System;
using System.Collections.Generic;

namespace Naboo.DataAccess.Model
{
    public partial class Trace
    {
        public int Id { get; set; }
        public string Message { get; set; }
        public string Severity { get; set; }
        public bool? Successfully { get; set; }
        public string Url { get; set; }
        public DateTime? CreateDate { get; set; }
        public string Ip { get; set; }
        public int? JobId { get; set; }
    }
}
