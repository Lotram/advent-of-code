use lazy_static::lazy_static;
use regex::Regex;
use std::collections::HashMap;

lazy_static! {
    static ref PATTERN: Regex = Regex::new(r"(?P<size>\d+) (?P<filename>\S+)").unwrap();
}
advent_of_code::solution!(7);

enum Command {
    Cd(String),
    Ls,
}

#[derive(Debug, Clone)]
struct Directory {
    name: String,
    parent: Option<Box<Directory>>,
    files: HashMap<String, u32>, // map of file name to file size
    directories: HashMap<String, Directory>, // map of directory name to directory
}

impl Directory {
    fn new(name: &str, parent: Option<Box<Directory>>) -> Directory {
        Directory {
            name: String::from(name),
            files: HashMap::new(),
            directories: HashMap::new(),
            parent: parent,
        }
    }

    fn add_file(&mut self, name: &str, size: u32) {
        self.files.insert(String::from(name), size);
    }

    fn add_directory(&mut self, name: &str, directory: &Directory) {
        self.directories.insert(String::from(name), *directory);
    }

    fn get_file_size(&self, name: &str) -> Option<&u32> {
        self.files.get(name)
    }

    fn get_directory(&mut self, name: &str) -> Option<&mut Directory> {
        self.directories.get_mut(name)
    }
}

pub fn part_one(input: &str) -> Option<u32> {
    let lines: Vec<&str> = input.split("\n").collect();
    let mut root_dir = Directory::new("/", None);
    let mut current_dir = &mut root_dir;
    for line in lines {
        if line.chars().next().unwrap() == '$' {
            let command: Vec<&str> = line.split(" ").collect();
            if command[1] == "cd" {
                let parent = &current_dir;
                let new_dir = current_dir.get_directory(command[2]);
                if new_dir.is_none() {
                    let new_dir = Directory::new(command[2], Some(Box(parent)));
                }
                current_dir.add_directory("..", *parent)
            }
        } else {
            let caps = PATTERN.captures(line).expect(line);
            let size: u32 = caps.name("size").unwrap().as_str().parse().unwrap();
            // let filename = String::from(caps.name("size").unwrap().as_str());
            let filename = caps.name("size").unwrap().as_str();
            current_dir.add_file(filename, size)
        }
    }
    None
}

pub fn part_two(input: &str) -> Option<u32> {
    None
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let result = part_one(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, None);
    }

    #[test]
    fn test_part_two() {
        let result = part_two(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, None);
    }
}
