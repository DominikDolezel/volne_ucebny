<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Volné učebny</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
    <?php
      $data = file_get_contents("data.json");
      $ucebny = json_decode($data, true);
    ?>
  </head>
  <body>
    <h3>Volné učebny</h3>
    <h4>Jaroška</h4>
    <table class="table">
      <thead>
        <tr>
          <th scope="col">#</th>
          <?php
            for($i = 0; $i <= 9; $i++) {
              echo "<th scope='col'>$i. hodina</th>";
            }
          ?>
        </tr>
      </thead>
      <tbody>
        <?php
          for($podlazi = 2; $podlazi <= 5; $podlazi++) {
            echo "<tr><th scope='row'>$podlazi. podlaží</th>";
            for($hodina = 0; $hodina <= 9; $hodina++) {
              echo "<td>";
              for($i = 0; $i < count($ucebny[0][$hodina][$podlazi-2]); $i++) {
                echo $ucebny[0][$hodina][$podlazi-2][$i]["name"] . "<br>";
              }
              echo "</td>";
            }
            echo "</tr>";
          }
        ?>

      </tbody>
    </table>
    <h4>Příční</h4>
    <table class="table">
      <thead>
        <tr>
          <th scope="col">#</th>
          <?php
            for($i = 0; $i <= 9; $i++) {
              echo "<th scope='col'>$i. hodina</th>";
            }
          ?>
        </tr>
      </thead>
      <tbody>
        <?php
          for($podlazi = 1; $podlazi <= 3; $podlazi++) {
            echo "<tr><th scope='row'>$podlazi. podlaží</th>";
            for($hodina = 0; $hodina <= 9; $hodina++) {
              echo "<td>";
              for($i = 0; $i < count($ucebny[1][$hodina][$podlazi-1]); $i++) {
                echo $ucebny[1][$hodina][$podlazi-1][$i]["name"] . "<br>";
              }
              echo "</td>";
            }
            echo "</tr>";
          }
        ?>

      </tbody>
    </table>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
  </body>
</html>
