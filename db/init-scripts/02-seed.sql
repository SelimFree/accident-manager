INSERT INTO public.users (user_id, name, email, password_hash, role, is_active) VALUES
('11111111-1111-1111-1111-111111111111', 'Admin', 'admin@urbanpulse.com', 'NEEDS_HASHING', 'admin', true),
('22222222-2222-2222-2222-222222222222', 'Selim', 'selim@student.com', 'NEEDS_HASHING', 'user', true);

-- Note: ST_MakePoint takes (Longitude, Latitude)
INSERT INTO public.accidents (accident_id, reporter_id, title, description, status, category, severity, location) VALUES
(
    '33333333-3333-3333-3333-333333333333', 
    '22222222-2222-2222-2222-222222222222', 
    'Major Pothole on Main Bridge', 
    'Deep pothole causing traffic slowdowns in the right lane.', 
    'pending',
    'pothole',
    'medium', 
    ST_SetSRID(ST_MakePoint(19.0402, 47.4979), 4326)
),
(
    '44444444-4444-4444-4444-444444444444', 
    '22222222-2222-2222-2222-222222222222', 
    'Broken Traffic Light', 
    'Traffic light at the intersection is completely off.', 
    'approved', 
    'traffic_light',
    'high',
    ST_SetSRID(ST_MakePoint(19.0600, 47.5000), 4326)
);

INSERT INTO public.comments (comment_id, author_id, accident_id, content) VALUES
(
    '55555555-5555-5555-5555-555555555555',
    '11111111-1111-1111-1111-111111111111',
    '44444444-4444-4444-4444-444444444444',
    'Maintenance crew has been dispatched and should arrive in 30 minutes.'
);