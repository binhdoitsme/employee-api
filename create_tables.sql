-- SQL schema for employee-api

CREATE TYPE employeestatus AS ENUM ('ACTIVE', 'NOT_STARTED', 'TERMINATED');

CREATE TABLE department (
    id UUID PRIMARY KEY,
    name VARCHAR NOT NULL
);

CREATE TABLE position (
    id UUID PRIMARY KEY,
    name VARCHAR NOT NULL
);

CREATE TABLE location (
    id UUID PRIMARY KEY,
    name VARCHAR NOT NULL
);

CREATE TABLE employee (
    id UUID PRIMARY KEY,
    org_id UUID NOT NULL,
    company_id UUID NOT NULL,
    first_name VARCHAR NOT NULL,
    last_name VARCHAR NOT NULL,
    email VARCHAR,
    phone_number VARCHAR,
    department_id UUID REFERENCES department(id),
    position_id UUID REFERENCES position(id),
    location_id UUID REFERENCES location(id),
    status employeestatus NOT NULL,
    CONSTRAINT ix_employee_status_location_department_company UNIQUE (status, location_id, department_id, company_id)
);

CREATE INDEX idx_employee_status_location_department_company
    ON employee (status, location_id, department_id, company_id);
