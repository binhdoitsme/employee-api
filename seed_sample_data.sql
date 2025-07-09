-- Sample data for employee-api

-- Departments
INSERT INTO department (id, name) VALUES
    ('11111111-1111-1111-1111-111111111111', 'Engineering'),
    ('22222222-2222-2222-2222-222222222222', 'HR');

-- Positions
INSERT INTO position (id, name) VALUES
    ('33333333-3333-3333-3333-333333333333', 'Software Engineer'),
    ('44444444-4444-4444-4444-444444444444', 'HR Manager');

-- Locations
INSERT INTO location (id, name) VALUES
    ('55555555-5555-5555-5555-555555555555', 'New York'),
    ('66666666-6666-6666-6666-666666666666', 'San Francisco');

-- Employees
INSERT INTO employee (
    id, org_id, company_id, first_name, last_name, email, phone_number,
    department_id, position_id, location_id, status
) VALUES
    ('aaaaaaa1-aaaa-aaaa-aaaa-aaaaaaaaaaa1', 'bbbbbbb1-bbbb-bbbb-bbbb-bbbbbbbbbbb1', 'ccccccc1-cccc-cccc-cccc-ccccccccccc1',
     'Alice', 'Smith', 'alice@example.com', '123-456-7890',
     '11111111-1111-1111-1111-111111111111', '33333333-3333-3333-3333-333333333333', '55555555-5555-5555-5555-555555555555', 'ACTIVE'),
    ('aaaaaaa2-aaaa-aaaa-aaaa-aaaaaaaaaaa2', 'bbbbbbb1-bbbb-bbbb-bbbb-bbbbbbbbbbb1', 'ccccccc2-cccc-cccc-cccc-ccccccccccc2',
     'Bob', 'Johnson', 'bob@example.com', '234-567-8901',
     '22222222-2222-2222-2222-222222222222', '44444444-4444-4444-4444-444444444444', '66666666-6666-6666-6666-666666666666', 'NOT_STARTED'),
    ('aaaaaaa3-aaaa-aaaa-aaaa-aaaaaaaaaaa3', 'bbbbbbb2-bbbb-bbbb-bbbb-bbbbbbbbbbb2', 'ccccccc1-cccc-cccc-cccc-ccccccccccc1',
     'Carol', 'Williams', 'carol@example.com', '345-678-9012',
     '11111111-1111-1111-1111-111111111111', '33333333-3333-3333-3333-333333333333', '55555555-5555-5555-5555-555555555555', 'TERMINATED');
