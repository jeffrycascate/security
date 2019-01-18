using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using System.Text;

namespace Naboo.DataAccess.Model
{
    public partial class OSAgnosticContext : DbContext
    {
        public string ConnectionString;
        public OSAgnosticContext(string ConnectionString)
        {
            this.ConnectionString = ConnectionString;
        }

        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        {
            if (!optionsBuilder.IsConfigured)
            {
                optionsBuilder.UseMySql(this.ConnectionString);
            }
        }
    }
}
