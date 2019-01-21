using Naboo.DataAccess.Model;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;

namespace Naboo.Entities
{
    public class Host
    {
        public int Id { get; set; }
        public string Name { get; set; }
        public string IPLocal { get; set; }
        public string IPPublic { get; set; }
        public string MacAddress { get; set; }
        public bool? State { get; set; }
        public DateTime CreateDate { get; set; }
        public DateTime UpdateDate { get; set; }
        public string OSName { get; set; }
        public string OSSystem { get; set; }
        public string OSRelease { get; set; }
        public string OSArchitecture { get; set; }

        public  List<Job> Job { get; set; }
        public int JobActive { get; set; }
        public int JobInaActive { get; set; }

        public OS OS { get; set; }

    }
}