use std::{
    fs::{self, File, OpenOptions},
    io::Write,
    path::Path,
    process,
};

use crate::{template::aoc_cli::get_year, Day};

const MODULE_TEMPLATE: &str = r#"advent_of_code::solution!(DAY_NUMBER);

pub fn part_one(input: &str) -> Option<u32> {
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
"#;

const PYTHON_TEMPLATE: &str = r#"def part_1(text):
    result = None
    return result


def part_2(text):
    result = None
    return result
"#;

fn safe_create_file(path: &str) -> Result<File, std::io::Error> {
    let _path = Path::new(&path);
    fs::create_dir_all(_path.parent().unwrap()).unwrap();
    OpenOptions::new().write(true).create_new(true).open(path)
}

fn create_file(path: &str) -> Result<File, std::io::Error> {
    let _path = Path::new(&path);
    fs::create_dir_all(_path.parent().unwrap()).unwrap();
    OpenOptions::new().write(true).create(true).open(path)
}

pub fn handle(day: Day, python: bool, rust: bool) {
    let year = get_year().unwrap();
    let input_path = format!("data/inputs/{year}/{day}.txt");
    let example_path = format!("data/examples/{year}/{day}.txt");
    let module_path = format!("src/bin/year_{year}/{day}.rs");
    let python_path = format!("src/bin/year_{year}/day_{day}.py");

    if rust {
        let mut file = match safe_create_file(&module_path) {
            Ok(file) => file,
            Err(e) => {
                eprintln!("Failed to create module file: {e}");
                process::exit(1);
            }
        };

        match file.write_all(
            MODULE_TEMPLATE
                .replace("DAY_NUMBER", &day.into_inner().to_string())
                .as_bytes(),
        ) {
            Ok(()) => {
                println!("Created module file \"{}\"", &module_path);
            }
            Err(e) => {
                eprintln!("Failed to write module contents: {e}");
                process::exit(1);
            }
        }
    }
    if python {
        let mut file = match safe_create_file(&python_path) {
            Ok(file) => file,
            Err(e) => {
                eprintln!("Failed to create python file: {e}");
                process::exit(1);
            }
        };

        match file.write_all(PYTHON_TEMPLATE.as_bytes()) {
            Ok(_) => {
                println!("Created python file \"{}\"", &python_path);
            }
            Err(e) => {
                eprintln!("Failed to create python file: {e}");
                process::exit(1);
            }
        }
    }

    match create_file(&input_path) {
        Ok(_) => {
            println!("Created empty input file \"{}\"", &input_path);
        }
        Err(e) => {
            eprintln!("Failed to create input file: {e}");
            process::exit(1);
        }
    }

    match create_file(&example_path) {
        Ok(_) => {
            println!("Created empty example file \"{}\"", &example_path);
        }
        Err(e) => {
            eprintln!("Failed to create example file: {e}");
            process::exit(1);
        }
    }

    println!("---");
    println!("🎄 Type `cargo solve {}` to run your solution.", day);
}
