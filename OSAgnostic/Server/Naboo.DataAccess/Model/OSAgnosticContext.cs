using System;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata;

namespace Naboo.DataAccess.Model
{
    public partial class OSAgnosticContext : DbContext
    {
        public OSAgnosticContext()
        {
        }

        public OSAgnosticContext(DbContextOptions<OSAgnosticContext> options)
            : base(options)
        {
        }

        public virtual DbSet<Host> Host { get; set; }
        public virtual DbSet<Job> Job { get; set; }
        public virtual DbSet<Trace> Trace { get; set; }

       
        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            modelBuilder.Entity<Host>(entity =>
            {
                entity.ToTable("host");

                entity.HasIndex(e => e.Id)
                    .HasName("Id_UNIQUE")
                    .IsUnique();

                entity.Property(e => e.Id).HasColumnType("int(11)");

                entity.Property(e => e.CreateDate).HasColumnType("datetime");

                entity.Property(e => e.IPLocal)
                    .HasColumnName("IPLocal")
                    .HasColumnType("varchar(128)");

                entity.Property(e => e.IPPublic)
                    .HasColumnName("IPPublic")
                    .HasColumnType("varchar(128)");

                entity.Property(e => e.MacAddress).HasColumnType("varchar(128)");

                entity.Property(e => e.Name).HasColumnType("varchar(128)");

                entity.Property(e => e.OSArchitecture)
                    .HasColumnName("OSArchitecture")
                    .HasColumnType("varchar(128)");

                entity.Property(e => e.OSName)
                    .HasColumnName("OSName")
                    .HasColumnType("varchar(128)");

                entity.Property(e => e.OSRelease)
                    .HasColumnName("OSRelease")
                    .HasColumnType("varchar(128)");

                entity.Property(e => e.OSSystem)
                    .HasColumnName("OSSystem")
                    .HasColumnType("varchar(128)");

                entity.Property(e => e.State).HasColumnType("bit(1)");

                entity.Property(e => e.UpdateDate).HasColumnType("datetime");
            });

            modelBuilder.Entity<Job>(entity =>
            {
                entity.HasKey(e => new { e.Id, e.HostId })
                    .HasName("PRIMARY");

                entity.ToTable("job");

                entity.HasIndex(e => e.HostId)
                    .HasName("FK_HostId");

                entity.HasIndex(e => e.Id)
                    .HasName("Id_5");

                entity.Property(e => e.Id)
                    .HasColumnType("int(11)")
                    .ValueGeneratedOnAdd();

                entity.Property(e => e.HostId).HasColumnType("int(11)");

                entity.Property(e => e.Code).HasColumnType("varchar(128)");

                entity.Property(e => e.CreateDate).HasColumnType("datetime");

                entity.Property(e => e.Interval).HasColumnType("int(11)");

                entity.Property(e => e.Name).HasColumnType("varchar(255)");

                entity.Property(e => e.Ostype)
                    .HasColumnName("OSType")
                    .HasColumnType("varchar(128)");

                entity.Property(e => e.State).HasColumnType("bit(1)");

                entity.Property(e => e.UpdateDate).HasColumnType("datetime");

                entity.HasOne(d => d.Host)
                    .WithMany(p => p.Job)
                    .HasForeignKey(d => d.HostId)
                    .HasConstraintName("FK_HostId");
            });

            modelBuilder.Entity<Trace>(entity =>
            {
                entity.ToTable("trace");

                entity.HasIndex(e => e.JobId)
                    .HasName("FKJob_");

                entity.Property(e => e.Id).HasColumnType("int(11)");

                entity.Property(e => e.CreateDate).HasColumnType("datetime");

                entity.Property(e => e.Ip)
                    .HasColumnName("IP")
                    .HasColumnType("varchar(255)");

                entity.Property(e => e.JobId).HasColumnType("int(11)");

                entity.Property(e => e.Message).HasColumnType("varchar(2000)");

                entity.Property(e => e.Severity).HasColumnType("varchar(255)");

                entity.Property(e => e.Successfully).HasColumnType("bit(1)");

                entity.Property(e => e.Url)
                    .HasColumnName("URL")
                    .HasColumnType("varchar(255)");
            });
        }
    }
}
