namespace JagoanApi.DTOs;

// DTO untuk menerima data saat create (Tanpa ID)
public record CreateKopiDTO(string Name, int Price);

// DTO untuk meneriam data saat update (Tanpa id, karena ID lewat URL)
public record UpdateKopiDTO(string Name, int Price);