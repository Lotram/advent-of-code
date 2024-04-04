advent_of_code::solution!(8);
use lazy_static::lazy_static;
use regex::{Captures, Regex};
use std::collections::HashMap;
lazy_static! {
    static ref PATTERN: Regex =
        Regex::new(r"(?P<position>\w{3}) = \((?P<left>\w{3}), (?P<right>\w{3})\)",).unwrap();
}

fn get_cap(caps: &Captures, name: &str) -> String {
    caps.name(name).unwrap().as_str().to_string()
}

pub fn part_one(input: &str) -> Option<u32> {
    let lines: Vec<&str> = input.trim().split("\n").collect();
    let mut directions = lines[0].chars().cycle();
    let mut instructions = HashMap::new();
    let mut current_position = "AAA".to_string();
    let end_position = "ZZZ".to_string();
    let mut counter: u32 = 0;

    for line in lines.iter().skip(2) {
        let caps = PATTERN.captures(line).unwrap();
        let left = get_cap(&caps, "left");
        let right = get_cap(&caps, "right");
        let position = get_cap(&caps, "position");
        instructions.insert(position, (left, right));
    }
    loop {
        counter += 1;

        let direction = directions.next().unwrap();
        let instruction = instructions.get(&current_position).unwrap();
        if direction == 'R' {
            current_position = instruction.1.clone();
        } else {
            current_position = instruction.0.clone();
        }
        if current_position == end_position {
            return Some(counter);
        }
    }
}

pub fn part_two(input: &str) -> Option<u32> {
    let lines: Vec<&str> = input.trim().split("\n").collect();
    let mut directions = lines[0].chars().cycle();
    let mut instructions = HashMap::new();
    let mut counter: u32 = 0;

    for line in lines.iter().skip(2) {
        let caps = PATTERN.captures(line).unwrap();
        let left = get_cap(&caps, "left");
        let right = get_cap(&caps, "right");
        let position = get_cap(&caps, "position");
        instructions.insert(position, (left, right));
    }
    let mut current_positions: Vec<String> = Vec::new();
    for node in instructions.keys() {
        let last_char = node.chars().skip(2).next().unwrap();
        if last_char == 'A' {
            current_positions.push(node.clone());
        }
    }

    loop {
        counter += 1;

        let direction = directions.next().unwrap();
        let mut new_positions: Vec<String> = Vec::new();
        for pos in current_positions {
            let instruction = instructions.get(&pos).unwrap();

            if direction == 'R' {
                new_positions.push(instruction.1.clone());
            } else {
                new_positions.push(instruction.0.clone());
            }
        }
        let mut is_over = true;
        current_positions = new_positions;

        for pos in &current_positions {
            let last_char = pos.chars().skip(2).next().unwrap();
            if last_char != 'Z' {
                is_over = false
            }
        }
        if is_over {
            return Some(counter);
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let result = part_one(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, Some(6));
    }

    #[test]
    fn test_part_two() {
        let result = part_two(&advent_of_code::template::read_file_part(
            "examples", DAY, 2,
        ));
        assert_eq!(result, Some(6));
    }
}
