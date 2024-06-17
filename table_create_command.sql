-- Drop the dbo.submission table if it exists
IF OBJECT_ID ('dbo.submission', 'U') IS NOT NULL
DROP TABLE dbo.submission;

-- Drop the dbo.problem table if it exists
IF OBJECT_ID ('dbo.problem', 'U') IS NOT NULL
DROP TABLE dbo.problem;

-- Create the dbo.problem table
CREATE TABLE dbo.problem (
    id NVARCHAR (36) PRIMARY KEY DEFAULT NEWID (),
    title NVARCHAR (200) NOT NULL,
    description NVARCHAR (200) NULL,
    input_format NVARCHAR (100) NULL,
    output_format NVARCHAR (100) NULL,
    sample_path NVARCHAR (200) NOT NULL,
    difficulty INT NOT NULL
);

-- Create the dbo.submission table
CREATE TABLE dbo.submission (
    Id NVARCHAR (36) PRIMARY KEY DEFAULT NEWID (),
    problemId NVARCHAR (36) NOT NULL,
    code_text NVARCHAR (500) NOT NULL,
    status INT NOT NULL,
    result NVARCHAR (200) NOT NULL,
    runtime INT NOT NULL,
    memory INT NOT NULL,
    FOREIGN KEY (problemId) REFERENCES dbo.problem (id)
);

-- Insert data into the dbo.problem table
INSERT INTO
    dbo.problem (
        id,
        title,
        description,
        input_format,
        output_format,
        sample_path,
        difficulty
    )
VALUES (
        NEWID (),
        'Sample Problem 1',
        'This is a description for problem 1',
        'Input format for problem 1',
        'Output format for problem 1',
        '/samples/sample1',
        1
    ),
    (
        NEWID (),
        'Sample Problem 2',
        'This is a description for problem 2',
        'Input format for problem 2',
        'Output format for problem 2',
        '/samples/sample2',
        2
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
        Id,
        problemId,
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