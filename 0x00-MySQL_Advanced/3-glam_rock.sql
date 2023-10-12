-- List bands with 'Glam rock' as their main style, ranked by longevity until 2022
SELECT band_name, 
       CASE 
           WHEN formed > 2022 THEN 0  -- If the band was formed after 2022, set lifespan to 0
           WHEN split > 2022 THEN 2022 - formed  -- If the band split after 2022, calculate lifespan until 2022
           ELSE split - formed  -- If neither, calculate the actual lifespan
       END AS lifespan
FROM metal_bands
WHERE band_style = 'Glam rock'
ORDER BY lifespan DESC;
