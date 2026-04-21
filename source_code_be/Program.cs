using JagoanApi.Data;
using JagoanApi.Endpoints;
using Microsoft.EntityFrameworkCore;

var builder = WebApplication.CreateBuilder(args);

// Konfigurasi Database
builder.Services.AddDbContext<KopiDb>(opt => opt.UseSqlite("Data Source=kopi.db"));

var app = builder.Build();

app.MapKopiEndpoints();

app.Run();