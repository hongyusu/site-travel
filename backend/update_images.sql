-- Update activity_images to use ID-based picsum URLs
UPDATE activity_images 
SET url = 'https://picsum.photos/id/' || (id % 200 + 100) || '/800/600'
WHERE url LIKE '%picsum.photos%';

-- Update users profile images
UPDATE users 
SET profile_image_url = 'https://picsum.photos/id/' || (id % 50 + 10) || '/200/200'
WHERE profile_image_url LIKE '%picsum.photos%';

-- Update vendor logo images  
UPDATE vendors
SET logo_url = 'https://picsum.photos/id/' || (id % 30 + 50) || '/300/300'
WHERE logo_url LIKE '%picsum.photos%';

-- Update review images
UPDATE review_images
SET url = 'https://picsum.photos/id/' || (id % 150 + 150) || '/600/400'
WHERE url LIKE '%picsum.photos%';

-- Update meeting point photos
UPDATE meeting_point_photos
SET url = 'https://picsum.photos/id/' || (id % 100 + 300) || '/800/600'
WHERE url LIKE '%picsum.photos%';
