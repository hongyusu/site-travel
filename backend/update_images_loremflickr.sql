-- Update activity_images with travel-themed real photos
UPDATE activity_images 
SET url = CASE 
    WHEN id % 10 = 0 THEN 'https://loremflickr.com/800/600/travel,landscape?lock=' || id
    WHEN id % 10 = 1 THEN 'https://loremflickr.com/800/600/travel,architecture?lock=' || id
    WHEN id % 10 = 2 THEN 'https://loremflickr.com/800/600/travel,food?lock=' || id
    WHEN id % 10 = 3 THEN 'https://loremflickr.com/800/600/travel,museum?lock=' || id
    WHEN id % 10 = 4 THEN 'https://loremflickr.com/800/600/travel,nature?lock=' || id
    WHEN id % 10 = 5 THEN 'https://loremflickr.com/800/600/travel,city?lock=' || id
    WHEN id % 10 = 6 THEN 'https://loremflickr.com/800/600/travel,beach?lock=' || id
    WHEN id % 10 = 7 THEN 'https://loremflickr.com/800/600/travel,mountain?lock=' || id
    WHEN id % 10 = 8 THEN 'https://loremflickr.com/800/600/travel,culture?lock=' || id
    ELSE 'https://loremflickr.com/800/600/travel,adventure?lock=' || id
END;

-- Update vendor logos
UPDATE vendors
SET logo_url = 'https://loremflickr.com/300/300/logo,business?lock=' || (id + 1000);

-- Update review images  
UPDATE review_images
SET url = 'https://loremflickr.com/600/400/travel,vacation?lock=' || (id + 2000);

-- Update meeting point photos
UPDATE meeting_point_photos
SET url = 'https://loremflickr.com/800/600/travel,location?lock=' || (id + 3000);
