﻿using System;
using System.Collections.Generic;

namespace Naboo.DataAccess.Model
{
    public partial class Job
    {
        public int Id { get; set; }
        public string Code { get; set; }
        public string Name { get; set; }
        public int? Interval { get; set; }
        public int HostId { get; set; }
        public string OSType { get; set; }
        public DateTime? CreateDate { get; set; }
        public DateTime? UpdateDate { get; set; }
        public bool? State { get; set; }

        public virtual Host Host { get; set; }
    }
}
