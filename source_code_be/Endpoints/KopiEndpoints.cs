using JagoanApi.Data;
using JagoanApi.DTOs;
using JagoanApi.Models;
using Microsoft.EntityFrameworkCore;

namespace JagoanApi.Endpoints;

public static class KopiEndpoints
{
    public static void MapKopiEndpoints(this WebApplication app)
    {
        /// GET All Kopi
        app.MapGet("/kopi", async (KopiDb db) =>
        {
            return await db.Kopis.ToListAsync();
        });

        /// GET Kopi By ID
        app.MapGet("/kopi/{id}", async (KopiDb db, int id) =>
        {
            return await db.Kopis.FindAsync(id) is Kopi kopi ? Results.Ok(kopi) : Results.NotFound();
        });

        /// POST Kopi
        app.MapPost("/kopi", async (KopiDb db, CreateKopiDTO request) =>
        {
            if (string.IsNullOrWhiteSpace(request.Name))
            {
                return Results.BadRequest("Nama kopi tidak boleh kosong!");
            }

            if (request.Price < 0)
            {
                return Results.BadRequest("Harga kopi tidak boleh minus!");
            }

            // Mapping : Pindahkan data dari DTO ke model asli (Entity)
            var kopiBaru = new Kopi
            {
                Name = request.Name,
                Price = request.Price
            };

            db.Kopis.Add(kopiBaru);
            await db.SaveChangesAsync();
            return Results.Ok(kopiBaru);
        });
    }
}