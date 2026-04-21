using Microsoft.EntityFrameworkCore;
using JagoanApi.Models;

namespace JagoanApi.Data;

public class KopiDb : DbContext
{
    public KopiDb(DbContextOptions<KopiDb> options) : base(options) { }

    public DbSet<Kopi> Kopis => Set<Kopi>();
}