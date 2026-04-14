-- Update destination images
UPDATE destinations 
SET image_url = 'https://loremflickr.com/1200/800/travel,' || LOWER(REPLACE(name, ' ', '')) || '?lock=' || id
WHERE image_url LIKE '%picsum%';

-- Update activity timeline images  
UPDATE activity_timelines
SET image_url = 'https://loremflickr.com/600/400/travel,activity?lock=' || id
WHERE image_url LIKE '%picsum%';
