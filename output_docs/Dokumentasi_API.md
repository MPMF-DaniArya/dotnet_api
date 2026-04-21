

---
### 🆕 Update: Tue Apr 21 10:19:04 UTC 2026
Berikut adalah dokumentasi teknis untuk fitur baru pada **Kopi Management API** berdasarkan Git Diff yang disediakan.

# Dokumentasi API: Pengelolaan Data Kopi

Sistem ini memperkenalkan modul pengelolaan data kopi yang menggunakan .NET 10 dan SQLite sebagai database.

## 1. Get All Kopi
Mengambil semua daftar kopi yang tersedia di database.

*   **Endpoint:** `GET /kopi`
*   **Content-Type:** `application/json`
*   **Business Logic:** Mengambil seluruh data dari tabel `Kopis` secara asinkron.

### Response
*   **Success (200 OK)**
    ```json
    [
      {
        "id": 1,
        "name": "Espresso",
        "price": 25000
      },
      {
        "id": 2,
        "name": "Cappuccino",
        "price": 30000
      }
    ]
    ```

---

## 2. Get Kopi By ID
Mengambil detail informasi satu produk kopi berdasarkan ID unik.

*   **Endpoint:** `GET /kopi/{id}`
*   **Path Parameter:** `id` (integer)
*   **Business Logic:** Melakukan pencarian berdasarkan Primary Key. Jika data ditemukan, mengembalikan objek kopi. Jika tidak, mengembalikan status 404.

### Response
*   **Success (200 OK)**
    ```json
    {
      "id": 1,
      "name": "Espresso",
      "price": 25000
    }
    ```
*   **Not Found (404 Not Found)**
    *(Empty Body)*

---

## 3. Create Kopi
Menambahkan data kopi baru ke dalam sistem.

*   **Endpoint:** `POST /kopi`
*   **Content-Type:** `application/json`
*   **Business Logic:**
    *   Melakukan validasi input: Nama tidak boleh kosong dan harga tidak boleh negatif.
    *   Melakukan mapping dari `CreateKopiDTO` ke entity `Kopi`.
    *   Menyimpan data ke database dan mengembalikan objek yang berhasil dibuat (termasuk ID yang di-generate sistem).

### Request Body
| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `name` | string | Yes | Nama produk kopi |
| `price` | int | Yes | Harga produk (minimal 0) |

```json
{
  "name": "Latte",
  "price": 35000
}
```

### Response
*   **Success (200 OK)**
    ```json
    {
      "id": 3,
      "name": "Latte",
      "price": 35000
    }
    ```
*   **Bad Request (400 Bad Request)** - Jika nama kosong:
    ```text
    "Nama kopi tidak boleh kosong!"
    ```
*   **Bad Request (400 Bad Request)** - Jika harga minus:
    ```text
    "Harga kopi tidak boleh minus!"
    ```

---

## Data Schema (DTO)

### CreateKopiDTO / UpdateKopiDTO
Digunakan untuk pengiriman data dari klien ke server.
```csharp
public record CreateKopiDTO(string Name, int Price);
```

### Kopi Model (Entity)
Struktur data yang tersimpan di database SQLite.
```csharp
public class Kopi
{
    public int Id { get; set; } // Primary Key, Autoincrement
    public string Name { get; set; }
    public int Price { get; set; }
}
```
