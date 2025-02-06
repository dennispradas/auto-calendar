<?php
// DB
define('DB_HOST', 'localhost');
define('DB_USER', 'local'); // Usuari
define('DB_PASSWORD', 'dp3879dp'); // Password
define('DB_NAME', 'form'); // Nom BBDD

function connectDatabase() {
    $mysqli = new mysqli(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME);
    if ($mysqli->connect_error) {
        die("Error al conectar con la base de datos: " . $mysqli->connect_error);
    }
    return $mysqli;
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $nombre = $_POST['nombre'];
    $fechaInicio = $_POST['fecha_inicio'];
    $fechaFin = $_POST['fecha_fin'];
    $email = $_POST['email'];

    $mysqli = connectDatabase();

    $query = "INSERT INTO eventos (nombre, fecha_inicio, fecha_fin, email) VALUES (?, ?, ?, ?)";
    $stmt = $mysqli->prepare($query);
    
    if (!$stmt) {
        die("Error al preparar la consulta: " . $mysqli->error);
    }

    $stmt->bind_param("ssss", $nombre, $fechaInicio, $fechaFin, $email);

    if ($stmt->execute()) {
        echo "[INFO] Evento guardado correctamente.\n";

        $command = escapeshellcmd("python3 query.py");
        $output = shell_exec($command);

        if ($output) {
            echo "[INFO] Salida del script Python: <pre>$output</pre>";
        } else {
            echo "[ERROR] El script Python no se ejecutó correctamente.";
        }
        echo "[INFO] Evento enviado a Google Calendar.\n";
    } else {
        echo "[ERROR] Error al guardar los datos: " . $stmt->error;
    }

    $stmt->close();
    $mysqli->close();
}
?>
