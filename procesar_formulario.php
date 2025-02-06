<?php
// Configuración de la base de datos
define('DB_HOST', 'localhost');
define('DB_USER', 'local'); // Cambia por tu usuario de MySQL
define('DB_PASSWORD', 'dp3879dp'); // Cambia por tu contraseña de MySQL
define('DB_NAME', 'form'); // Cambia por el nombre de tu base de datos

// Conexión a la base de datos
function connectDatabase() {
    $mysqli = new mysqli(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME);
    if ($mysqli->connect_error) {
        die("Error al conectar con la base de datos: " . $mysqli->connect_error);
    }
    return $mysqli;
}

// Procesar el formulario
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $nombre = $_POST['nombre'];
    $fechaInicio = $_POST['fecha_inicio'];
    $fechaFin = $_POST['fecha_fin'];
    $email = $_POST['email'];

    // Conexión a la base de datos
    $mysqli = connectDatabase();

    // Insertar los datos en la base de datos
    $query = "INSERT INTO eventos (nombre, fecha_inicio, fecha_fin, email) VALUES (?, ?, ?, ?)";
    $stmt = $mysqli->prepare($query);
    
    if (!$stmt) {
        die("Error al preparar la consulta: " . $mysqli->error);
    }

    $stmt->bind_param("ssss", $nombre, $fechaInicio, $fechaFin, $email);

    if ($stmt->execute()) {
        echo "[INFO] Evento guardado correctamente.\n";

        // Ejecutar el script Python para crear el evento en Google Calendar
        // Ejecutar el script Python y capturar la salida
        $command = escapeshellcmd("python3 /ruta/a/tu/script/create_google_event.py");
        $output = shell_exec($command);

        // Verificar la salida
        if ($output) {
            echo "[INFO] Salida del script Python: <pre>$output</pre>";
        } else {
            echo "[ERROR] El script Python no se ejecutó correctamente.";
        }
        echo "[INFO] Evento enviado a Google Calendar.\n";
    } else {
        echo "[ERROR] Error al guardar los datos: " . $stmt->error;
    }

    // Cerrar conexión
    $stmt->close();
    $mysqli->close();
}
?>
