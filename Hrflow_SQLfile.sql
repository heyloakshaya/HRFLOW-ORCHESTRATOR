USE hrflowdb;
CREATE TABLE employee (
    emp_id             VARCHAR(20)    PRIMARY KEY,
    emp_name           VARCHAR(100)   NOT NULL,
    email              VARCHAR(100)   UNIQUE NOT NULL,
    password           VARCHAR(64),
    phone              VARCHAR(15),
    department         VARCHAR(50),
    role               VARCHAR(50),
    performance_rating DECIMAL(3,1)   DEFAULT 0.0,
    total_leave        INT            DEFAULT 30,
    used_leave         INT            DEFAULT 0,
    created_at         DATETIME       DEFAULT NOW(),
    updated_at         DATETIME       DEFAULT NOW()
);
INSERT INTO employee (emp_id, emp_name, email, password, phone, department, role, performance_rating, total_leave, used_leave)
VALUES
('EMP001', 'Jagadish Itikala',  'jagadish@xyz.com',  SHA2('admin123', 256), '9876543210', 'Engineering',  'HR',       4.5, 30, 2),
('EMP002', 'Akshaya Sharma',    'akshaya@xyz.com',   SHA2('emp123',   256), '9876543211', 'Engineering',  'EMPLOYEE', 3.8, 30, 5),
('EMP003', 'Ravi Kumar',        'ravi@xyz.com',      SHA2('emp456',   256), '9876543212', 'Finance',      'EMPLOYEE', 4.2, 30, 0);



CREATE TABLE candidate (
    id         INT          AUTO_INCREMENT PRIMARY KEY,
    c_name     VARCHAR(100) NOT NULL,
    c_mail     VARCHAR(100) UNIQUE NOT NULL,
    c_phone    VARCHAR(15),
    c_role     VARCHAR(50),
    c_yop      INT,
    created_at DATETIME     DEFAULT NOW()
);

-- Sample Data
INSERT INTO candidate (c_name, c_mail, c_phone, c_role, c_yop)
VALUES
('Arun Prasad',   'arun@gmail.com',   '9111111111', 'Java Developer',     2021),
('Sneha Reddy',   'sneha@gmail.com',  '9222222222', 'Data Analyst',       2022),
('Kiran Babu',    'kiran@gmail.com',  '9333333333', 'DevOps Engineer',    2020);


CREATE TABLE ats_result (
    id              INT           AUTO_INCREMENT PRIMARY KEY,
    candidate_email VARCHAR(100)  UNIQUE NOT NULL,
    score           INT           DEFAULT 0,
    decision        VARCHAR(20),
    reason          TEXT,
    evaluated_at    DATETIME      DEFAULT NOW(),
    FOREIGN KEY (candidate_email) REFERENCES candidate(c_mail)
);

-- Sample Data
INSERT INTO ats_result (candidate_email, score, decision, reason)
VALUES
('arun@gmail.com',  85, 'SHORTLISTED', 'Strong Java skills and relevant experience.'),
('sneha@gmail.com', 60, 'REJECTED',    'Lacks required data engineering tools experience.'),
('kiran@gmail.com', 78, 'SHORTLISTED', 'Good DevOps background with CI/CD knowledge.');



CREATE TABLE interview (
    id             INT         AUTO_INCREMENT PRIMARY KEY,
    candidate_id   INT         NOT NULL,
    interviewer_id VARCHAR(20),
    scheduled_at   DATETIME,
    status         VARCHAR(20) DEFAULT 'SCHEDULED',
    created_at     DATETIME    DEFAULT NOW(),
    FOREIGN KEY (candidate_id)   REFERENCES candidate(id),
    FOREIGN KEY (interviewer_id) REFERENCES employee(emp_id)
);

-- Sample Data
INSERT INTO interview (candidate_id, interviewer_id, scheduled_at, status)
VALUES
(1, 'EMP002', '2026-03-25 10:00:00', 'SCHEDULED'),
(3, 'EMP002', '2026-03-26 11:00:00', 'SCHEDULED'),
(1, 'EMP003', '2026-03-27 14:00:00', 'COMPLETED');



CREATE TABLE leave_request (
    id           INT          AUTO_INCREMENT PRIMARY KEY,
    emp_id       VARCHAR(20)  NOT NULL,
    days         INT          NOT NULL,
    reason       TEXT,
    status       VARCHAR(20)  DEFAULT 'PENDING',
    risk_score   DECIMAL(4,3) DEFAULT 0.000,
    ai_reasoning TEXT,
    approved_by  VARCHAR(20),
    created_at   DATETIME     DEFAULT NOW(),
    updated_at   DATETIME     DEFAULT NOW(),
    FOREIGN KEY (emp_id)      REFERENCES employee(emp_id),
    FOREIGN KEY (approved_by) REFERENCES employee(emp_id)
);

-- Sample Data
INSERT INTO leave_request (emp_id, days, reason, status, risk_score, ai_reasoning)
VALUES
('EMP002', 3,  'Family function',       'APPROVED', 0.200, 'Low risk, no critical deadlines.'),
('EMP003', 5,  'Medical treatment',     'PENDING',  0.450, 'Moderate risk due to active project.'),
('EMP002', 10, 'Vacation',              'REJECTED', 0.850, 'High risk, critical project deadline near.');




CREATE TABLE skill (
    skill_id   INT          AUTO_INCREMENT PRIMARY KEY,
    skill_name VARCHAR(100) UNIQUE NOT NULL
);

-- Sample Data
INSERT INTO skill (skill_name)
VALUES
('Java'),
('Python'),
('DevOps'),
('MySQL'),
('MuleSoft'),
('React');


CREATE TABLE employee_skill (
    id                INT         AUTO_INCREMENT PRIMARY KEY,
    emp_id            VARCHAR(20) NOT NULL,
    skill_id          INT         NOT NULL,
    proficiency_level INT         DEFAULT 1,
    FOREIGN KEY (emp_id)   REFERENCES employee(emp_id),
    FOREIGN KEY (skill_id) REFERENCES skill(skill_id)
);

-- Sample Data
INSERT INTO employee_skill (emp_id, skill_id, proficiency_level)
VALUES
('EMP002', 1, 3),
('EMP002', 4, 2),
('EMP003', 3, 4),
('EMP003', 2, 2);



CREATE TABLE project_allocation (
    id           INT          AUTO_INCREMENT PRIMARY KEY,
    emp_id       VARCHAR(20)  NOT NULL,
    project_name VARCHAR(100) NOT NULL,
    weekly_hours INT          DEFAULT 0,
    deadline     DATE,
    critical     TINYINT(1)   DEFAULT 0,
    FOREIGN KEY (emp_id) REFERENCES employee(emp_id)
);

-- Sample Data
INSERT INTO project_allocation (emp_id, project_name, weekly_hours, deadline, critical)
VALUES
('EMP002', 'HRFlow Platform',   30, '2026-04-01', 1),
('EMP003', 'Finance Dashboard', 20, '2026-05-15', 0),
('EMP002', 'API Migration',     15, '2026-03-30', 1);



CREATE TABLE project_required_skill (
    id               INT          AUTO_INCREMENT PRIMARY KEY,
    project_name     VARCHAR(100) NOT NULL,
    skill_id         INT          NOT NULL,
    importance_level INT          DEFAULT 1,
    FOREIGN KEY (skill_id) REFERENCES skill(skill_id)
);

-- Sample Data
INSERT INTO project_required_skill (project_name, skill_id, importance_level)
VALUES
('HRFlow Platform',   1, 3),
('HRFlow Platform',   5, 3),
('Finance Dashboard', 4, 2),
('API Migration',     5, 3);


CREATE TABLE skill_market_availability (
    id             INT AUTO_INCREMENT PRIMARY KEY,
    skill_id       INT NOT NULL,
    scarcity_level INT DEFAULT 1,
    FOREIGN KEY (skill_id) REFERENCES skill(skill_id)
);

-- Sample Data
INSERT INTO skill_market_availability (skill_id, scarcity_level)
VALUES
(1, 2),
(3, 4),
(5, 5);


CREATE TABLE complaint (
    id                     INT          AUTO_INCREMENT PRIMARY KEY,
    emp_id                 VARCHAR(20)  NOT NULL,
    complaint_type         VARCHAR(50),
    complaint_description  TEXT,
    filed_at               DATETIME     DEFAULT NOW(),
    FOREIGN KEY (emp_id) REFERENCES employee(emp_id)
);

-- Sample Data
INSERT INTO complaint (emp_id, complaint_type, complaint_description)
VALUES
('EMP002', 'Harassment',     'Inappropriate comments made during team meeting.'),
('EMP003', 'Work Overload',  'Consistently assigned tasks beyond defined scope.'),
('EMP002', 'Policy Breach',  'Attendance policy not being followed by team lead.');


CREATE TABLE resignation_analysis (
    id                           INT          AUTO_INCREMENT PRIMARY KEY,
    emp_id                       VARCHAR(20)  NOT NULL,
    impact_level                 VARCHAR(10),
    risk_score                   DECIMAL(4,3) DEFAULT 0.000,
    replacement_difficulty       VARCHAR(10),
    knowledge_transfer_required  TINYINT(1)   DEFAULT 0,
    retention_suggestion         TEXT,
    reason                       TEXT,
    analyzed_at                  DATETIME     DEFAULT NOW(),
    FOREIGN KEY (emp_id) REFERENCES employee(emp_id)
);

-- Sample Data
INSERT INTO resignation_analysis (emp_id, impact_level, risk_score, replacement_difficulty, knowledge_transfer_required, retention_suggestion, reason)
VALUES
('EMP002', 'HIGH',   0.850, 'HIGH',   1, 'Offer promotion and salary revision.',     'Better opportunity abroad.'),
('EMP003', 'MEDIUM', 0.500, 'MEDIUM', 0, 'Provide flexible work from home options.', 'Personal health reasons.'),
('EMP002', 'LOW',    0.200, 'LOW',    0, 'No immediate action required.',            'Relocation to home city.');