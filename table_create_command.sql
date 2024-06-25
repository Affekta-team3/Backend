-- Drop the dbo.submission table if it exists
IF OBJECT_ID ('dbo.submission', 'U') IS NOT NULL
DROP TABLE dbo.submission;

-- Drop the dbo.problem table if it exists
IF OBJECT_ID ('dbo.problem', 'U') IS NOT NULL
DROP TABLE dbo.problem;

-- Create the dbo.problem table with the new columns
CREATE TABLE dbo.problem (
    id NVARCHAR (36) PRIMARY KEY DEFAULT NEWID (),
    title NVARCHAR (200) NOT NULL,
    description NVARCHAR (200) NULL,
    input_format NVARCHAR (100) NULL,
    output_format NVARCHAR (100) NULL,
    difficulty INT NOT NULL,
    totalSubmissions INT NOT NULL DEFAULT 0,
    successfulSubmissions INT NOT NULL DEFAULT 0
);

-- Create the dbo.submission table
CREATE TABLE dbo.submission (
    id NVARCHAR (36) PRIMARY KEY DEFAULT NEWID (),
    problem_id NVARCHAR (36) NOT NULL,
    code_text NVARCHAR (500) NOT NULL,
    status INT NOT NULL,
    result NVARCHAR (200) NOT NULL,
    runtime INT NOT NULL,
    memory INT NOT NULL,
    FOREIGN KEY (problem_id) REFERENCES dbo.problem (id)
);

-- Insert data into the dbo.problem table with sample_path same as id
DECLARE @id1 NVARCHAR (36) = NEWID ();

DECLARE @id2 NVARCHAR (36) = NEWID ();

INSERT INTO
    dbo.problem (
        id,
        title,
        description,
        input_format,
        output_format,
        sample_path,
        difficulty,
        totalSubmissions,
        successfulSubmissions
    )
VALUES (
        @id1,
        'Sample Problem 1',
        'This is a description for problem 1',
        'Input format for problem 1',
        'Output format for problem 1',
        1,
        10,
        5
    ),
    (
        @id2,
        'Sample Problem 2',
        'This is a description for problem 2',
        'Input format for problem 2',
        'Output format for problem 2',
        2,
        20,
        10
    );

-- Retrieve problem IDs to use in the submission table
DECLARE @problem1Id NVARCHAR (36), @problem2Id NVARCHAR (36);

SELECT @problem1Id = id
FROM dbo.problem
WHERE
    title = 'Sample Problem 1';

SELECT @problem2Id = id
FROM dbo.problem
WHERE
    title = 'Sample Problem 2';

-- Insert data into the dbo.submission table
INSERT INTO
    dbo.submission (
        id,
        problem_id,
        code_text,
        status,
        result,
        runtime,
        memory
    )
VALUES (
        NEWID (),
        @problem1Id,
        'print("Hello World")',
        0,
        'Accepted',
        10,
        256
    ),
    (
        NEWID (),
        @problem2Id,
        'print("Hello Azure")',
        1,
        'Failed',
        20,
        512
    );

CREATE TABLE dbo.[user] (
    userId NVARCHAR(36) PRIMARY KEY,
    username NVARCHAR(100) NOT NULL,
    email NVARCHAR(100) NOT NULL,
    totalSubmissions INT NOT NULL DEFAULT 0,
    successfulSubmissions INT NOT NULL DEFAULT 0
);