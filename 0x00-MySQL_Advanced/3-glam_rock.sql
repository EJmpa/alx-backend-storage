-- List bands with 'Glam rock' as their main style, ranked by longevity until 2022

-- Import the table dump: metal_bands.sql.zip
-- Column names are band_name and lifespan (in years until 2022)
-- The script uses attributes formed and split to compute the lifespan

SELECT band_name,
       CASE
           WHEN split IS NULL THEN 2022 - formed  -- If the band is still active, calculate lifespan until 2022
           ELSE split - formed  -- If the band has split, calculate the actual lifespan
       END AS lifespan
FROM metal_bands
WHERE style = 'Glam rock'
ORDER BY lifespan DESC;
