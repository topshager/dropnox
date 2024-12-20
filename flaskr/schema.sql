DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS folders ;
DROP TABLE IF EXISTS files ;

CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username VARCHAR(77) UNIQUE NOT NULL,
  password VARCHAR(55) NOT NULL
);

CREATE TABLE folders (
  folder_id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  parent_id INTEGER,
  id INTEGER,
  typ TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (parent_id) REFERENCES folders(folder_id) ON DELETE CASCADE,
  FOREIGN KEY (id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE files (
  file_id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  folder_id INTEGER,
  typ TEXT NOT NULL,
  content BLOB NOT NULL,
  id INTEGER NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (folder_id) REFERENCES folders(folder_id) ON DELETE CASCADE,
  FOREIGN KEY (id) REFERENCES users(id) ON DELETE CASCADE
);
