using System;

namespace Naboo.Entities
{
    public class Trace
    {
        public int Id { get; set; }
        public string Message { get; set; }
        public string  Severity { get; set; }
        public bool Successfully { get; set; }
        public string URL { get; set; }
        public string CreateDate { get; set; }
        public string IP { get; set; }
        public int? JobId { get; set; }
    }
}