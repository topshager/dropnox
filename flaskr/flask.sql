
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username VARCHAR(77) UNIQUE NOT NULL,
  password VARCHAR(55) NOT NULL
);


CREATE TABLE folders (
  folder_id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  parent_id INT REFERENCES folders(folder_id) ON DELETE CASCADE,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);


CREATE TABLE files (
  file_id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  folder_id INT REFERENCES folders(folder_id) ON DELETE CASCADE,
  size BIGINT NOT NULL,
  typ TEXT NOT NULL,
  content BYTEA,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()        
);
