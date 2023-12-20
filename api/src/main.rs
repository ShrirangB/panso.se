use actix_web::{web, App, HttpResponse, HttpServer};
use tokio_postgres::NoTls;

#[derive(serde::Serialize)]
struct Ean {
    ean: String,
    name: String,
}

async fn list_eans() -> Result<HttpResponse, actix_web::Error> {
    // Read from .env file
    dotenvy::dotenv().ok();
    let db_host: String = dotenvy::var("POSTGRES_HOST").unwrap();
    let db_user: String = dotenvy::var("POSTGRES_USER").unwrap();
    let db_password: String = dotenvy::var("POSTGRES_PASSWORD").unwrap();

    // Connect to the database
    let (client, connection) = tokio_postgres::connect(
        &format!(
            "host={} user={} password={} dbname=panso",
            db_host, db_user, db_password
        ),
        NoTls,
    )
    .await
    .map_err(|e| {
        eprintln!("Error connecting to the database: {}", e);
        actix_web::error::ErrorInternalServerError("Internal Server Error")
    })?;

    // Spawn a new task to handle the database connection
    tokio::spawn(async move {
        if let Err(e) = connection.await {
            eprintln!("Database connection error: {}", e);
        }
    });

    // Perform the database query
    let statement: tokio_postgres::Statement = client
        .prepare("SELECT ean, name FROM eans")
        .await
        .map_err(|e| {
        eprintln!("Error preparing query: {}", e);
        actix_web::error::ErrorInternalServerError("Internal Server Error")
    })?;

    let rows: Vec<tokio_postgres::Row> = client.query(&statement, &[]).await.map_err(|e| {
        eprintln!("Error executing query: {}", e);
        actix_web::error::ErrorInternalServerError("Internal Server Error")
    })?;

    // Convert the rows to Ean structs
    let eans: Vec<Ean> = rows
        .iter()
        .map(|row| Ean {
            ean: row.get(0),
            name: row.get(1),
        })
        .collect();

    Ok(HttpResponse::Ok().json(eans))
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    HttpServer::new(|| App::new().service(web::resource("/eans").route(web::get().to(list_eans))))
        .bind("127.0.0.1:8080")?
        .run()
        .await
}
